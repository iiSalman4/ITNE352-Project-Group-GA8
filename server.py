import socket
import threading
import requests
import json


def send_option(client_socket, recv_option, name):
    
    with open("GA8.json", 'r') as file:
        data = json.load(file)
        flights = data.get('data', [])

    if recv_option.lower() == 'a':
        print(f'client: {name} chose option: A. All Arrived Flights ')
        # Extract the required information for all arrived flights
        data = []
        for flight in flights:
            if flight['flight_status'] == 'landed':
                flight_info = {
                    'Flight IATA Code': flight['flight']['iata'],
                    'Departure Airport Name': flight['departure']['airport'],
                    'Arrival Time': flight['arrival']['estimated'],
                    'Arrival Terminal Number': flight['arrival']['terminal'],
                    'Arrival Gate': flight['arrival']['gate']
                }
                data.append(flight_info)
        if data:
            return json.dumps(data, indent=2)
        else:
            return "No Arrived Flights found."
       
    elif recv_option.lower() == 'b':
        print(f'client: {name} chose option: B. All Delayed Flights ')
        # Extract the required information for all arrived flights
        data = []
        for flight in flights:
            if flight['arrival']['delay'] != None:
                flight_info = {
                    'Flight IATA Code': flight['flight']['iata'],
                    'Departure Airport Name': flight['departure']['airport'],
                    'Original departure time': flight['departure']['scheduled'],
                    'Estimated arrival time': flight['arrival']['estimated'],
                    'Arrival Terminal Number': flight['arrival']['terminal'],
                    'Delay': flight['arrival']['delay'],
                    'Arrival Gate': flight['arrival']['gate']
                }
                data.append(flight_info)
        if data:
            return json.dumps(data, indent=2)
        else:
            return "No Delayed Flights found."

    elif recv_option.lower() == 'c':
        # Extract the required information for all flights from a specific airport
        airport_code = client_socket.recv(1024).decode("ascii")
        print(f'client: {name} chose option: C. All Flights From Airport {airport_code}')
        data = []
        for flight in flights:
            if flight['departure']['iata'] == airport_code:
                flight_info = {
                    'Flight IATA Code': flight['flight']['iata'],
                    'Departure Airport Name': flight['departure']['airport'],
                    'Original departure time': flight['departure']['scheduled'],
                    'Estimated arrival time': flight['arrival']['estimated'],
                    'Departure Gate': flight['departure']['gate'],
                    'Arrival Gate': flight['arrival']['gate'],
                    'Status': flight['flight_status']
                }
                data.append(flight_info)
        if data:
            return json.dumps(data, indent=2)    
        else:
            return f"Airport {airport_code} not found."
        

    elif recv_option.lower() == 'd':
        flight_iata_code = client_socket.recv(1024).decode().strip()
        print(f'client: {name} chose option: D. Details of Flight Number {flight_iata_code}')
        data = []
        for flight in flights:
            if flight['flight']['iata'] == flight_iata_code:
                specific_flight = {
                    'Flight IATA Code': flight['flight']['iata'],
                    'Departure Airport Name': flight['departure']['airport'],
                    'Departure Gate': flight['departure']['gate'],
                    'Departure Terminal Number': flight['departure']['terminal'],
                    'Arrival Airport Name': flight['arrival']['airport'],
                    'Arrival Gate': flight['arrival']['gate'],
                    'Arrival Terminal Number': flight['arrival']['terminal'],
                    'Status': flight['flight_status'],
                    'Scheduled Departure Time': flight['departure']['scheduled'],
                    'Scheduled Arrival Time': flight['arrival']['scheduled']
                }
                data.append(specific_flight)
        if data:
            return json.dumps(data, indent=2)
        else:
            return f"Flight {flight_iata_code} not found."


def clients_handler(client_socket, addr):
    try:
        #Receives the client name.
        name = client_socket.recv(1024).decode('ascii')
        print(f"accepted connection with {addr} client's name is: {name}")
        while True:
            # to send the option
            recv_option = client_socket.recv(1024).decode('ascii')
            response = send_option(client_socket, recv_option, name)
            client_socket.sendall((response).encode('ascii'))   
    except :
        print(f"connection with {name} at address {addr} has been disconnected")

def main():
    
    """airport_code = input("Enter the airport's ICAO code: ")

    api_key = '97cb3a487d121f559d1dea7e9565fe33'
    url = f'http://api.aviationstack.com/v1/flights?access_key={api_key}&arr_icao={airport_code}&limit=100'

    response = requests.get(url)
    data = response.json()

    with open("GA8.json", 'w') as file:
        json.dump(data, file, indent=4)"""
        
    server4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server4.bind(('127.0.0.1', 9999))
    server4.listen()
    print("Server listening on {}:{}".format('127.0.0.1', 9999))

    while True:
        client_socket, addr = server4.accept()

        #thread to handle multiple clients.
        clients_thread = threading.Thread(target=clients_handler, args=(client_socket, addr))
        clients_thread.start()
        
if __name__ == "__main__":
    main()
