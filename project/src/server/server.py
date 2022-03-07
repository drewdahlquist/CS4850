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

online = str()
users = dict()

print()
print('My chat room server. Version One.')
print()

# read in users.txt on startup
with open('users.txt') as file:
    lines = file.read().splitlines()
    for line in lines:
        user, pwd = line.strip('()').split(', ')
        users[user] = pwd

# open socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    # print(f"Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            # print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # conn.sendall(data)

                cmd = str(data.decode())
                parsed = cmd.split()
                
                if(parsed[0] == 'login' and len(parsed) == 3):
                    # valid user & pass
                    if(parsed[1] in users.keys() and parsed[2] == users[parsed[1]]):
                        online = parsed[1]
                        ack = f'Ack:Server: Logged on as {online}.'
                        conn.send(ack.encode())
                        print(f'{online} login.')
                    # error
                    else:
                        err = f'Err:Server: Invalid username or password.'
                        conn.send(err.encode())

                if(parsed[0] == 'newuser' and len(parsed) == 3):
                    # user creation
                    if(parsed[1] not in users.keys()):
                        users[parsed[1]] = parsed[2]
                        ack = f'Ack:Server: New user created with username: {parsed[1]}, password: {parsed[2]}.'
                        conn.send(ack.encode())
                        print('New user account created.')
                    # user already exists
                    else:
                        err = f'Err:Server: User already exists.'
                        conn.send(err.encode())
                
                if(parsed[0] == 'send' and len(parsed) >= 2):
                    # logged in
                    if(online != ''):
                        ack = f'Ack:Server:{online}: {" ".join(parsed[1:])}'
                        conn.sendall(ack.encode())
                        print(f'{online}: {" ".join(parsed[1:])}')
                    # not logged in
                    else:
                        err = f'Err:Server: Not logged in.'
                        conn.send(err.encode())

                if(parsed[0] == 'logout'):
                    # logged in
                    if(online != ''):
                        ack = f'Ack:Server:{online} left.'
                        conn.send(ack.encode())
                        print(f'{online} logout.')
                        online = ''
                    # not logged in
                    else:
                        err = f'Err:Server: Not logged in.'
                        conn.send(err.encode())