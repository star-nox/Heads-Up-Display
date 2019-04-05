from guizero import App, Text, Box, Picture
from guizero import system_config
print(system_config.supported_image_types)

#urgent sms notification
x=1
if(x == 1):
    text = "You have an urgent message."
else:
    text = " "

y="left"
if(y=="left"):
    image = "left.png"
elif(y=="right"):
    image = "right.png"
elif(y=="straight"):
    image = "forward.png"
elif(y=="uturn"):
    image = "turn.png"

app = App(title="HUD HUD",width=250, height=250, bg="black")

message_box = Box(app, width="fill", align="top")
message = Text(message_box, text, size=13, font="Calibri", color="lightblue")

#arrow_box = Box(app, width="fill", align="bottom")
direction = Picture(app, image="back.png", width=50, height=50, align="bottom")

app.display()