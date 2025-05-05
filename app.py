from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route("/korea-bond-yield")
def korea_bond_yield():
    url = "https://www.kofiabond.or.kr/asp/servlet/BondISub?cmd=forwardStats&bnd_clss_cd=005"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", {"class": "table_style01"})
    rows = table.find_all("tr")

    data = []

    for row in rows[2:]:
        cols = row.find_all("td")
        if len(cols) >= 11:
            date_str = cols[0].text.strip().replace(".", "-")
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                y10 = float(cols[9].text.strip()) if cols[9].text.strip() else None
                y30 = float(cols[10].text.strip()) if cols[10].text.strip() else None
                if y10 and y30:
                    data.append({"date": date.isoformat(), "10Y": y10, "30Y": y30})
            except:
                continue

    return jsonify(data[:254])

if __name__ == "__main__":
    app.run(debug=True)
