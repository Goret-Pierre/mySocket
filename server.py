from mySocket import MySocket
import os

if __name__ == "__main__":    
    # SAV
    screen = ""
    import os
    os.system('cls')
    def Startup_Message(obj):
        global screen
        screen += "Le serveur est démarrer sur \"{};{}\" \n".format(obj.host,obj.port)
    s = MySocket()
    s.bind(("localhost",5060))
    @s.on("Erreur")
    def jdnjdb():
        global screen
        screen += "un client c'est deconnecté !\n"
        os.system("cls")
        print(screen)
    @s.on("connection",)
    def affiche_receve(conn):
        global screen
        screen += "Un client c'est connecté ! \n"
        os.system('cls')
        print(screen)
        @s.on(conn)
        def test(data):
            # print(data)
            global screen
            screen += data.decode("utf8") + "\n"
            os.system('cls')
            print(screen)

    s.listen(5,Startup_Message(s))
    s.start()
    data = ""
    while data != "STOP":
        os.system('cls')
        print(screen)
        data = input()
        if data !="":
            s.send_data(data.encode("utf8"))