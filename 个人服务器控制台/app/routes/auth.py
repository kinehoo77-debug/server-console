from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.utils.auth import verify_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("is_admin"):
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        password = request.form.get("password", "")
        if verify_password(password):
            session["is_admin"] = True
            return redirect(url_for("main.dashboard"))
        flash("密码错误，请重试。", "danger")

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
