from flask import Flask, render_template, redirect, url_for, request, session, flash
import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import sqlite3

conn = sqlite3.connect('users.db')

app = Flask(__name__)
app.secret_key = "hello"

def data_entry(name, email, password):
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        c.close()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form["nm"]
        email = request.form["email"]
        password = request.form["pass"]
        session["name"] = name
        session["email"] = email
        session["password"] = password
        data_entry(name, email, password) #save into our database (will encrypt password later)
    return render_template("register.html")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)