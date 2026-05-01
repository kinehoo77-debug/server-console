from __future__ import annotations

from flask import Blueprint, Response, current_app, render_template, request, send_file

from app.services.file_service import FileService
from app.services.log_service import LogService
from app.services.monitor_service import MonitorService
from app.utils.auth import login_required
from app.utils.response import fail, ok

main_bp = Blueprint("main", __name__)


def _file_service() -> FileService:
    return FileService(current_app.config["FILE_ROOT"])


def _log_service() -> LogService:
    return LogService(current_app.config["LOG_FILE"], current_app.config["FILE_ROOT"])


@main_bp.route("/")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        active_page="dashboard",
        docker_panel_url=current_app.config["DOCKER_PANEL_URL"],
    )


@main_bp.route("/files")
@login_required
def files_page():
    return render_template(
        "files.html",
        active_page="files",
        docker_panel_url=current_app.config["DOCKER_PANEL_URL"],
    )


@main_bp.route("/logs")
@login_required
def logs_page():
    return render_template(
        "logs.html",
        active_page="logs",
        docker_panel_url=current_app.config["DOCKER_PANEL_URL"],
    )


@main_bp.route("/api/system/info")
@login_required
def system_info():
    return ok({"info": MonitorService.get_system_info()})


@main_bp.route("/api/system/metrics")
@login_required
def system_metrics():
    return ok({"metrics": MonitorService.get_metrics()})


@main_bp.route("/api/files/list")
@login_required
def files_list():
    path = request.args.get("path", "/")
    try:
        data = _file_service().list_dir(path)
        return ok(data)
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))


@main_bp.route("/api/files/upload", methods=["POST"])
@login_required
def files_upload():
    path = request.form.get("path", "/")
    files = request.files.getlist("files")
    if not files:
        return fail("未选择上传文件")
    try:
        data = _file_service().save_upload(path, files)
        return ok(data)
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))


@main_bp.route("/api/files/download")
@login_required
def files_download():
    path = request.args.get("path", "")
    if not path:
        return fail("缺少 path 参数")
    try:
        file_path = _file_service().get_file_path(path)
        return send_file(file_path, as_attachment=True, download_name=file_path.name)
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))


@main_bp.route("/api/files/raw")
@login_required
def files_raw():
    path = request.args.get("path", "")
    if not path:
        return fail("缺少 path 参数")
    try:
        file_path = _file_service().get_file_path(path)
        return send_file(file_path, as_attachment=False)
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))


@main_bp.route("/api/files/delete", methods=["POST"])
@login_required
def files_delete():
    payload = request.get_json(silent=True) or {}
    path = payload.get("path", "")
    if not path:
        return fail("缺少 path 参数")
    try:
        _file_service().delete(path)
        return ok()
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))


@main_bp.route("/api/files/rename", methods=["POST"])
@login_required
def files_rename():
    payload = request.get_json(silent=True) or {}
    path = payload.get("path", "")
    new_name = payload.get("new_name", "")
    if not path:
        return fail("缺少 path 参数")
    try:
        data = _file_service().rename(path, new_name)
        return ok(data)
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))


@main_bp.route("/api/files/mkdir", methods=["POST"])
@login_required
def files_mkdir():
    payload = request.get_json(silent=True) or {}
    path = payload.get("path", "/")
    name = payload.get("name", "")
    try:
        data = _file_service().mkdir(path, name)
        return ok(data)
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))


@main_bp.route("/api/files/read")
@login_required
def files_read():
    path = request.args.get("path", "")
    if not path:
        return fail("缺少 path 参数")
    try:
        data = _file_service().read_text(path)
        return ok(data)
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))


@main_bp.route("/api/files/write", methods=["POST"])
@login_required
def files_write():
    payload = request.get_json(silent=True) or {}
    path = payload.get("path", "")
    content = payload.get("content", "")
    if not path:
        return fail("缺少 path 参数")
    try:
        _file_service().write_text(path, content)
        return ok()
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))


@main_bp.route("/api/logs")
@login_required
def api_logs():
    lines = request.args.get("lines", current_app.config["LOG_TAIL_LINES"], type=int)
    search = request.args.get("search", "")
    try:
        data = _log_service().read_logs(lines=lines, keyword=search)
        return ok(data)
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))


@main_bp.route("/healthz")
def healthz() -> Response:
    return Response("ok", status=200, mimetype="text/plain")
