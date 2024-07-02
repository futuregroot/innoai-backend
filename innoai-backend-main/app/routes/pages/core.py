from flask import Blueprint, render_template, redirect, url_for
import subprocess
import os

core_bp = Blueprint("core", __name__, url_prefix="/")

@core_bp.route("/")
def home_route():
    return render_template("pages/home.html")
# Default Streamlit port