from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


class FileService:
    def __init__(self, root_path: str) -> None:
        self.root = Path(root_path).resolve()

    def resolve(self, virtual_path: str) -> Path:
        base = virtual_path.strip() if virtual_path else "/"
        relative = base.lstrip("/")
        target = (self.root / relative).resolve()
        if not self._is_in_root(target):
            raise ValueError("非法路径访问")
        return target

    def list_dir(self, virtual_path: str) -> dict:
        current = self.resolve(virtual_path)
        if not current.exists():
            raise FileNotFoundError("目录不存在")
        if not current.is_dir():
            raise NotADirectoryError("当前路径不是目录")

        entries = []
        for item in current.iterdir():
            stat = item.stat()
            entries.append(
                {
                    "name": item.name,
                    "is_dir": item.is_dir(),
                    "size": stat.st_size if item.is_file() else 0,
                    "mtime": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "path": self.to_virtual(item),
                    "type": self.file_type(item),
                }
            )
        entries.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        current_virtual = self.to_virtual(current)
        return {
            "current": current_virtual,
            "parent": self.parent_virtual(current_virtual),
            "entries": entries,
        }

    def save_upload(self, virtual_path: str, files: list[FileStorage]) -> dict:
        target_dir = self.resolve(virtual_path)
        if not target_dir.exists():
            raise FileNotFoundError("目标目录不存在")
        if not target_dir.is_dir():
            raise NotADirectoryError("目标路径不是目录")

        saved = []
        for file in files:
            if not file.filename:
                continue
            safe_name = secure_filename(file.filename) or file.filename
            full_path = target_dir / safe_name
            file.save(full_path)
            saved.append(safe_name)
        return {"saved": saved}

    def delete(self, virtual_path: str) -> None:
        target = self.resolve(virtual_path)
        if not target.exists():
            raise FileNotFoundError("文件不存在")
        if target == self.root:
            raise ValueError("不允许删除根目录")
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()

    def rename(self, virtual_path: str, new_name: str) -> dict:
        new_name = new_name.strip()
        if not new_name:
            raise ValueError("新名称不能为空")

        target = self.resolve(virtual_path)
        if target == self.root:
            raise ValueError("不允许重命名根目录")
        new_path = target.parent / new_name
        new_path = new_path.resolve()
        if not self._is_in_root(new_path):
            raise ValueError("非法目标路径")
        if new_path.exists():
            raise FileExistsError("目标名称已存在")
        target.rename(new_path)
        return {"path": self.to_virtual(new_path)}

    def mkdir(self, virtual_path: str, name: str) -> dict:
        folder_name = name.strip()
        if not folder_name:
            raise ValueError("目录名不能为空")

        target = self.resolve(virtual_path)
        folder = (target / folder_name).resolve()
        if not self._is_in_root(folder):
            raise ValueError("非法目录路径")
        folder.mkdir(parents=False, exist_ok=False)
        return {"path": self.to_virtual(folder)}

    def read_text(self, virtual_path: str, max_bytes: int = 2 * 1024 * 1024) -> dict:
        target = self.resolve(virtual_path)
        if not target.exists() or not target.is_file():
            raise FileNotFoundError("文件不存在")
        if target.stat().st_size > max_bytes:
            raise ValueError("文件过大，无法在线编辑")
        content = target.read_text(encoding="utf-8", errors="ignore")
        return {"content": content, "path": self.to_virtual(target)}

    def write_text(self, virtual_path: str, content: str) -> None:
        target = self.resolve(virtual_path)
        if not target.exists() or not target.is_file():
            raise FileNotFoundError("文件不存在")
        target.write_text(content, encoding="utf-8")

    def get_file_path(self, virtual_path: str) -> Path:
        target = self.resolve(virtual_path)
        if not target.exists() or not target.is_file():
            raise FileNotFoundError("文件不存在")
        return target

    def to_virtual(self, path_obj: Path) -> str:
        rel = path_obj.resolve().relative_to(self.root)
        rel_txt = rel.as_posix()
        return "/" if rel_txt == "." else f"/{rel_txt}"

    @staticmethod
    def parent_virtual(virtual_path: str) -> str | None:
        if virtual_path == "/":
            return None
        parent = str(Path(virtual_path).parent).replace("\\", "/")
        if not parent.startswith("/"):
            parent = f"/{parent}"
        return parent if parent else "/"

    @staticmethod
    def file_type(path_obj: Path) -> str:
        if path_obj.is_dir():
            return "dir"
        suffix = path_obj.suffix.lower()
        if suffix in {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg"}:
            return "image"
        if suffix in {".txt", ".log", ".json", ".yaml", ".yml", ".ini", ".conf", ".py", ".js", ".css", ".html", ".md", ".sh"}:
            return "text"
        return "binary"

    def _is_in_root(self, target: Path) -> bool:
        try:
            target.relative_to(self.root)
            return True
        except ValueError:
            return False
