from flask import Blueprint, render_template, redirect, url_for
from .controllers import Controller

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def register():
    users, status, form = Controller.home()

    if status:
        return redirect(url_for("main.register"))

    return render_template("register.html", form=form, users=users)


@main.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    Controller.delete_user(user_id)
    return redirect(url_for("main.register"))
