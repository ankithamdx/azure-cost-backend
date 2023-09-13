from flask import Flask, jsonify
import azure.mgmt.costmanagement.models
from azure.identity import DefaultAzureCredential

app = Flask(__name__)

@app.route('/sample_costs', methods=['GET'])
def sample():

    # Get the subscription ID
    subscription_id = "e89dbf0b-3a6f-4ab6-b29a-9ee784f528f9"

    # Get the start and end dates
    start_date = "2023-08-01"
    end_date = "2023-08-31"

    # Create a cost management client
    client = azure.mgmt.costmanagement.CostManagementClient(
        DefaultAzureCredential()
    )
    l = dir(client)
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', l)
    

    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', dir(client.query))
    # Get the costs
    costs = client.query("SELECT * FROM Cost WHERE time >= '2020-08-01' AND time <= '2020-08-31'")
    print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
    # Print the costs
    for cost in costs:
        print(cost)
    
    return str(costs)



if __name__ == '__main__':
    app.run(debug=True)