import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
#import encode_mesg
#import soliton
#import gen_matrix
#import test_imports2
import lt_codes_encode
import lt_codes_decode
import os

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "10.8.9.152"
#SERVER_HOST = "192.168.1.244"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# prompt the client for a name
name = input("Enter your name: ")

def listen_for_messages():    
    while True:
        # keep listening for a message from `cs` socket
        msg = s.recv(1024).decode()
        while msg:
            if not msg:
                break
    
            with open("serverResponse.txt", "a") as f:
                f.write(msg)
 
            s.settimeout(1)
            try:
                msg = s.recv(1024).decode()
            except Exception as e:
                s.settimeout(None)
                print("File finished transmitting")
                break
            s.settimeout(None)

#        while msg:
#            with open("testClientENC.txt", "ab") as f:
#                f.write(msg.encode())
#            msg = s.recv(1024).decode()

            #V ADDED V
#        print(msg)
        
       #Check if server is sending it multiple times or if this is writing it multiple times
    



    #  while True:
        #message needs to be initialized or else there's an infinite loop
  #      with open("testRecENC.txt", "w") as f:
  #  message = s.recv(1024).decode()
  #  print(message)
  #          f.write(message)
  #          if not message:
  #              break
  #  f.close()
  #      print("Message recieved")
#        print("Reached Decoding")
        command = 'python3 lt_codes_decode.py serverResponse.txt'
        os.system(command)
        
        print("Decoded data:\n")
        with open("serverResponse-output.txt", "r") as f:
            print(f.read())

        command = 'rm serverResponse.txt userInputENCRYPTED.txt'
        #command = 'rm serverResponse.txt'
        os.system(command)
        
#        sys.exit()

        #break
 #       command = ("rm testClientENC.txt")
 #       os.system(command)


t1 = Thread(target=listen_for_messages)
t1.daemon = True
t1.start()

def wait_for_input():
    while True:
        inputFile = "userInput.txt"
        userIn = input()

        if userIn == "q":
            s.shutdown(1)
            break

        with open(inputFile, "w") as f:
            f.write(userIn)


        command = 'python3 lt_codes_encode.py ' + inputFile
        os.system(command)

        f = open("userInputENCRYPTED.txt", "rb")
 #       print(f.read())
 #           if not fileData: 
 #               break
 #           while fileData: 
 #       fileData = f.read()
        s.sendfile(f, offset=0, count=None)
 #       s.sendall(str(fileData).encode()) 
        print("sending data...")
 #       fileData = f.read() 
            # File is closed after data is sent 
        f.close() 
  
        #except IOError: 
        #    print('You entered an invalid filename! Please enter a valid name') 


  #  to_send = "sending a message to activate decoding"
  #  s.send(to_send.encode())

wait_for_input()

# close the socket
s.close()
