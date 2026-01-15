#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, session, jsonify
from account import Account

app = Flask(__name__)
app.secret_key = "atm_secret_key"

account = Account("1234", 1000.0)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pin = request.form["pin"]
        if account.check_pin(pin):
            session["logged_in"] = True
            return redirect("/dashboard")
        return render_template("login.html", error="Wrong PIN")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("dashboard.html", balance=account.balance)

@app.route("/withdraw", methods=["POST"])
def withdraw():
    amt = float(request.form["amount"])
    success = account.withdraw(amt)
    return redirect("/dashboard")

@app.route("/deposit", methods=["POST"])
def deposit():
    amt = float(request.form["amount"])
    account.deposit(amt)
    return redirect("/dashboard")

@app.route("/statement")
def statement():
    return jsonify(account.ministatement(10))

@app.route("/changepin", methods=["POST"])
def changepin():
    old = request.form["old"]
    new = request.form["new"]
    if account.check_pin(old):
        account.changepin(new)
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

