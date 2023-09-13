from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
from azure.identity import DefaultAzureCredential
from azure.mgmt.consumption import ConsumptionManagementClient
from datetime import datetime
import calendar

subscription_id = 'a3093e96-c12e-477f-80f6-801680364694' # Pay-asYouGo
# subscription_id = 'fb76c5cb-a40f-49ff-b57f-d0cdd91ef688'
# subscription_id = '88afd314-47c4-424e-b91e-c3189eba9dcd'
billing_period_name = '2023-08'


@app.route('/billing_graph', methods=['GET'])
def get_azure_billing_cost():
     current_datetime = datetime.now()
     first_day_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

     # Calculate the total number of days in the current month
     _, last_day_of_month = calendar.monthrange(current_datetime.year, current_datetime.month)

     # Calculate the total number of minutes in a day
     minutes_per_hour = 60
     minutes_per_day = minutes_per_hour * 24

     # Calculate the total number of minutes in the current month
     total_minutes_in_month = minutes_per_day * last_day_of_month

     # Calculate the minutes elapsed in the current month
     elapsed_minutes = (current_datetime - first_day_of_month).total_seconds() / 60

     print(f"Minutes elapsed in the current month: {elapsed_minutes}")
     print(f"Total minutes in the current month: {total_minutes_in_month}")


     credential = DefaultAzureCredential()
     consumption_client = ConsumptionManagementClient(credential, subscription_id)
     scope = f"/subscriptions/{subscription_id}"

     # Get the billing information
     billing_data = consumption_client.usage_details.list(
          scope=scope
     )
     # Calculate the total cost
     cost_data = []
     graph_data = []
     payg_cost_in_usd = 0
     for item in billing_data:
          cost_data.append(vars(item))
          payg_cost_in_usd = payg_cost_in_usd + item.payg_cost_in_usd
          graph_data.append({"name": item.consumed_service, "price": item.payg_cost_in_usd,
                              "desc": item.product, "resource_group": item.resource_group})

     total_projected_amount = (payg_cost_in_usd/elapsed_minutes) * total_minutes_in_month
     graph_data = sorted(graph_data, key=lambda x: x['price'], reverse=True)

     return {'total_cost_in_usd': payg_cost_in_usd, 'billing_details': graph_data, 'total_projected_amount': total_projected_amount}


if __name__ == "__main__":
    app.run(debug=True)
