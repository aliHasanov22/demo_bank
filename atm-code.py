#!/usr/bin/python3
from flask import Flask, request, jsonify
from datetime import datetime
from collections import deque

app = Flask(__name__)


# --- Məlumat Modeli (Sizin account sinfiniz əsasında) ---
class ATMBackend:
    def __init__(self, pin="1234", balance=1000.0):
        self.pin = pin
        self.balance = balance
        self.withdraw_limit = 1000.0
        self.transactions = deque(maxlen=10)
        self.is_authenticated = False

    def add_transaction(self, ttype, amount, note=""):
        self.transactions.appendleft({
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "type": ttype,
            "amount": amount,
            "balance": self.balance,
            "note": note
        })


# ATM obyektini yaradırıq (Real layihədə bu verilənlər bazasından gəlir)
atm = ATMBackend()


# --- Routing / Endpoints ---

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    entered_pin = data.get('pin')

    if atm.pin == entered_pin:
        atm.is_authenticated = True
        atm.add_transaction("LOGIN", 0.0, "Uğurlu giriş")
        return jsonify({"message": "Giriş uğurludur", "status": "success"}), 200
    return jsonify({"message": "PIN yanlışdır", "status": "error"}), 401


@app.route('/balance', methods=['GET'])
def get_balance():
    if not atm.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"balance": atm.balance}), 200


@app.route('/withdraw', methods=['POST'])
def withdraw():
    if not atm.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    amount = data.get('amount')

    if amount <= 0:
        return jsonify({"error": "Məbləğ müsbət olmalıdır"}), 400
    if amount > atm.balance:
        return jsonify({"error": "Balans kifayət deyil"}), 400
    if amount > atm.withdraw_limit:
        return jsonify({"error": f"Limit aşıldı: {atm.withdraw_limit}"}), 400

    atm.balance -= amount
    atm.add_transaction("WITHDRAW", amount)
    return jsonify({"message": "Vəsait çıxarıldı", "new_balance": atm.balance}), 200


@app.route('/deposit', methods=['POST'])
def deposit():
    if not atm.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    amount = data.get('amount')

    if amount <= 0:
        return jsonify({"error": "Məbləğ müsbət olmalıdır"}), 400

    atm.balance += amount
    atm.add_transaction("DEPOSIT", amount)
    return jsonify({"message": "Məbləğ daxil edildi", "new_balance": atm.balance}), 200


@app.route('/statement', methods=['GET'])
def statement():
    if not atm.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(list(atm.transactions)), 200


@app.route('/logout', methods=['POST'])
def logout():
    atm.is_authenticated = False
    return jsonify({"message": "Sistemdən çıxış edildi"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
