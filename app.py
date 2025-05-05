from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/krx-korea-bond")
def get_krx_bond_yields():
    try:
        url = "https://finance.naver.com/marketindex/bondDetail.naver?marketindexCd=INDEX_KRBGOVT10Y"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.find("table", {"class": "tbl_tb"})

        if table is None:
            return jsonify({"error": "No table found. KRX may have changed layout."}), 500

        data = []
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols if ele.text.strip() != ""]
            if cols:
                data.append(cols)

        return jsonify({"data": data})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
