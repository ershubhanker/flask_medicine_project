from flask import Flask, request, render_template, jsonify
import jwt  # PyJWT is a library to work with JSON Web Tokens
import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from .env

# API_KEY = os.getenv('DRUGBANK_API_KEY')
# JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
API_KEY = 'df338cac4d1c76de487260acb441be5c'
JWT_SECRET_KEY = 'askdjbfirua438235bt642ndal'

# Ensure API_KEY and JWT_SECRET_KEY are available
if not API_KEY or not JWT_SECRET_KEY:
    raise ValueError("API_KEY and JWT_SECRET_KEY must be set in .env file")

HEADERS = {
    'authorization': API_KEY
}

app = Flask(__name__)




# Endpoint to get the API token - you must secure this!
@app.route('/get-token', methods=['POST'])
def get_token():
    try:

        # Here you'd implement your own authentication to ensure that the
        # request to this route is authorized.
        
        # This is the server-to-server request to DrugBank API to get the token
        response = requests.post(
            'https://api.drugbank.com/v1/tokens',
            headers={
                'Content-Type': 'application/json',
                'Authorization': API_KEY,
                'Cache-Control': 'no-cache'
            },
            json={'ttl': '15m'}  # Example of token that lasts for 15 minutes
        )
        response.raise_for_status()  # Raises a HTTPError if the HTTP request returned an unsuccessful status code

        # Send the token back to the front-end
        return jsonify(response.json()), 200
    except requests.exceptions.HTTPError as e:
        # You can log e.response or e.request for debugging or return a custom message
        return jsonify({'message': 'Failed to obtain API token'}), response.status_code
    except requests.exceptions.RequestException as e:
        # Handle any other exceptions that may occur
        return jsonify({'message': 'An error occurred when requesting the API token'}), 500
    


@app.route('/proxy/drug_names')
def proxy_drug_names():
    query = request.args.get('q')  # You get the query from the URL parameters
    url = "https://api.drugbank.com/v1/drug_names"
    params = {"q": query}
    response = requests.get(url, params=params, headers=HEADERS)
    
    return jsonify(response.json()) if response.ok else jsonify({"error": response.text}), response.status_code


@app.route('/submit', methods=['POST'])
def submit():
    # This endpoint would receive the form submission with the DBPCID
    medication_id = request.form.get('medication-1')
    # Here you would process the DBPCID, for example, check for drug interactions
    print(f'Received DBPCID: {medication_id}')
    # Perform any actions you need with the medication_id

    # Return a response or redirect the user to another page
    return 'Form submission received'






# Function to generate JWT tokens
def generate_jwt():
    payload = {
        'iss': 'drugbank_app', 
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)  # Token expiry
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token


# Initial page load, serves index.html with an initial jwt token
@app.route('/')
def index():
    jwt_token = generate_jwt()
    return render_template('index.html', jwt_token=jwt_token)


# Requested by page automatically when initial JWT token expires to ensure continous session on the client side
@app.route('/refresh', methods=['GET'])
def refresh_token():
    new_token = generate_jwt()
    return jsonify({'jwt_token': new_token}), 200


if __name__ == '__main__':
    app.run(debug=True)





# This was an example of the drug name API
# url = "https://api.drugbank.com/v1/us/drug_names"
# params = { "q": "Tylenol" }
# response = requests.get(url, params=params, headers=HEADERS)
# print(response.json())


# # This one was an example of product concepts
# url = "https://api.drugbank.com/v1/us/product_concepts?"
# # /DBPC0055443/strengths"
# params = { "q": "Tyl" }
# response = requests.get(url, params=params, headers=HEADERS)
# print(response.json())