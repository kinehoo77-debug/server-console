from __future__ import annotations

from pathlib import Path


class LogService:
    def __init__(self, log_file: str, file_root: str) -> None:
        self.file_root = Path(file_root).resolve()
        self.log_path = self._choose_log_file(log_file)

    def read_logs(self, lines: int = 300, keyword: str = "") -> dict:
        lines = max(10, min(lines, 2000))
        if not self.log_path.exists():
            return {"path": str(self.log_path), "content": "日志文件不存在"}

        content = self._tail(self.log_path, lines)
        if keyword.strip():
            matched = [line for line in content.splitlines() if keyword.lower() in line.lower()]
            content = "\n".join(matched)
        return {"path": str(self.log_path), "content": content}

    def _choose_log_file(self, value: str) -> Path:
        if value:
            return Path(value).resolve()

        candidates = [
            self.file_root / "var/log/syslog",
            self.file_root / "var/log/messages",
            self.file_root / "var/log/auth.log",
        ]
        for file in candidates:
            if file.exists():
                return file
        return candidates[0]

    @staticmethod
    def _tail(path_obj: Path, lines: int) -> str:
        with path_obj.open("rb") as f:
            f.seek(0, 2)
            end = f.tell()
            block = 1024
            data = bytearray()
            while end > 0 and data.count(b"\n") <= lines:
                read_size = min(block, end)
                end -= read_size
                f.seek(end)
                data = f.read(read_size) + data
            text = data.decode("utf-8", errors="ignore")
            return "\n".join(text.splitlines()[-lines:])
