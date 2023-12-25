import socket
import requests
import json

airport_code = input("Enter airport ICAO code: ")

# Replace 'YOUR_API_ACCESS_KEY' with your aviationstack.com API access key
api_key = '97cb3a487d121f559d1dea7e9565fe33'
url = f'http://api.aviationstack.com/v1/flights?access_key={api_key}&arr_icao={airport_code}&limit=100'

response = requests.get(url)
data = response.json()

with open("GA8.json", 'w') as file:
    json.dump(data, file, indent=4)

server4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server4.bind(('127.0.0.1', 9999))
server4.listen()
print("Server listening on {}:{}".format('127.0.0.1', 9999))
