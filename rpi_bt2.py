from bluetooth import *
from tkinter import *
from PIL import Image, ImageTk
from guizero import App, Text, Box, Picture
import rpi_predict


msg = ""
dir = ""

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
        words = []
        words = data.split(" ")

        def transport_sms(x):
            ans = rpi_predict.applier([x])
            if (ans == "ham"):
                global msg
                msg = "urgent"

        def sms_function():
            return (msg)

        def transport_direction(y):
            global dir
            dir = y

        def img_function():
            return (dir)

        if (words[0] == "sms"):
            transport_sms(words)
        if (words[0] == "direct"):
            transport_direction(words)

        text = sms_function()
        z = img_function()

        # gui code 2
        window = Tk()
        window.title("HUD")
        window.geometry("250x250")

        if (msg == "urgent"):
            image2 = Image.open("mail.png")
        else:
            image2 = Image.open("default.png")

        if (z == "left"):
            image1 = Image.open("left.png")
        elif (z == "right"):
            image1 = Image.open("right.png")
        elif (z == "straight"):
            image1 = Image.open("forward.png")
        elif (z == "turn"):
            image1 = Image.open("back.png")
        else:
            image1 = Image.open("default.png")

        image1 = image1.resize((50, 50), Image.ANTIALIAS)
        ph1 = ImageTk.PhotoImage(image1)
        image2 = image2.resize((50, 50), Image.ANTIALIAS)
        ph2 = ImageTk.PhotoImage(image2)

        frame = Frame(window)
        frame.configure(background="#333")
        Label(frame, image=ph1).pack(side=TOP, expand=YES)
        Label(frame, image=ph2).pack(side=BOTTOM, expand=YES)

        frame.pack(fill=BOTH, expand=YES)
        window.mainloop()

except IOError:
    pass


#gui code1
'''
if(z=="left"):
    image = "left.png"
elif(z=="right"):
    image = "right.png"
elif(z=="straight"):
    image = "forward.png"
elif(z=="turn"):
    image = "back.png"


app = App(title="HUD HUD",width=250, height=250, bg="black")
#message_box = Box(app, width="fill", align="top")
#message = Text(message_box, "", size=13, font="Calibri", color="lightblue")
message = Picture(app, image2, width=50, height=50, align="top")
message.after(1000, sms_function())
direction = Picture(app, image, width=50, height=50, align="bottom")
app.display()
'''

#close connection
print("Disconnected")
client_sock.close()
server_sock.close()
print("Done")