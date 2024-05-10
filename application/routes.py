from flask import Blueprint, render_template

# from .database.services import get_user, insert_user


main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html", title="Homepage")


# @main.route("/test")
# def test():
#     insert_user("lapochka3")
#     data = get_user("lapochka3")
#     return render_template("test.html", id = data["uuid"], name = data["user"], password = data["password"])
