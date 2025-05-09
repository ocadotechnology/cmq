import boto3

# Get available AWS service names
session = boto3.Session()
available_services = session.get_available_services()

resource_list = []

for service_name in available_services:
    try:
        client = session.client(service_name)
        # List available functions for the service
        functions = dir(client)

        # Identify functions that list resources (typically 'list_' or 'describe_' prefixes)
        list_functions = [func for func in functions if func.startswith(("list_", "describe_")) and func.endswith("s") and "tag" not in func]

        for func in list_functions:
            # Convert the function name to snake_case resource short name
            short_name = func.replace("list_", "").replace("describe_", "").lower()
            resource_list.append((service_name, short_name, func))

    except Exception as e:
        print(f"Could not process {service_name}: {e}")

# Print results
print(f"{'Boto3 Service':<20} {'Short Name':<20} {'Listing Function'}")
print("-" * 60)

for service, short_name, function in resource_list:
    print(f"{service:<20}, {short_name:<20}, {function}")
