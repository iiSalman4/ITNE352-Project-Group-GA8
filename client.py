import socket


#To make sure all the data is received
def receive_large_data(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(("127.0.0.1", 9999)) # connect to the server
except:
    print("cant find server !") # if cant be found then the client will shutdown
    exit(0)



name = input("Enter your name: ") # gets the client name from user 
client.send(name.encode('ascii')) # send name to the server after encoding it


print(f"------------Welcome {name}-------------")
while True:
    recv_option = client.recv(2085).decode()

    print(recv_option)
    choice=input("please Enter your choice: ")
    client.send(choice.encode('ascii'))
    
    # quit option
    if choice.lower() == 'e':
        break
    
    #print the received data
    received_data = receive_large_data(client)
    received_data=received_data.decode('ascii')
    print(received_data,'\n')
client.close()
