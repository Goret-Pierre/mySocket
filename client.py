from mySocket import MySocket
import os
os.system('cls')
screen = ""
c = MySocket()
@c.on("connection")
def affiche_receve(client):
    @c.on(client)
    def test(data):
        global screen
        screen += data.decode("utf8") + "\n"
        os.system('cls')
        print(screen)
c.connect(("localhost",5060))
data = ""
while data != "close":
    data =  input("=>")
    c.send_data(data.encode("utf8"))
c.close()
os.system("pause")