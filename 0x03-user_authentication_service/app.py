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
    




if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")