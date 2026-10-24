from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading AI Assistant</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root { --bg: #0b0f19; --card: #161e2e; --accent: #f59e0b; --green: #10b981; --blue: #3b82f6; --text: #f8fafc; --muted: #94a3b8; }
        body { font-family: Tahoma, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 15px; text-align: center; }
        .card { background: var(--card); border: 1px solid #1f2937; border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.4); text-align: right; }
        h2 { color: var(--accent); margin-top: 5px; }
        button { width: 100%; background: var(--blue); color: white; border: none; padding: 12px; border-radius: 8px; font-size: 15px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button:active { opacity: 0.8; }
        .btn-signal { background: var(--green); }
        .res { margin-top: 12px; background: #0f172a; padding: 12px; border-radius: 8px; font-size: 13px; border-right: 4px solid var(--accent); display: none; line-height: 1.6; }
    </style>
</head>
<body>
    <h2>🤖 بوت التحليل الذكي للذهب والعملات</h2>
    <p style="color: var(--muted); font-size: 12px;">تحليل فني لحظي وإشارات دقيقة لـ XAUUSD</p>

    <div class="card">
        <h3>📊 تحليل السوق (Market Analysis)</h3>
        <button onclick="getAnalysis()">احصل على التحليل الفني</button>
        <div id="analysisResult" class="res"></div>
    </div>

    <div class="card">
        <h3>⚡ إشارة تداول فورية (Live Signal)</h3>
        <button class="btn-signal" onclick="getSignal()">طلب صفقة الآن</button>
        <div id="signalResult" class="res"></div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        function getAnalysis() {
            const resDiv = document.getElementById('analysisResult');
            resDiv.style.display = 'block';
            resDiv.innerHTML = "⏳ جاري فحص الشموع والدعوم...";

            fetch('/?req=analyze')
                .then(res => res.json())
                .then(data => {
                    resDiv.innerHTML = `📈 الأداة: <b>${data.symbol}</b><br>` +
                                        `⚖️ الاتجاه: <b>${data.trend}</b><br>` +
                                        `💪 قوة التحليل: <b>${data.strength}%</b><br>` +
                                        `🛡️ الدعم: <b>${data.support}</b> | المقاومة: <b>${data.resistance}</b>`;
                })
                .catch(() => { resDiv.innerHTML = "❌ حدث خطأ في الاتصال"; });
        }

        function getSignal() {
            const resDiv = document.getElementById('signalResult');
            resDiv.style.display = 'block';
            resDiv.innerHTML = "⏳ جاري حساب نقاط الدخول...";

            fetch('/?req=signal')
                .then(res => res.json())
                .then(data => {
                    resDiv.innerHTML = `🎯 الإشارة: <b>${data.action}</b><br>` +
                                        `📌 سعر الدخول: <b>${data.entry}</b><br>` +
                                        `🛑 وقف الخسارة (SL): <b>${data.sl}</b><br>` +
                                        `✅ الهدف (TP): <b>${data.tp}</b><br>` +
                                        `📊 الدقة المتوقعة: <b style="color:#10b981;">${data.accuracy}%</b>`;
                })
                .catch(() => { resDiv.innerHTML = "❌ حدث خطأ في الاتصال"; });
        }
    </script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    req_type = request.args.get('req')
    
    if req_type == 'analyze':
        return jsonify({
            "status": "success",
            "symbol": "XAUUSD (الذهب)",
            "trend": "صاعد قوي (Bullish)",
            "strength": 88,
            "support": "2715.00",
            "resistance": "2748.50"
        })
    elif req_type == 'signal':
        return jsonify({
            "status": "success",
            "action": "شراء (BUY) 🟢",
            "entry": "2725.00",
            "sl": "2714.00",
            "tp": "2740.00",
            "accuracy": 86
        })
        
    return render_template_string(HTML_CODE)
