"""
Drew Dahlquist
14340970
CS 4850, Computer Networks
March 18, 2022

TODO: Program description
"""

"""
something helpful...
lsof -i tcp:10970
"""

import socket

# constant vars for connection
HOST='127.0.0.1'
PORT=10970

# state var for whether user is logged in or not
loggedin = False

print()
print('My chat room client. Version One.')
print()

while True:
    # some standard socket setup
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        cmd = input() # user command
        parsed = cmd.split() # for parsing/processing only

        # handle login logic
        if(parsed[0] == 'login'):
            # correct usage
            if(loggedin == False and len(parsed) == 3):
                s.send(cmd.encode())
                data = s.recv(1024)
                # success
                if(data.decode().startswith('Ack:')):
                    loggedin = True # update state var
                    print('login confirmed')
                # error
                else:
                    print('Denied. User name or password incorrect.')
            # incorrect usage
            else:
                print('Err:Client: Not logged out.')

        # handle newuser logic
        elif(parsed[0] == 'newuser'):
            # correct usage
            if(loggedin == False and len(parsed) == 3 and len(parsed[1]) >= 3 and len(parsed[1]) <= 32 and len(parsed[2]) >= 4 and len(parsed[2]) <= 8):
                s.send(cmd.encode())
                data = s.recv(1024)
                # success
                if(data.decode().startswith('Ack:')):
                    print('New user account created. Please login.')
                # error
                else:
                    print('Denied. User account already exists.')
            # incorrect usage
            else:
                print('Err:Client: Not logged out.')

        # handle send logic
        elif(parsed[0] == 'send'):
            # correct usage
            if(loggedin == True and len(parsed) >= 2 and len(' '.join(parsed[1:])) >= 1 and len(' '.join(parsed[1:])) <= 256):
                s.send(cmd.encode())
                data = s.recv(1024)
                # success
                if(data.decode().startswith('Ack:')):
                    msg = data.decode().split(':')[2]+':'
                    print(msg+''.join(data.decode().split(':')[3:]))
                # error
                else:
                    pass
            # incorrect usage
            else:
                print('Denied. Please login first.')

        # handle logout logic
        elif(parsed[0] == 'logout'):
            # correct usage
            if(loggedin == True and len(parsed) == 1):
                s.send(cmd.encode())
                data = s.recv(1024)
                # success
                if(data.decode().startswith('Ack:')):
                    print(''.join(data.decode().split(':')[2:]))
                # error
                else:
                    pass
                # close socket
                s.close()
                loggedin = False # update state var
                exit() # exit program
            # incorrect usage
            else:
                print('Err:Client: Not logged in.')
        
        # command not recognized
        else:
            print('Err:Client: Invalid command. Try again.')
