from bluetooth import *
from guizero import App, Text, Box, Picture


#prints all bluetooth devices
nearby_devices = discover_devices(lookup_names=True)
for name,address in nearby_devices:
    print(name, " : ", address)

#server code
server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
uuid = "8ce255c0-200a-11e0-ac64-0800200c9a66"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ])

print("Waiting for connection on RFCOMM channel ", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from: ", client_info)

#receives and prints received data
try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0:
            break
        print("Received: ", data)
except IOError:
    pass


text = data

if(data=="left"):
    image = "left.png"
elif(data=="right"):
    image = "right.png"
elif(data=="straight"):
    image = "forward.png"
elif(data=="uturn"):
    image = "turn.png"

#gui code 1

app = App(title="HUD HUD",width=250, height=250, bg="black")

message_box = Box(app, width="fill", align="top")
message = Text(message_box, text, size=13, font="Calibri", color="lightblue")
direction = Picture(app, image, width=50, height=50, align="bottom")

app.display()


print("Disconnected")
client_sock.close()
server_sock.close()
print("Done")



