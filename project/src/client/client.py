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

HOST='127.0.0.1'
PORT=10970

loggedin = False

print()
print('My chat room client. Version One.')
print()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        cmd = input()

        parsed = cmd.split()

        if(parsed[0] == 'login'):
            if(loggedin == False and len(parsed) == 3):
                s.send(cmd.encode())
                data = s.recv(1024)
                # print(f'{data.decode()!r}')
                # success
                if(data.decode().startswith('Ack:')):
                    loggedin = True
                    print('login confirmed')
                else:
                    print('Denied. User name or password incorrect.')
            # err
            else:
                print('Err:Client: Not logged out.')

        elif(parsed[0] == 'newuser'):
            if(loggedin == False and len(parsed) == 3 and len(parsed[1]) >= 3 and len(parsed[1]) <= 32 and len(parsed[2]) >= 4 and len(parsed[2]) <= 8):
                s.send(cmd.encode())
                data = s.recv(1024)
                # print(f'{data.decode()!r}')
                # success
                if(data.decode().startswith('Ack:')):
                    print('New user account created. Please login.')
                # err
                else:
                    print('Denied. User account already exists.')
            # err
            else:
                print('Err:Client: Not logged out.')

        
        elif(parsed[0] == 'send'):
            if(loggedin == True and len(parsed) >= 2 and len(' '.join(parsed[1:])) >= 1 and len(' '.join(parsed[1:])) <= 256):
                s.send(cmd.encode())
                data = s.recv(1024)
                if(data.decode().startswith('Ack:')):
                    print(data.decode().split(':')[2:])
                else:
                    pass
            # err
            else:
                print('Denied. Please login first.')

        elif(parsed[0] == 'logout'):
            if(loggedin == True and len(parsed) == 1):
                s.send(cmd.encode())
                data = s.recv(1024)
                if(data.decode().startswith('Ack:')):
                    print(data.decode().split(':')[2:])
                else:
                    pass
                s.close()
                loggedin = False
            # err
            else:
                print('Err:Client: Not logged in.')
        
        else:
            print('Err:Client: Invalid command. Try again.')
