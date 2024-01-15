from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from flask_mail import Mail, Message

import bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = "TEMP_SECRET_KEY_LOL"

conn = sqlite3.connect('accounts.db')


# cursor.execute('''
#     CREATE TABLE users (
#         id INTEGER PRIMARY KEY,
#         name TEXT NOT NULL,
#         email TEXT NOT NULL,
#         password TEXT NOT NULL
#     )
# ''')


def data_entry(name, email, password):
    with sqlite3.connect("accounts.db") as conn:
        c = conn.cursor()
        list_of_email = c.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
        if list_of_email == []:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            # msg = Message("Verification Test", sender='noreply@mailtrap.club', recipients=['james.cai4@student.tdsb.on.ca'])
            # msg.body = "verification test"
            # mail.send(msg)
            return True
        else:
            print("You already have an account. Please contact admin for changes.")
        conn.commit()
        c.close()


def verify_login(email, password):
    with sqlite3.connect("accounts.db") as conn:
        c = conn.cursor()
        list_of_email = c.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
        if list_of_email == []:
            print("not found")
            return False
        else:
            list_of_pass = c.execute("SELECT password FROM users WHERE email = ?", (email,)).fetchone()
            if bcrypt.checkpw(password.encode('utf-8'), list_of_pass[0]):
                print("successfully logged in!")
                return True
        conn.commit()
        c.close()


def findName(email):
    with sqlite3.connect("accounts.db") as conn:
        c = conn.cursor()
        list_of_name = c.execute("SELECT name FROM users WHERE email = ?", (email,)).fetchall()
        if list_of_name != []:
            name = list_of_name[0]
        conn.commit()
        c.close()
        return name


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if not "email" in session:
        if request.method == "POST":
            name = request.form["nm"]
            email = request.form["email"]
            password = request.form["pass"]
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            if data_entry(name, email, hashed):
                return redirect(url_for("login"))
        return render_template("register.html")
    else:
        return redirect(url_for("application"))


@app.route("/application", methods=["POST", "GET"])
def login():
    # initial check
    if not "email" in session:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["pass"]
            # check after submitting information
            if verify_login(email, password):
                session["email"] = email
                return redirect(url_for("application"))
    else:
        return redirect(url_for("application"))
    return render_template("login.html")


@app.route("/start-application")
def application():
    name = findName(session["email"])[0]
    print(name)
    if "email" in session:
        return render_template("application.html", name=name)
    else:
        return redirect(url_for("login"))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
