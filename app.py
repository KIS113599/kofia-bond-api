from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# KRX 비공식 수익률 API
KRX_URL = "https://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0"
}

# 최근 2년간 날짜 리스트 생성 (영업일만 필터링은 생략)
def get_recent_dates(days=500):
    today = datetime.today()
    return [(today - timedelta(days=i)).strftime("%Y%m%d") for i in range(days)]

# 날짜별 수익률 조회
def fetch_bond_yield_by_date(date_str):
    payload = {
        "bld": "dbms/MDC/STAT/standard/MDCSTAT03901",
        "mktId": "ALL",
        "trdDd": date_str,
        "bndTpCd": "101",
        "askType": "1"
    }
    try:
        res = requests.post(KRX_URL, headers=HEADERS, data=payload, timeout=10)
        items = res.json().get("OutBlock_1", [])
        row = {"date": datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")}
        for item in items:
            name = item.get("isuNm", "")
            if "10년" in name:
                row["10Y"] = float(item.get("intR"))
            if "30년" in name:
                row["30Y"] = float(item.get("intR"))
        return row if "10Y" in row and "30Y" in row else None
    except Exception:
        return None

@app.route("/krx-korea-bond")
def get_korea_bond_yields():
    results = []
    count = 0
    for date in get_recent_dates():
        row = fetch_bond_yield_by_date(date)
        if row:
            results.append(row)
            count += 1
        if count >= 254:
            break
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
