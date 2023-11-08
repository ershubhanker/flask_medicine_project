from flask import Flask, request, render_template, jsonify
import requests
import json
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from .env

API_KEY = os.getenv('DRUGBANK_API_KEY')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index_new.html")


@lru_cache(maxsize=32)
def get_drug_suggestions(query):
    url = f"https://api.drugbank.com/v1/product_concepts?q={query}&min_level=4&max_level=4"
    headers = {
        'authorization': API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        suggestion_list = []
        for item in data:
            suggestion_list.append({
                'value': item['name'],  # the display value now comes from 'name'
                'data': {
                    'value': item['name'],  # the display value now comes from 'name'
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


@app.route("/interactions")
def get_interactions():
    pcids = request.args.get('pcids')
    if pcids:
        try:
            response = requests.get(f"https://api.drugbank.com/v1/ddi?product_concept_id={pcids},DBPC0097331", headers={'authorization': API_KEY})
            if response.status_code == 200:
                return jsonify(response.json())  # Send the JSON response back to the client
            else:
                return jsonify({"error": "API request failed"}), response.status_code
        except requests.RequestException as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No PCIDs provided"}), 400



if __name__ == "__main__":
    app.run(debug=True)