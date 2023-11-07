import routeros_api
import ipaddress  # Make sure to import ipaddress if it's not already imported

# Define the device information
router_ip = "12.12.12.1"
router_username = "Eclipse"
router_password = "3cL1p32!"

try:
    # Create an API connection
    api = routeros_api.RouterOsApiPool(
        router_ip, username=router_username, password=router_password
    )

    # Open the API connection
    connection = api.get_api()

    # Retrieve the list of queues
    list_queues = connection.get_resource("/queue/simple")
    list_queues.add(
        queue="UnlimUp/UnlimDown",
        target="target_ip_here",  # Replace with the actual target IP address
        comment="daily",
    )

    for queue in list_queues.get():
        print(
            f"Name: {queue['name']}, Target: {queue['target']}, Rate: {queue['rate']}"
        )

    # Disconnect from the router
    api.disconnect()
    print("Disconnected from MikroTik Router")
except Exception as e:
    print(f"Error: {str(e)}")
