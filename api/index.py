from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

ALAAN_APP_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Trading Assistant</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root {
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --accent-color: #f59e0b;
            --green: #10b981;
            --red: #ef4444;
            --text-color: #f0f6fc;
            --muted-color: #8b949e;
            --border-color: #30363d;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 10px 10px 70px 10px;
            direction: rtl;
        }

        .tab-content { display: none; }
        .tab-content.active { display: block; }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            text-align: right;
        }

        h2, h3 { color: var(--accent-color); margin-top: 0; }
        label { font-size: 13px; color: var(--muted-color); display: block; margin-bottom: 5px; }
        
        select, input {
            width: 100%;
            padding: 10px;
            background: #0d1117;
            border: 1px solid var(--border-color);
            color: #fff;
            border-radius: 8px;
            margin-bottom: 10px;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
            margin-top: 5px;
            background: #238636;
            color: #fff;
        }

        .btn-blue { background: #1f6feb; }
        .btn-red { background: var(--red); }

        .res-box {
            margin-top: 10px;
            padding: 12px;
            background: #0d1117;
            border-radius: 8px;
            border-right: 3px solid var(--accent-color);
            font-size: 13px;
            line-height: 1.6;
        }

        /* Bottom Nav bar like Ala'a Ayman's Bot */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #161b22;
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-around;
            padding: 8px 0;
        }

        .nav-item {
            color: var(--muted-color);
            text-decoration: none;
            font-size: 11px;
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
        }

        .nav-item.active { color: var(--accent-color); font-weight: bold; }
        .nav-icon { font-size: 18px; margin-bottom: 2px; }
    </style>
