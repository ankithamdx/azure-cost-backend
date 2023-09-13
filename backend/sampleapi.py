import requests

credential = DefaultAzureCredential()
token = credential.get_token("https://management.azure.com/.default")

headers = {"Authorization": "Bearer " + token["access_token"]}

from flask import Flask, jsonify
# import azure.mgmt.costmanagement.models
# from azure.identity import DefaultAzureCredential

app = Flask(__name__)

@app.route('/sample_costs', methods=['GET'])
def sample():

    response = requests.post(
        "https://management.azure.com/...", 
        headers=headers
    )

    print(response.json())
    return str(costs)



if __name__ == '__main__':
    app.run(debug=True)