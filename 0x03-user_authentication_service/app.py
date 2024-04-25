#!/usr/bin/env python3
"""Flask application
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)

@app.route('/')
def home():
    """it returns json payload of form
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST', 'GET'])
def users(email: str, password: str) -> str:
    """It registers a user
    """
    
    email = request.form.get('email')
    password = request.form.get('password')

    if request.method == 'POST':
        try:
            user = AUTH.register_user(email, password)
            return jsonify({"email": user.email, "message": "user created"})
        
        except Exception:
            return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """it logs a user into the application
    """

    email = request.form.get('email')
    password = request.form.get('password')

    if not (AUTH.valid_login(email, password)):
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie('session_id', session_id)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """it logs a user out
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return None
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """It finds user using session_id.  If the 
    user exist, respond with a 200 HTTP status 
    and the following JSON payload:
    {"email": "<user email>"}
    """

    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """Gets email from request.
    If the email is not registered, respond with a 403 
    status code. Otherwise, generate a token and respond 
    with a 200 HTTP status and the following JSON payload:
    {"email": "<user email>", "reset_token": "<reset token>"}
    """
    email = request.form.get('email')
    try:
        reset_token = Auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """It updates password.
    If the token is invalid, catch the exception and respond with a 403 HTTP code.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")