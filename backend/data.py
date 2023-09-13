from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from flask import Flask, jsonify

app = Flask(__name__)
subscription_id = "e89dbf0b-3a6f-4ab6-b29a-9ee784f528f9"
credential = DefaultAzureCredential()
client = CostManagementClient(credential, subscription_id)

@app.route('/azure_costs', methods=['GET'])
def get_costs():

    query_response = client.query.execute(
        type="Usage",
        time_frame="MonthToDate",
        dataset={"aggregation": {"totalCost": {"name": "PreTaxCost", "function": "Sum"}}}  
    )
    return jsonify(query_response.results)
    print('AAAAAAAAAAAAAAAAA')
    # print(str(client))
    # print('BBBBBBBBBBBBBBBBBBBBBBBBBBBb')

    result = client.query_client.query(
        # "SELECT * FROM Cost WHERE",
        # time_period=TimePeriod(
        #     from_property='08/01/2023', to_property='08/31/2023'
        # )
        "SELECT * FROM Cost WHERE time >= '2020-08-01' AND time <= '2020-08-31'"
    ).result()
    print('CCCCCCCCCCCCCCCCCCCCCCCCCCC')
    print(result.cost)
    return jsonify(str(result.cost))


if __name__ == '__main__':
    app.run(debug=True)
