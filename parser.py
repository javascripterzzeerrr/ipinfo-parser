from dotenv import load_dotenv
import os
import ipinfo
import re
import time
import json

# Load environment variables from the .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("API_KEY")

handler = ipinfo.getHandler(api_key)

exitNodeTor = {}
exitNodeTor['list_nodes'] = []

regexIp = r'([0-9]{1,3}[\.]){3}[0-9]{1,3}'


async def do_req(ip_address):
    return await handler.getDetails(ip_address)

# unit added in the exitNodeTor
count = 0
node = {}
node_name = ""


def switch_parameter_node(line):
    global node_name, count, node

    lines_list = line.split(" ")

    if lines_list[0] == "ExitNode":
        node_name = lines_list[1].replace("\n", "")
        node[node_name] = {}
        node[node_name]['ExitNode'] = node_name
        count += 1
    elif lines_list[0] == "Published":
        node[node_name]['Published'] = lines_list[1] + lines_list[2].replace("\n", "")
        count += 1
    elif lines_list[0] == "LastStatus":
        node[node_name]['LastStatus'] = lines_list[1] + lines_list[2].replace("\n", "")
        count += 1
    elif lines_list[0] == "ExitAddress":
        match = re.search(regexIp, line)

        ip_addr = match[0] if match else 'Not found'

        city = 'Not found'
        location = 'Not found'
        country = 'Not found'

        if ip_addr != 'Not found':
            # details = do_req(ip_addr)
            details = handler.getDetails(ip_addr)
            city = details.city
            location = details.loc
            country = details.country

        node[node_name]['ExitAddress'] = ip_addr
        node[node_name]['City'] = city
        node[node_name]['Location'] = location
        node[node_name]['Country'] = country
        count += 1


        exitNodeTor['list_nodes'].append(node[node_name])

        if count == 4:
            count = 0
            node = {}
            node_name = ""


with open("exit-addresses") as f:
    for line in f:
        switch_parameter_node(line)
    else:
        # Check correct storage data
        for key in exitNodeTor['list_nodes']:
            print("KEY => ", key)