from flask import Flask, request, render_template, jsonify
import requests
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index_new.html")

@app.route("/search/<string:box>")
def process(box):
    query = request.args.get('query')

    if box == 'names':
        print("input data= ",query)
        url = f"https://api.drugbank.com/v1/drug_names?q={query}"

        payload = {}
        headers = {
        'authorization': 'df338cac4d1c76de487260acb441be5c'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        val = json.loads(response.text)
        # print(len(val['products']))
        suggestion_list = []
        for i in range(len(val['products'])):
            for j in range(len(val['products'][i]['hits'])):
                print(val['products'][i]['hits'][j]['value'])

                # do some stuff to open your names text file
                # do some other stuff to filter
                # put suggestions in this format...
                {'value': val['products'][i]['hits'][j]['value'],'data': val['products'][i]['hits'][j]['value']}
                suggestion_list.append({'value': val['products'][i]['hits'][j]['value'],'data': val['products'][i]['hits'][j]['value']})
        # suggestions = [{'value': 'joe','data': 'joe'},{'value': 'aman','data': 'aman'}, {'value': 'jim','data': 'jim'}]
        suggestions = suggestion_list
    # if box == 'songs':
    #     # do some stuff to open your songs text file
    #     # do some other stuff to filter
    #     # put suggestions in this format...
    #     suggestions = [{'value': 'song1','data': '123'}, {'value': 'song2','data': '234'}]
    return jsonify({"suggestions":suggestions})

if __name__ == "__main__":
    app.run(debug=True)