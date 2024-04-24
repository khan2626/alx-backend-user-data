#!/usr/bin/env python3
"""Flask application
"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)

@app.route('/')
def home():
    """it returns json payload of form
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users(email, password):
    """It registers a user
    """
    
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 400
    
    except Exception as e:
        return jsonify({"message": "email already registered"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)