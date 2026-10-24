from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading AI Assistant</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { font-family: Tahoma, sans-serif; background: #0b0f19; color: #fff; margin: 0; padding: 15px; text-align: center; }
        .card { background: #161e2e; border-radius: 12px; padding: 15px; margin-bottom: 15px; border: 1px solid #1f2937; text-align: right; }
        h2 { color: #f59e0b; text-align: center; }
        button { width: 100%; background: #3b82f6; color: white; border: none; padding: 12px; border-radius: 8px; font-size: 15px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        .btn-signal { background: #10b981; }
        .res { margin-top: 12px; background: #0b0f19; padding: 12px; border-radius: 8px; font-size: 13px; border-right: 4px solid #f59e0b; display: none; line-height: 1.6; }
    </style>
</head>
<body>
    <h2>🤖 بوت التحليل الذكي للذهب والعملات</h2>
    <p style="color: #94a3b8; font-size: 12px; text-align: center;">تحليل فني لحظي وإشارات دقيقة لـ XAUUSD</p>

    <div class="card">
        <h3>📊 تحليل السوق (Market Analysis)</h3>
        <button onclick="loadData('analyze')">احصل على التحليل الفني</button>
        <div id="resAnalyze" class="res"></div>
    </div>

    <div class="card">
        <h3>⚡ إشارة تداول فورية (Live Signal)</h3>
        <button class="btn-signal" onclick="loadData('signal')">طلب صفقة الآن</button>
        <div id="resSignal" class="res"></div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        function loadData(type) {
            const div = document.getElementById(type === 'analyze' ? 'resAnalyze' : 'resSignal');
            div.style.display = 'block';
            div.innerHTML = "⏳ جاري الاتصال بالسيرفر وجلب البيانات...";

            fetch('/api/index?action=' + type)
                .then(res => res.json())
                .then(data => {
                    if(type === 'analyze') {
                        div.innerHTML = `📈 الأداة: <b>${data.symbol}</b><br>⚖️ الاتجاه: <b>${data.trend}</b><br>💪 القوة: <b>${data.strength}%</b><br>🛡️ الدعم: <b>${data.support}</b> | المقاومة: <b>${data.resistance}</b>`;
                    } else {
                        div.innerHTML = `🎯 الإشارة: <b>${data.action}</b><br>📌 الدخول: <b>${data.entry}</b><br>🛑 وقف الخسارة: <b>${data.sl}</b><br>✅ الهدف: <b>${data.tp}</b>`;
                    }
                })
                .catch(() => { div.innerHTML = "❌ خطأ في الاتصال، جرب مرة أخرى"; });
        }
    </script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    action = request.args.get('action')
    
    if action == 'analyze':
        return jsonify({
            "symbol": "XAUUSD (الذهب)",
            "trend": "صاعد قوي (Bullish)",
            "strength": 89,
            "support": "2715.00",
            "resistance": "2750.00"
        })
    elif action == 'signal':
        return jsonify({
            "action": "شراء (BUY) 🟢",
            "entry": "2725.00",
            "sl": "2714.00",
            "tp": "2740.00"
        })
        
    return render_template_string(HTML_PAGE)
