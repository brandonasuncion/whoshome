'''
Who's Home
by Brandon Asuncion <me@brandonasuncion.tech>

Uses an ASUS router's web interface to determine active wireless devices.
'''
import requests
import re
import json
from base64 import b64encode
from collections import defaultdict

### START CONFIG ###

USERNAME = "username"
PASSWORD = "password"
GATEWAY = "192.168.1.1"

USERS = {
    'Me': ['5C:F9:38:8E:0B:E6', '60:9A:C1:12:9A:13'],
    'Dad': ['D0:33:11:5F:01:0E'],
    'Mom': ['D0:A6:37:7F:8F:99'],
}

### END CONFIG ###

safeInt = lambda i: int(i) if i.strip() else 0

def getActiveClients():
    s = requests.Session()

    loginData = {
        'group_id': '',
        'action_mode': '',
        'action_script': '',
        'action_wait': '5',
        'current_page': 'Main_Login.asp',
        'next_page': 'index.asp',
        'login_authorization': b64encode("{}:{}".format(USERNAME, PASSWORD).encode())
    }

    reqHeaders = {'Referer': "http://{}/".format(GATEWAY)}

    # Login to router
    s.post("http://{}/login.cgi".format(GATEWAY), data=loginData, headers=reqHeaders, verify=False)

    # Get client data
    clientData = s.get("http://{}/update_clients.asp".format(GATEWAY), headers=reqHeaders, verify=False).text

    # Logout
    s.get("http://{}/Logout.asp".format(GATEWAY), headers=reqHeaders, verify=False)


    activeClients = defaultdict(lambda :{})
    clientLists = re.findall(r"(?:g:(\s){1,})(\[(.)*?],\n)", clientData)
    for cList in clientLists:

        clientData = json.loads(cList[1].strip()[:-1])
        for c in clientData:
            device = c[0]

            if ':' in c[3]:
                activeClients[device]['Tx'] = safeInt(c[1])
                activeClients[device]['Rx'] = safeInt(c[2])
                activeClients[device]['accessTime'] = c[3]
                
            else:
                activeClients[device]['isWireless'] = c[1] == 'Yes'
                activeClients[device]['unknown'] = c[2] == 'Yes'
                activeClients[device]['RSSI'] = c[3]

    return activeClients

def activeUsers():
    activeClients = getActiveClients()
    for user, MACs in USERS.items():
        if any(device in activeClients for device in activeClients):
            yield user

if __name__ == '__main__':
    for user in activeUsers():
        print(user)