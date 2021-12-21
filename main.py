import time
from cf_oauth_token import aciat001_oauth_token

import requests
import json
import re
import datetime

base_url = "https://api.cf.sap.hana.ondemand.com/v3/apps"
space_guid = "2c92d3e7-a833-4fbf-89e2-917c07cea220"
token = f"{aciat001_oauth_token()}"

url = f"{base_url}?page=1&per_page=1000&space_guids={space_guid}"

payload = {}
headers = {
    'Authorization': token
}

response = requests.request("GET", url, headers=headers, data=payload)

# TODO convert the string received from above to a dictionary

response_dict = json.loads(response.text)
# with open("all_apps.json", "w") as datafile:
#     json.dump(response_dict, datafile)

resources = response_dict["resources"]

len_of_resources = len(response_dict["resources"])

# TODO  list all the apps

string_of_apps = []
for app in range(0, len_of_resources):
    string_of_apps.append(resources[app]["name"])
    # print(string_of_apps)

# TODO create a dictionary with {appname: guid} by parsing

# dict_app_guid = {}
#
# for app in range(0, len_of_resources):
#     temp_dict_app_guid = {
#         name: resources[app]["name"],
#         guid: resources[app]["guid"]
#
#     }
#     dict_app_guid.update(temp_dict_app_guid)
# print(dict_app_guid)

# print(string_of_apps)

# TODO out of the apps collected list the apps starting with itw- and sore it in a list - by matching substring -
#  https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method

worker_list = []
for item in string_of_apps:
    if "itw-" in item:
        worker_list.append(item)

print(worker_list)
no_of_workers = len(worker_list)
print(f"Total no. of workers found here is -  {no_of_workers}")

# TODO get guid of all the workers in the list - "worker_list"
guid_list = []
for worker in worker_list:
    url = f"{base_url}?page=1&per_page=1000&space_guids={space_guid}&names={worker}"

    payload = {}
    headers = {
        'Authorization': token
    }

    response_for_guid = requests.request("GET", url, headers=headers, data=payload)
    response_guid_dict = json.loads(response_for_guid.text)
    worker_guid = response_guid_dict["resources"][0]["guid"]
    worker_name = response_guid_dict["resources"][0]["name"]
    guid_list.append(worker_guid)
    # TODO Restart all the collected workers
    url = f"{base_url}/{worker_guid}/actions/restart"

    payload = {}
    headers = {
        'Authorization': token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"Restarting {worker_name} with {worker_guid} ")

# print(f"\n {guid_list}")
time.sleep(30)

# TODO Get the worker status after restart
# for worker in worker_list:
#     url = f"{base_url}?page=1&per_page=1000&space_guids={space_guid}&names={worker}"
#
#     payload = {}
#     headers = {
#         'Authorization': token
#     }
#
#     response_for_guid = requests.request("GET", url, headers=headers, data=payload)
#     response_guid_dict = json.loads(response_for_guid.text)
#     worker_name = response_guid_dict["resources"][0]["name"]
#     worker_state = response_guid_dict["resources"][0]["state"]
#     print(f"{worker_name} is {worker_state}")

# # TODO get the process state
for guid in guid_list:
    url = f"https://api.cf.sap.hana.ondemand.com/v3/processes/{guid}/stats"
    payload = {}
    headers = {
        'Authorization': token
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    for i in range(0, len(response_dict["resources"])):
        print(f"for {guid}-\nindex-{response_dict['resources'][i]['index']}, state-{response_dict['resources'][i]['state']}")


