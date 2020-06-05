from pytube import * #  importing libaries all
from tkinter import * #graphics 
from tkinter.filedialog import * #importing for diloauge box
from tkinter.messagebox import * #popup mseeage
from threading import * #thread handiling
import pafy #audio libary 
import random
select = None
size = 0
#continious progress check....
def checkprogress(stream, chunk, remaining):
    p = ((size - remaining/1024**2)/size)*100
    btn.configure(text="Downloading...  {:.2f} %".format(p))

def download():
    try: 
        global size      
        url = field.get()
        print(url)
        #changing button 
        btn.configure(text="Downloading...")
        btn['state']= 'disable'

        downloc = askdirectory() #ask path for download location
        print(downloc)
        if downloc is None:
            return
        if(select == "video"):
#utube object with url
            ob = YouTube(url, on_progress_callback = checkprogress)

#getting n assigning all available strems --- .all()
            streams = ob.streams.first() #only first stream- first stream is alwz progressive and high quality one(usually 360p)
            size = streams.filesize/1024**2
            print("Resolution: " + str(streams.resolution))
            btn2.config(state=NORMAL)
        else:
            ob = pafy.new(url)
            streams = ob.getbestaudio() #best quality audio
            size = streams.get_filesize()/1024**2  #filesize
            btn1.config(state=NORMAL)
            
        tt.config(text ='Title:'+ streams.title + '-{}MB'.format(str(round(size,2)))) #for stream title  with  size
        tt.pack(side=TOP, pady=5)
#downloading
        streams.download(downloc)
#re-configuring button
        btn.config(text="Download")
        #btn.config(state=NORMAL)

#pop-up message
        showinfo("Download Completed","Downloaded Successfully")

        field.delete(0,END) #deleting old url
        tt.pack_forget()    #deleting title box
    
    except Exception as e:
        print(e)
        print("Error!!")

def startdownload(): #threat to download - to  handel downloading
    th = Thread(target = download)
    th.start()


#GUI building
box = Tk()
box.title("Utube_Video_Downloader")
#set icon
box.iconbitmap('images.ico')
box.geometry("500x500")

#inside main box
#image
file = PhotoImage(file='images.png')
img = Label(box,image=file)
img.pack(side=TOP)

#url enrty
def clear(event): #function to delete defult text
    field.delete(0,END)
field = Entry(box, font=("Comic Sans MS italic",16),justify=CENTER)
#default entry value.
field.insert(0,"Video_Url...")
field.bind("<Button-1>",clear) #calling clear function on clicking
field.pack(side=TOP, fill=X, padx=30, pady=5) #x-axi n y-axis padding 

#buttonss
btn = Button(box, text="Start Download", bg="green", fg="white", \
    font=("Comic Sans MS italic", 16), relief="groove", state='disabled')
btn['command']=startdownload  #calling function -thread
btn.pack(side=TOP, pady=5)

#selection button
def selection(id):
    global select
    btn.config(state='normal') #enables downloading as type is selected
    if(id == 1):
        select = "video"
        btn2['state']= 'disable'
        
    else:
        select = "audio"
        btn1['state'] = 'disable'

btn1 = Button(box, text="Video + Audio", bg="green", fg="white", \
    font=("Comic Sans MS italic", 10), relief="groove")
btn1['command']=lambda:selection(1) #calling function selection on clicking btn1
btn1.pack()

btn2 = Button(box, text="Audio", bg="green", fg="white",  \
    font=("Comic Sans MS italic", 10), relief="groove")
btn2.bind('<Button-1>',selection)   #btn2['command']=lambda:selection(2)
btn2.pack()
#button geometry
btn1.place(x=230, y=345)
btn2.place(x=180, y=345)

#title for video
tt = Label(box, bg="#ccccb3", fg="white", font=("Comic Sans MS italic", 12))

#message from file.
def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)
mess = random_line('test.txt')
#tkinter canvas for text
tx = Canvas(box, height= 40, width = 400)
tx.create_text(200, 20, font=("Segoe Print",10), anchor="center",
    text=mess, width= 390)
tx.pack(pady=40, padx=10, side=BOTTOM)
box.mainloop()
