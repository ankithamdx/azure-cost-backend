from flask import Flask, jsonify
app = Flask(__name__)
from azure.identity import DefaultAzureCredential
from azure.mgmt.consumption import ConsumptionManagementClient
from azure.identity import ChainedTokenCredential
from azure.mgmt.managementgroups import ManagementGroupsAPI
from azure.mgmt.billing import BillingManagementClient
from azure.mgmt.costmanagement import CostManagementClient
from datetime import datetime, timedelta
import pytz

# Replace with your Azure AD tenant ID, client ID, client secret, and subscription ID
tenant_id = '5f9d8183-ac49-417b-95c3-f12d0b218595'
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
subscription_id = 'a3093e96-c12e-477f-80f6-801680364694' # Pay-asYouGo
# subscription_id = 'fb76c5cb-a40f-49ff-b57f-d0cdd91ef688'
# subscription_id = '88afd314-47c4-424e-b91e-c3189eba9dcd'
start_date = '2023-08-01'  
end_date = '2023-08-31'
billing_period_name = '2023-08'
# 
# payg_cost_in_usd 141.0135197210487
# payg_cost_in_usd 141.01351972104857
@app.route('/billing_periods', methods=['GET'])
def get_billing_period_name():
    # Initialize Azure credentials using DefaultAzureCredential
    # credential = DefaultAzureCredential()
    # consumption_client = ConsumptionManagementClient(credential, subscription_id)

    # # Get the billing periods for the subscription
    # billing_periods = list(consumption_client.billing_periods.list())

    # # You can choose the desired billing period based on your criteria
    # # For example, you can select the latest billing period
    # if billing_periods:
    #     latest_billing_period = max(billing_periods, key=lambda bp: bp.name)
    #     billing_period_name = latest_billing_period.name
    #     return jsonify(billing_period_name)
    # else:
    #     return None

    # credential = ChainedTokenCredential(DefaultAzureCredential())

    # # Initialize the SubscriptionClient
    # subscription_client = SubscriptionClient(credential)

    # # Get the billing period name for the specified subscription
    # subscription = subscription_client.subscriptions.get(subscription_id)
    # billing_period_name = subscription.billing_details.last_billing_period.name

    # return billing_period_name
    credential = DefaultAzureCredential()
    client = BillingManagementClient(credential, subscription_id)
    billing_periods = client.billing_periods_operations.list()
    #   for billing_period in billing_periods:
    #   print(billing_period.billing_period_name)
    return billing_periods
    

@app.route('/test2', methods=['GET'])
def get_azure_billing_cost():
    credential = DefaultAzureCredential()
    consumption_client = ConsumptionManagementClient(credential, subscription_id)
    scope = f"/subscriptions/{subscription_id}"
    if billing_period_name:
        scope += f"/providers/Microsoft.Billing/billingPeriods/{billing_period_name}"

    # Calculate date range for the previous month
    utc_now = datetime.now(pytz.utc)
    first_day_of_current_month = utc_now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_last_month = first_day_of_last_month.replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)

    # Get the billing information
    billing_data = consumption_client.usage_details.list(
        scope=scope
    )
    # Calculate the total cost
    cost_data = []
    payg_cost_in_usd = 0
    for item in billing_data:
        # print('DDDDDDD', item)
        cost_data.append(vars(item))
        payg_cost_in_usd = payg_cost_in_usd + item.payg_cost_in_usd

    return {'total_cost_in_usd': payg_cost_in_usd, 'billing_details': cost_data}


@app.route('/management_groups', methods=['GET'])
def management_groups():
    credential = DefaultAzureCredential()
    management_groups_client = ManagementGroupsAPI(credential)

    # List all management groups
    management_groups = management_groups_client.management_groups.list()
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAA')
    # man_list = []
    # for mg in management_groups:
    #     # print(f"Management Group ID: {mg.id}")
    #     man_list.append(vars(mg))
    return management_groups


@app.route('/cost_management', methods=['GET'])
def cost_management():
    credential = DefaultAzureCredential()
    client = CostManagementClient(credential, subscription_id)
    scope = f"/subscriptions/{subscription_id}"
    costs = client.query.usage(parameters={}, scope=scope)
    return jsonify(costs)

if __name__ == "__main__":
    # total_cost = get_azure_billing_cost(tenant_id, client_id, client_secret, subscription_id)
    # print(f'Total billing cost for subscription {subscription_id}: ${total_cost:.2f}')
    app.run(debug=True)
