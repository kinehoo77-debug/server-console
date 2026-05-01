import functools
import hmac

from flask import current_app, jsonify, redirect, request, session, url_for


def verify_password(password: str) -> bool:
    expected = str(current_app.config.get("ADMIN_PASSWORD", ""))
    return hmac.compare_digest(password, expected)


def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        if session.get("is_admin"):
            return view_func(*args, **kwargs)
        if request.path.startswith("/api/"):
            return jsonify({"ok": False, "message": "未登录或会话已过期"}), 401
        return redirect(url_for("auth.login"))

    return wrapper
