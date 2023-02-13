from flask import Blueprint, render_template

example = Blueprint("example", __name__)

# View / Routes for app

@example.route("/")
def index():
    return render_template("example_base/staff_base_eg.html")
