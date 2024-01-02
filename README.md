This project is about a client-server system that retrives flight information at a certain airport from an API and gives the client some options to view data.

To run the program you need to follow these steps:

1. make sure to have the server, client and JSON files all downloaded and in the same folder
2. Run the server script
3. Enter the airport code using 4 capitalised letters (for example"OBBI")
4. after the server starts, run the client script 
5. please enter your name in the designated field then click enter to proceed
6. if the connection is successful, the server will receive and display your name
7. Now the available options will show up. Please choose the selection you wish to make:
	A. To display all the arrived flights at the airport
	B. To display all the delayed flights in the airport
	C. To display all the flights coming from a specific city. (Enter departure IATA code (example"DXB")).
	D. To display the details of a particular flight. ( Enter flight IATA code(example"GF2")).
-for options C and D you have to enter the input first before clicking on the option or it won't proceed

notes: 
-the client will stay running you can enter multiple options or click the quit button to exit
-to use the program with the same data as in the JSON file you can remove the hash at line 114 and the API code will be commented

Done BY:
SALMAN ABDULLA ALSUMAIT  ID: 202108970
ABDULLA EYAD A.LATIF     ID: 202102993
ITNE352 - Group GA8   