</head>
<body>

    <!-- Tab 1: Analysis -->
    <div id="tab-analysis" class="tab-content active">
        <div class="card">
            <h2>📊 التحليل الفني (Market Analysis)</h2>
            <label>اختر العملة أو المعدن:</label>
            <select id="analysisSymbol">
                <option value="XAUUSD">الذهب (XAUUSD)</option>
                <option value="EURUSD">يورو / دولار (EURUSD)</option>
                <option value="BTCUSD">بيتكوين (BTCUSD)</option>
            </select>
            <button class="btn-blue" onclick="getAnalysis()">طلب التحليل الفني</button>
            <div id="resAnalysis" class="res-box" style="display:none;"></div>
        </div>
    </div>

    <!-- Tab 2: Signals -->
    <div id="tab-signals" class="tab-content">
        <div class="card">
            <h2>⚡ إشارات التداول (Signals)</h2>
            <label>سوق التداول:</label>
            <select id="signalMarket">
                <option value="FOREX">فوركس (Forex)</option>
                <option value="CRYPTO">كريبتو (Crypto)</option>
                <option value="QUICK">تداول سريع (Quick Trading)</option>
            </select>
            <button onclick="getSignal()">جلب الصفقة القادمة</button>
            <div id="resSignal" class="res-box" style="display:none;"></div>
        </div>
    </div>

    <!-- Tab 3: Quick Trading -->
    <div id="tab-quick" class="tab-content">
        <div class="card">
            <h2>🚀 التداول السريع (Quick Trading)</h2>
            <p style="font-size: 12px; color: var(--muted-color);">مخصص لمطابقة منصات Pocket Option والخيارات الثنائية.</p>
            <label>مدة الصفقة:</label>
            <select id="quickTime">
                <option value="1 Min">دقيقة واحدة (1M)</option>
                <option value="3 Min">3 دقائق (3M)</option>
                <option value="5 Min">5 دقائق (5M)</option>
            </select>
            <button class="btn-blue" onclick="getQuickSignal('BUY')">🟢 صفقة صعود (CALL)</button>
            <button class="btn-red" onclick="getQuickSignal('SELL')">🔴 صفقة هبوط (PUT)</button>
            <div id="resQuick" class="res-box" style="display:none;"></div>
        </div>
    </div>

    <!-- Tab 4: History -->
    <div id="tab-history" class="tab-content">
        <div class="card">
            <h2>📜 سجل الصفقات (History)</h2>
            <div class="res-box">
                ✔️ <b>XAUUSD (BUY):</b> +24 pips (ربح) <br>
                ✔️ <b>EURUSD (SELL):</b> +12 pips (ربح) <br>
                ❌ <b>BTCUSD (BUY):</b> -8 pips (خسارة) <br>
                <hr style="border-color: var(--border-color);">
                <b>معدل النجاح الإجمالي:</b> 82%
            </div>
        </div>
    </div>

    <!-- Tab 5: Profile -->
    <div id="tab-profile" class="tab-content">
        <div class="card">
            <h2>👤 الملف الشخصي (Profile)</h2>
            <p><b>حالة الحساب:</b> <span style="color:var(--green);">موثق (Verified)</span></p>
            <p><b>معرف المستخدم:</b> #7829411</p>
            <p><b>المنصة المربوطة:</b> Pocket Option / MetaTrader 5</p>
        </div>
    </div>

    <!-- Bottom Navigation Bar -->
    <div class="bottom-nav">
        <div class="nav-item active" onclick="switchTab('analysis', this)">
            <span class="nav-icon">📊</span>التحليل
        </div>
        <div class="nav-item" onclick="switchTab('signals', this)">
            <span class="nav-icon">⚡</span>الإشارات
        </div>
        <div class="nav-item" onclick="switchTab('quick', this)">
            <span class="nav-icon">🚀</span>تداول سريع
        </div>
        <div class="nav-item" onclick="switchTab('history', this)">
            <span class="nav-icon">📜</span>السجل
        </div>
        <div class="nav-item" onclick="switchTab('profile', this)">
            <span class="nav-icon">👤</span>حسابي
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        function switchTab(tabId, el) {
            document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(ni => ni.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            el.classList.add('active');
        }

        function getAnalysis() {
            const sym = document.getElementById('analysisSymbol').value;
            const res = document.getElementById('resAnalysis');
            res.style.display = 'block';
            res.innerHTML = "⏳ جاري فحص المؤشرات لـ " + sym + "...";

            fetch('/api/index?req=analysis&sym=' + sym)
                .then(r => r.json())
                .then(d => {
                    res.innerHTML = `📈 الاتجاه: <b>${d.trend}</b><br>💪 القوة: <b>${d.strength}%</b><br>🛡️ الدعم: <b>${d.support}</b><br>⚔️ المقاومة: <b>${d.resistance}</b>`;
                }).catch(() => { res.innerHTML = "❌ خطأ في الاتصال"; });
        }

        function getSignal() {
            const mkt = document.getElementById('signalMarket').value;
            const res = document.getElementById('resSignal');
            res.style.display = 'block';
            res.innerHTML = "⏳ جاري توليد إشارة لـ " + mkt + "...";

            fetch('/api/index?req=signal&mkt=' + mkt)
                .then(r => r.json())
                .then(d => {
                    res.innerHTML = `🎯 الإشارة: <b>${d.action}</b><br>📌 سعر الدخول: <b>${d.entry}</b><br>🛑 SL: <b>${d.sl}</b> | ✅ TP: <b>${d.tp}</b><br>📊 قوة الصفقة: <b>${d.accuracy}%</b>`;
                }).catch(() => { res.innerHTML = "❌ خطأ في الاتصال"; });
        }

        function getQuickSignal(type) {
            const time = document.getElementById('quickTime').value;
            const res = document.getElementById('resQuick');
            res.style.display = 'block';
            res.innerHTML = "⏳ جاري حساب صفقة " + time + "...";

            fetch('/api/index?req=quick&type=' + type + '&time=' + time)
                .then(r => r.json())
                .then(d => {
                    res.innerHTML = `🎯 نوع الصفقة: <b>${d.action}</b><br>⏱️ المدة: <b>${d.time}</b><br>📊 نسبة الدقة: <b style="color:var(--green);">${d.accuracy}%</b><br>💡 <i>ادخل الصفقة فوراً على المنصة!</i>`;
                }).catch(() => { res.innerHTML = "❌ خطأ في الاتصال"; });
        }
    </script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    req = request.args.get('req')
    
    if req == 'analysis':
        return jsonify({"trend": "صاعد (Bullish)", "strength": 88, "support": "2715.00", "resistance": "2748.50"})
    elif req == 'signal':
        return jsonify({"action": "BUY 🟢", "entry": "2725.10", "sl": "2714.00", "tp": "2742.00", "accuracy": 85})
    elif req == 'quick':
        action_type = request.args.get('type')
        time_val = request.args.get('time')
        return jsonify({"action": f"{action_type} 🟢" if action_type == 'BUY' else f"{action_type} 🔴", "time": time_val, "accuracy": 89})

    return render_template_string(ALAAN_APP_HTML)
