from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/api/analyze', methods=['GET'])
def api_analyze():
    symbol = request.args.get('symbol', 'XAUUSD')
    trend = random.choice(["صاعد 📈 (Bullish)", "هابط 📉 (Bearish)", "عرضي ⚖️ (Sideways)"])
    strength = random.randint(55, 92)
    base_price = 2650.0 if symbol == 'XAUUSD' else 1.0850
    return jsonify({
        "trend": trend,
        "strength": strength,
        "support": round(base_price * 0.994, 2),
        "resistance": round(base_price * 1.006, 2)
    })

@app.route('/api/signal', methods=['GET'])
def api_signal():
    symbol = request.args.get('symbol', 'XAUUSD')
    action = random.choice(["شراء (BUY)", "بيع (SELL)"])
    entry = 2652.5 if symbol == 'XAUUSD' else 1.0845
    return jsonify({
        "action": action,
        "accuracy": random.randint(70, 95),
        "entry": entry,
        "sl": round(entry - 5.0 if action == "شراء (BUY)" else entry + 5.0, 2),
        "tp": round(entry + 12.0 if action == "شراء (BUY)" else entry - 12.0, 2)
    })
