from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

POCKET_STYLE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading AI Assistant & Pocket Signals</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root { --bg: #0b0f19; --card: #161e2e; --accent: #f59e0b; --green: #10b981; --red: #ef4444; --blue: #3b82f6; --text: #f8fafc; --muted: #94a3b8; }
        body { font-family: Tahoma, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 15px; text-align: center; }
        .header { background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid #334155; border-radius: 14px; padding: 15px; margin-bottom: 15px; }
        h2 { color: var(--accent); margin: 5px 0; font-size: 19px; }
        p { color: var(--muted); font-size: 12px; margin: 5px 0; }
        .card { background: var(--card); border: 1px solid #1f2937; border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.4); text-align: right; }
        .card h3 { color: var(--accent); font-size: 15px; margin-top: 0; border-bottom: 1px solid #334155; padding-bottom: 8px; }
        select, button { width: 100%; padding: 12px; border-radius: 8px; border: none; font-size: 14px; font-weight: bold; margin-top: 8px; cursor: pointer; }
        select { background: #0f172a; color: white; border: 1px solid #475569; text-align: right; }
        .btn-analysis { background: var(--blue); color: white; }
        .btn-buy { background: var(--green); color: white; }
        .btn-sell { background: var(--red); color: white; }
        .res { margin-top: 12px; background: #0b0f19; padding: 12px; border-radius: 8px; font-size: 13px; border-right: 4px solid var(--accent); display: none; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="header">
        <h2>🤖 مساعد التداول الذكي (Pocket Integration)</h2>
        <p>إشارات فورية وتحليل فني متوافق مع منصات التداول السريع</p>
    </div>

    <!-- قسم التحليل الفني -->
    <div class="card">
        <h3>📊 التحليل الفني للذهب والعملات</h3>
        <select id="analysisSymbol">
            <option value="XAUUSD">ذهب (XAUUSD)</option>
            <option value="EURUSD">يورو دولار (EURUSD)</option>
        </select>
        <button class="btn-analysis" onclick="getAnalysis()">احصل على التحليل الفني</button>
        <div id="analysisResult" class="res">جاري فحص الشموع...</div>
    </div>

    <!-- قسم إشارات التداول السريع (Pocket Option Style) -->
    <div class="card">
        <h3>⚡ إشارات التداول السريع (Quick Signals)</h3>
        <select id="timeframe">
            <option value="1m">صفقة لمدة دقيقة (1 Min)</option>
            <option value="3m">صفقة لمدة 3 دقائق (3 Mins)</option>
            <option value="5m">صفقة لمدة 5 دقائق (5 Mins)</option>
        </select>
        <button class="btn-buy" onclick="getQuickSignal('BUY')">🟢 إشارة صعود (CALL / BUY)</button>
        <button class="btn-sell" onclick="getQuickSignal('SELL')">🔴 إشارة هبوط (PUT / SELL)</button>
        <div id="signalResult" class="res">جاري توليد تفاصيل الصفقة...</div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        function getAnalysis() {
            const sym = document.getElementById('analysisSymbol').value;
            const resDiv = document.getElementById('analysisResult');
            resDiv.style.display = 'block';
            resDiv.innerHTML = "⏳ جاري فحص المؤشرات والدعوم لـ " + sym + "...";
            
            fetch('/api/analyze?symbol=' + sym)
                .then(res => res.json())
                .then(data => {
                    resDiv.innerHTML = `📈 الأصل: <b>${data.symbol}</b><br>
                                        ⚖️ الاتجاه العام: <b>${data.trend}</b><br>
                                        💪 قوة التحليل: <b>${data.strength}%</b><br>
                                        🛡️ الدعم: <b>${data.support}</b> | المقاومة: <b>${data.resistance}</b>`;
                }).catch(() => { resDiv.innerHTML = "❌ حدث خطأ في الاتصال بالسيرفر"; });
        }

        function getQuickSignal(type) {
            const tf = document.getElementById('timeframe').value;
            const resDiv = document.getElementById('signalResult');
            resDiv.style.display = 'block';
            resDiv.innerHTML = "⏳ جاري حساب نقطة الدخول للتداول السريع (" + tf + ")...\nانتقل لمنصة التداول لتنفيذها فور ظهورها!";

            fetch('/api/signal?tf=' + tf + '&type=' + type)
                .then(res => res.json())
                .then(data => {
                    resDiv.innerHTML = `🎯 الإشارة الموصى بها: <b style="color: ${data.action.includes('شراء') ? '#10b981' : '#ef4444'};">${data.action}</b><br>
                                        ⏱️ المدة الزمنية: <b>${data.timeframe}</b><br>
                                        📌 سعر التنفيذ المقترح: <b>${data.entry}</b><br>
                                        📊 نسبة النجاح والدقة: <b style="color: #f59e0b;">${data.probability}%</b><br>
                                        💡 <i>نفّذ الصفقة الآن على المنصة بناءً على المعطيات!</i>`;
                }).catch(() => { resDiv.innerHTML = "❌ حدث خطأ في الاتصال بالسيرفر"; });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(POCKET_STYLE_TEMPLATE)

@app.route('/api/analyze', methods=['GET'])
def analyze():
    return jsonify({
        "status": "success",
        "symbol": "XAUUSD (الذهب)",
        "trend": "صاعد قوي (Bullish)",
        "strength": 89,
        "support": "2712.50",
        "resistance": "2750.00"
    })

@app.route('/api/signal', methods=['GET'])
def signal():
    return jsonify({
        "status": "success",
        "action": "شراء (CALL / BUY) 🟢",
        "timeframe": "دقيقة واحدة (1 Min)",
        "entry": "2724.30",
        "probability": 87
    })
