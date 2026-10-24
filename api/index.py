from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

# كود واجهة المستخدم HTML
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading AI Assistant</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { font-family: Tahoma, sans-serif; background: #0f172a; color: #fff; margin: 0; padding: 15px; text-align: center; }
        .card { background: #1e293b; border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h2 { color: #f59e0b; margin-top: 5px; }
        button { background: #3b82f6; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 16px; cursor: pointer; width: 100%; margin-top: 10px; font-weight: bold; }
        button:active { background: #2563eb; }
        .res { margin-top: 15px; background: #0f172a; padding: 10px; border-radius: 8px; text-align: right; font-size: 14px; display: none; }
    </style>
</head>
<body>
    <h2>🤖 بوت التحليل الذكي للذهب والعملات</h2>
    <p style="color: #94a3b8; font-size: 13px;">تحليل فني لحظي وإشارات دقيقة لـ XAUUSD</p>

    <div class="card">
        <h3>📊 تحليل السوق (Market Analysis)</h3>
        <button onclick="getAnalysis()">احصل على التحليل الفني</button>
        <div id="analysisResult" class="res">جاري التحليل...</div>
    </div>

    <div class="card">
        <h3>⚡ إشارة تداول فورية (Live Signal)</h3>
        <button onclick="getSignal()" style="background: #10b981;">طلب صفقة الآن</button>
        <div id="signalResult" class="res">جاري توليد الإشارة...</div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        function getAnalysis() {
            const resDiv = document.getElementById('analysisResult');
            resDiv.style.display = 'block';
            resDiv.innerHTML = "⏳ جاري فحص الشموع والدعوم...";
            fetch('/api/analyze?symbol=XAUUSD')
                .then(res => res.json())
                .then(data => {
                    resDiv.innerHTML = `📈 الاتجاه: <b>${data.trend}</b><br>💪 القوة: <b>${data.strength}%</b><br>🛡️ الدعم: <b>${data.support}</b><br>⚔️ المقاومة: <b>${data.resistance}</b>`;
                }).catch(() => { resDiv.innerHTML = "❌ حدث خطأ في الاتصال بالسيرفر"; });
        }

        function getSignal() {
            const resDiv = document.getElementById('signalResult');
            resDiv.style.display = 'block';
            resDiv.innerHTML = "⏳ جاري حساب نقاط الدخول...";
            fetch('/api/signal?symbol=XAUUSD')
                .then(res => res.json())
                .then(data => {
                    resDiv.innerHTML = `🎯 الإشارة: <b>${data.action}</b><br>📌 نقطة الدخول: <b>${data.entry}</b><br>🛑 وقف الخسارة (SL): <b>${data.sl}</b><br>✅ الأهداف (TP): <b>${data.tp}</b>`;
                }).catch(() => { resDiv.innerHTML = "❌ حدث خطأ في الاتصال بالسيرفر"; });
        }
    </script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/analyze', methods=['GET'])
def analyze():
    return jsonify({
        "status": "success",
        "symbol": "XAUUSD",
        "trend": "صاعد (Bullish)",
        "strength": 85,
        "support": "2710.50",
        "resistance": "2745.00"
    })

@app.route('/api/signal', methods=['GET'])
def signal():
    return jsonify({
        "status": "success",
        "action": "شراء (BUY) 🟢",
        "entry": "2722.10",
        "sl": "2712.00",
        "tp": "2738.50"
    })
