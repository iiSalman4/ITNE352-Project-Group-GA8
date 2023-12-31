import socket
import customtkinter

def receive_large_responses(socket):
    response = b''
    while True:
        part = socket.recv(4096)
        response += part
        if len(part) < 4096:
            break
    return response

def name_enter_button():
    try:
        #gets the client name from the Entry box "name".
        client_name=name.get()
        if client_name:
            # connect to the server
            client.connect(("127.0.0.1", 9999)) # connect to the server
            
            client.send(client_name.encode('ascii'))
            #remove the frame for the name entry and show the frame for the rest of the options.
            frame1.pack_forget()
            frame.pack(expand="true")
        else:
            #displays the text in red if the user has clicked the button without entering a name.
            name_error =customtkinter.CTkLabel(frame1, text="Please Enter Your Name To Continue", font=("", 20), text_color="red")
            name_error.grid(column=1, row=2)
    except:
        print("Error can't communicate with the server")
        app.destroy()

def send_option_to_server(choice):
    try:
        #sends the choices and the input if applicable to the server.
        if choice == 'c':
            input = opt_C_IATA.get()
            if not input:
                opt_C_IATA.configure(placeholder_text_color="red", font=('',17))
            else:
                client.send(choice.encode('ascii'))
                client.send(input.encode('ascii'))
                opt_C_IATA.configure(placeholder_text_color="gray", font=('',14))
                opt_C_IATA.delete("0","end")
                receive_and_print_data(choice)
        elif choice == 'd':
            input = opt_D_IATA.get()
            if not input:
                opt_D_IATA.configure(placeholder_text_color="red", font=('',17))
            else:
                client.send(choice.encode('ascii'))
                client.send(input.encode('ascii'))
                opt_D_IATA.configure(placeholder_text_color="gray", font=('',14))
                opt_D_IATA.delete("0","end")
                receive_and_print_data(choice)
        else:
            client.send(choice.encode('ascii'))
            receive_and_print_data(choice)
    except:
        print("Error can't communicate with the server")
        app.destroy()

def receive_and_print_data(choice):
    #calls receive_large_responses function then printing the response in the textbox.
    received_data = receive_large_responses(client)
    received_data=received_data.decode('ascii')
    
    textbox.configure(state="normal")
    textbox.delete('1.0', 'end')
    textbox.insert("end", f"Server's response for option {choice.upper()}: \n")
    textbox.insert("end", received_data)
    textbox.configure(state="disabled")

def quit_command():
    #closes the connection and gui if user presses quit button.
    client.close()
    app.destroy()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


######################################################################################################################################
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("720x480")
app.title("ITNE352")

#Frames for the username window and options window
frame = customtkinter.CTkFrame(app, fg_color="transparent")
frame1 = customtkinter.CTkFrame(app, fg_color="transparent")

quit_button = customtkinter.CTkButton(app, text= "quit", command=quit_command, width = 60, height = 20)
quit_button.pack(anchor = "nw")

#client's name entry box and enter button
name = customtkinter.CTkEntry(frame1, placeholder_text="Enter your name",font=("",18), width=250, height=60,)
name.grid(column=1, row=0, pady=10,)
button=customtkinter.CTkButton(frame1, text="Enter", font=("",18), width=250, height=60, command=name_enter_button)
button.grid(column=1, pady=10, row=1)
frame1.pack(expand="true")


#options buttons and input boxes
button1=customtkinter.CTkButton(frame, font=("",14), text="A. All Arrived Flights",width=230, height=40, command=lambda: send_option_to_server('a'))
button1.grid(column=0, pady=10, row=2, padx=30 )

button2=customtkinter.CTkButton(frame, font=("",14), text="B. All Delayed Flights", width=230, height=40, command=lambda: send_option_to_server('b'))
button2.grid(column=0, pady=10, row=4, padx=30)

opt_C_IATA = customtkinter.CTkEntry(frame, font=("",14), placeholder_text="Enter The Airport's IATA Code", width=230, height=40)
opt_C_IATA.grid(column=2,row=3, padx=30)

button3=customtkinter.CTkButton(frame, font=("",14), text="C. All Flights From a Specific Airport", width=230, height=40, command=lambda: send_option_to_server('c'))
button3.grid(column=2, row=2, padx=30)

opt_D_IATA = customtkinter.CTkEntry(frame, font=("",14), placeholder_text="Enter The Flight's IATA Code", width=230, height=40)
opt_D_IATA.grid(column=2,  row=5, padx=30)

button4=customtkinter.CTkButton(frame, font=("",14), text="D. Details of a Particular Flight", width=230, height=40, command=lambda: send_option_to_server('d'))
button4.grid(column=2, row=4, padx=30)

#response box 
textbox= customtkinter.CTkTextbox(frame, width=720)
textbox.configure(state="disabled")
textbox.grid(column=0, columnspan=3, row=6, pady = 30)

try:
    app.mainloop()

except:
    print("Error client terminated")