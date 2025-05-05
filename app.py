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
        response.encoding = 'euc-kr'  # 한글 인코딩
        csv_text = response.text

        f = io.StringIO(csv_text)
        reader = csv.reader(f)
        data = []

        for row in reader:
            try:
                date = datetime.strptime(row[0].strip(), "%Y.%m.%d").date()
                y10 = float(row[9].replace(",", "").strip()) if row[9].strip() else None
                y30 = float(row[10].replace(",", "").strip()) if row[10].strip() else None
                if y10 and y30:
                    data.append({"date": date.isoformat(), "10Y": y10, "30Y": y30})
            except:
                continue

        return jsonify(data[:254])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
