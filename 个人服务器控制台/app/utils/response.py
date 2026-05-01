from flask import jsonify


def ok(data: dict | None = None):
    payload = {"ok": True}
    if data:
        payload.update(data)
    return jsonify(payload)


def fail(message: str, code: int = 400):
    return jsonify({"ok": False, "message": message}), code
