import socket
from threading import Thread
from tkinter import *

#nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__ (self) :
        self.window = Tk()
        self.window.withdraw()

        self.login = Toplevel()
        self.login.title("login")
        self.login.resizable(width=False ,height=False )  
        self.login.configure(width=400, height=300)   

        self.pls=Label(self.login, text="Please login to continue", justify=CENTER, font="Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.labelname= Label(self.login, text="Name : ", font="Helvetica 12")
        self.labelname.place(relheight=0.2, relx=0.1, rely=0.2)

        self.entryname = Entry(self.login,font="Helvetica 12" )
        self.entryname.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        self.entryname.focus()

        self.go = Button(self.login, text="Continue", font="Helvetica 14 bold", command= lambda: self.goahead(self.entryname.get()))
        self.go.place(relx=0.4, rely=0.55)

        self.window.mainloop()

    def goahead(self, name):
        self.login.destroy()
        self.layout(name)
        rcv=Thread(target=self.receive)
        rcv.start()

    def layout(self, name):
        self.name = name
        self.window.deiconify()
        self.window.title("Chat Room")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg="#17202A")

        self.labelhead = Label(self.window, text=self.name, bg="#17202A", fg="#eaecee", font="Helvetica 13 bold", pady=5)
        self.labelhead.place(relwidth=1)

        self.line = Label(self.window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textcons = Text(self.window, width=20, height=2, bg="#17202A", fg="#EAECEE", font="Helvetica 13", padx=5, pady=5)
        self.textcons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelbutton = Label(self.window, bg="#ABB2B9", height=80)
        self.labelbutton.place(relwidth=1, rely=0.825)

        self.entrymsg = Entry(self.labelbutton, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")
        self.entrymsg.place(relheight=0.06, relwidth=0.74, rely=0.008, relx=0.011)
        self.entrymsg.focus()

        self.btnmsg = Button(self.labelbutton, text="Send", font="Helvetica 10 bold", bg="#ABB2B9", width=20, command=lambda:self.sendbtn(self.entrymsg.get()))
        self.btnmsg.place(relx=0.77, rely=0.008, relheight=0.06,relwidth=0.22)

        self.textcons.config(cursor="arrow")
        scrollbar = Scrollbar(self.textcons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textcons.yview)
        self.textcons.config(state=DISABLED)

    def sendbtn(self, msg):
        self.textcons.config(state=DISABLED)
        self.msg= msg
        self.entrymsg.delete(0,END)  
        snd=Thread(target=self.write)
        snd.start()

    def showmsg(self, msg) :
        self.textcons.config(state=NORMAL)
        self.textcons.insert(END, msg+"\n\n")
        self.textcons.config(state=DISABLED)
        self.textcons.see(END)     

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    print(message)
                    self.showmsg(message)
            except:
                print("An error occured!")
                client.close()
                break

    def write(self):
        self.textcons.config(state=DISABLED)
        while True:
            message = (f"{self.name}:{self.msg}")
            client.send(message.encode('utf-8'))
            self.showmsg(message)
            break      
    
g=GUI()

#def write():
#    while True:
 #       message = '{}: {}'.format(nickname, input(''))
  #      client.send(message.encode('utf-8'))

#receive_thread = Thread(target=receive)
#receive_thread.start()
#write_thread = Thread(target=write)
#write_thread.start()
