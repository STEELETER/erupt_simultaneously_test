import json
import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('172.21.1.13',9090))
s.listen(20)
client_socket,address = s.accept()
data = client_socket.recv(1024).decode()
# print(data)
# print(type(data))
# new = json.loads(data)
# print(new)
# print(type(new))
b=eval(data)
print(b)
if int(b['sysnum']) == 868608:
    if b['identity'] == 'user':
        print('1')
    else:
        print('2')

else:
    print('非法')