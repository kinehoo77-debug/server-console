import os
from pathlib import Path


def _default_file_root() -> str:
    if os.name == "nt":
        return str(Path.cwd())
    return "/"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "please-change-this-secret")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "replace-with-strong-password")
    PORT = int(os.getenv("PORT", "7010"))
    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "200"))
    FILE_ROOT = os.getenv("FILE_ROOT", _default_file_root())
    LOG_FILE = os.getenv("LOG_FILE", "")
    LOG_TAIL_LINES = int(os.getenv("LOG_TAIL_LINES", "300"))
    DOCKER_PANEL_URL = os.getenv("DOCKER_PANEL_URL", "http://38.76.188.104:7080/")
