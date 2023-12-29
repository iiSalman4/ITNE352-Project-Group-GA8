import socket
import threading
import requests
import json


def get_data(client_socket, recv_option):

    #open the json file to extract data
    with open("GA8.json", 'r') as file:
        data = json.load(file)
        flights = data.get('data', [])

    if recv_option.lower() == 'a':
        # Extract the required information for arrived flights
        arrived_flights = []
        for flight in flights:
            if flight['flight_status'] == 'landed':
                flight_info = {
                    'Flight IATA Code': flight['flight']['iata'],
                    'Departure Airport Name': flight['departure']['airport'],
                    'Arrival Time': flight['arrival']['estimated'],
                    'Arrival Terminal Number': flight['arrival']['terminal'],
                    'Arrival Gate': flight['arrival']['gate']
                }
                arrived_flights.append(flight_info)
        return json.dumps(arrived_flights, indent=2)

    elif recv_option.lower() == 'b':
        # Extract the required information for delayed flights
        delayed_flights = []
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
                delayed_flights.append(flight_info)
        return json.dumps(delayed_flights, indent=2)

    elif recv_option.lower() == 'c':
        # Extract the required information for all flights from a specific airport
        airport_code = client_socket.recv(1024).decode("ascii")
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
            return "Airport not found."
    elif recv_option.lower() == 'd':
        flight_iata_code = client_socket.recv(1024).decode().strip()
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
            return "Flight not found."

    else:
        client_socket.send(b"Invalid option. Please choose again.")


def clients_handler(client_socket, name):
    while True:
        #send the options to the client
        client_socket.send(b"Choose on of the following Options: \n"
                           b"a. ALL Arrived Flights \n"
                           b"b. ALL Delayed Flights \n"
                           b"c. ALL Flight From a Specific Airport \n"
                           b"d. Details Of a Particular Flight \n"
                           b"e. to terminate the connection")

        # receive the client's choice 
        recv_option = client_socket.recv(1024).decode('ascii')

        #option 'e' to close the connection and print that the client has disconnected
        if recv_option.lower() == 'e':
            client_socket.close()
            print(f"client: {name} has disconnected")
            return
        
        print(f'client: {name} chose option: {recv_option}')
        response = get_data(client_socket, recv_option)#get the desired data using the option from the client
        client_socket.send(response.encode('ascii'))#send the data to the client
        print(65*'-')
        print(response)#for testing and development
        print(65*'-')


def main():
    #the code to retrieve the data from the api commented for development and testing 
    """
    airport_code = input("Enter airport ICAO code: ")

    api_key = '97cb3a487d121f559d1dea7e9565fe33'
    url = f'http://api.aviationstack.com/v1/flights?access_key={api_key}&arr_icao={airport_code}&limit=100'

    response = requests.get(url)
    data = response.json()

    with open("GA8.json", 'w') as file:
        json.dump(data, file, indent=4)
"""
    #create the socket and start listening 
    server4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server4.bind(('127.0.0.1', 9999))
    server4.listen()
    print("Server listening on {}:{}".format('127.0.0.1', 9999))

    while True:
        client_socket, addr = server4.accept()
        print("Client connected:", addr)
        # Receive the name from the client
        name = client_socket.recv(1024).decode('ascii')
        print(f"Client: {name} successfully connected")
        #thread to be able to handle multiple clients
        clients_thread = threading.Thread(target=clients_handler, args=(client_socket, name))
        clients_thread.start()


if __name__ == "__main__":
    main()
