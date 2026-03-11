from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def evaluate_privacy(cookies):
    analyzed = []
    score = 10.0
    stats = {"safe": 0, "tracking": 0, "ads": 0, "high_risk": 0}

    tracking_keywords = ['_ga', 'track', 'pixel', 'sim']
    ad_keywords = ['ads', 'marketing', 'pixel']

    for cookie in cookies:
        c_risk = "Safe"
        c_name = cookie.name.lower()
        
        # Security Flags (Requests specific parsing)
        is_secure = cookie.secure
        is_httponly = 'HttpOnly' in cookie._rest or cookie.has_nonstandard_attr('HttpOnly')
        
        # Classification
        if any(x in c_name for x in ad_keywords):
            c_risk = "Advertising"
            stats["ads"] += 1
            score -= 1.5
        elif any(x in c_name for x in tracking_keywords):
            c_risk = "Tracking"
            stats["tracking"] += 1
            score -= 1.0
        
        # Flag Penalties
        if not is_secure:
            c_risk = "High Risk"
            stats["high_risk"] += 1
            score -= 1.0
        if not is_httponly:
            score -= 0.5
            
        if c_risk == "Safe": stats["safe"] += 1

        analyzed.append({
            "name": cookie.name,
            "secure": is_secure,
            "httponly": is_httponly,
            "category": c_risk
        })

    final_score = max(0.5, min(10.0, round(score, 1)))
    rec = "Accept essential cookies only." if final_score < 7 else "Site appears secure."
    if stats["high_risk"] > 0:
        rec = "Reject all cookies. Critical security flags (Secure/HttpOnly) are missing."

    return analyzed, final_score, stats, rec

@app.route('/')
def index():
    return render_template('analyzer.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    target_url = request.form.get('url')
    if not target_url.startswith('http'):
        target_url = 'http://' + target_url

    try:
        # Simulate a real browser request
        headers = {'User-Agent': 'Mozilla/5.0 (SecurityAuditor/1.0)'}
        response = requests.get(target_url, timeout=5, headers=headers)
        
        cookies = response.cookies
        if not cookies:
            return "<h3>No cookies detected at " + target_url + ". Ensure the Generator is running.</h3>"

        analyzed_list, score, stats, rec = evaluate_privacy(cookies)
        return render_template('result.html', url=target_url, cookies=analyzed_list, score=score, stats=stats, rec=rec)
        
    except Exception as e:
        return f"<h3>Connection Error</h3><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)