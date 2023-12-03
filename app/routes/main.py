from flask import Flask, flash, Blueprint, render_template

home = Blueprint("/", __name__)


@home.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")
