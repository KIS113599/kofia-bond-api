from flask import Flask, jsonify
import requests
import csv
import io
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/korea-bond-yield")
def korea_bond_yield():
    url = "https://www.kofiabond.or.kr/statistics/download?gubun=yield&bnd_clss_cd=005"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.kofiabond.or.kr/"
    }

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'euc-kr'
        csv_text = response.text

        f = io.StringIO(csv_text)
        reader = csv.reader(f)
        all_rows = list(reader)

        # ✅ 처음 5줄만 반환하여 구조 확인
        return jsonify(all_rows[:5])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
