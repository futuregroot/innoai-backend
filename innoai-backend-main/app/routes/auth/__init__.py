from flask import Blueprint, jsonify, request, session
from flask_login import login_required, current_user, login_user, logout_user

from app.models.auth import User
from app.extensions import db, bcrypt, limiter, csrf
from flask_wtf.csrf import generate_csrf, validate_csrf, CSRFError

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/get-csrf-token", methods=["GET"])
def get_csrf_token():
    # CSRF 토큰 생성 및 전송
    csrf_token = generate_csrf()
    session['_csrf_token'] = csrf_token  # 세션에 저장
    return jsonify({"csrf_token": csrf_token}), 200

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("30/minute")
def login():
    if current_user.is_authenticated:
        return jsonify({"message": "Already authenticated"}), 200

    csrf_token = request.json.get("csrf_token")
    if not csrf_token:
        return jsonify({"message": "CSRF token is missing"}), 400

    session_csrf_token = session.get('_csrf_token')
    if csrf_token != session_csrf_token:
        return jsonify({"message": "Invalid CSRF token"}), 400

    if request.is_json:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        remember_me = data.get("remember_me", False)

        user = User.query.filter_by(email=email).one_or_none()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember_me)
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({"message": "Invalid request format"}), 400

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("30/minute")
def register():
    if current_user.is_authenticated:
        return jsonify({"message": "Already authenticated"}), 200

    csrf_token = request.json.get("csrf_token")
    if not csrf_token:
        return jsonify({"message": "CSRF token is missing"}), 400

    session_csrf_token = session.get('_csrf_token')
    if csrf_token != session_csrf_token:
        return jsonify({"message": "Invalid CSRF token"}), 400

    if request.is_json:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        hashed_password = bcrypt.generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return jsonify({"message": "Registration successful"}), 200

    return jsonify({"message": "Invalid request format"}), 400

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200