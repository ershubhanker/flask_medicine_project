from flask import Flask, request, render_template, jsonify
import requests
import json
from functools import lru_cache

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index_new.html")


@lru_cache(maxsize=32)
def get_drug_suggestions(query):
    url = f"https://api.drugbank.com/v1/product_concepts?q={query}"
    headers = {
        'authorization': 'df338cac4d1c76de487260acb441be5c'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        suggestion_list = []
        for item in data:
            for hit in item.get('hits', []):
                # Remove HTML tags for highlighting
                clean_value = hit['value'].replace('<em>', '').replace('</em>', '')
                suggestion_list.append({
                'value': clean_value,  # the display value
                'data': {
                    'value': clean_value,
                    'drugbank_pcid': item['drugbank_pcid']  # the PCID from the item
                }
            })
        return suggestion_list
    else:
        response.raise_for_status()


@app.route("/search/<string:box>")
def process(box):
    query = request.args.get('query')
    if box == 'names' and len(query) >= 3:
        try:
            suggestions = get_drug_suggestions(query)
        except requests.HTTPError as e:
            # Handle HTTP errors here
            return jsonify({"error": str(e)}), e.response.status_code
        return jsonify({"suggestions": suggestions})
    else:
        # Handle cases where query is too short or box is not 'names'
        return jsonify({"error": "Invalid request"})



@app.route("/drug_routes/<string:pcid>")
def drug_routes(pcid):
    url = f"https://api.drugbank.com/v1/product_concepts/{pcid}/routes"
    headers = {
        'authorization': 'df338cac4d1c76de487260acb441be5c'  # Make sure to keep your API keys secret in a production environment
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        routes_list = [{'label': f"{item.get('name')}", 'value': item.get('route')} for item in data]
        return jsonify(routes_list)
    else:
        return jsonify({"error": "Failed to fetch drug routes"}), response.status_code




if __name__ == "__main__":
    app.run(debug=True)