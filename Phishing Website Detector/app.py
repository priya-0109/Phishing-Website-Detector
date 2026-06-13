import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def check_url(url):
    score = 0

    suspicious_words = [
        "login",
        "verify",
        "secure",
        "account",
        "update",
        "bank",
        "paypal",
        "signin"
    ]

    if len(url) > 50:
        score += 10

    if "@" in url:
        score += 20

    if "-" in url:
        score += 15

    if url.count(".") > 3:
        score += 15

    if not url.startswith("https://"):
        score += 20

    for word in suspicious_words:
        if word in url.lower():
            score += 10

    risk_score = min(score, 100)

    if risk_score >= 50:
        result = "PHISHING WEBSITE 🚨"
    else:
        result = "SAFE WEBSITE ✅"

    return result, risk_score


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    # Total scans
    cursor.execute("SELECT COUNT(*) FROM scan_history")
    total_scans = cursor.fetchone()[0]

    # Safe websites
    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE result='SAFE WEBSITE ✅'")
    safe_count = cursor.fetchone()[0]

    # Phishing websites
    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE result='PHISHING WEBSITE 🚨'")
    phishing_count = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        total_scans=total_scans,
        safe_count=safe_count,
        phishing_count=phishing_count
    )


@app.route('/predict', methods=['POST'])
def predict():

    # URL lena
    url = request.form['url']

    # URL analyze karna
    result, risk_score = check_url(url)

    # Database me save karna
    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO scan_history(url,result,risk_score) VALUES (?,?,?)",
        (url, result, risk_score)
    )

    conn.commit()
    conn.close()

    # Result page show karna
    return render_template(
        'result.html',
        url=url,
        result=result,
        risk_score=risk_score
    )


@app.route('/history')
def history():

    conn = sqlite3.connect('phishing.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scan_history ORDER BY id DESC")

    data = cursor.fetchall()

    conn.close()

    return render_template('history.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)