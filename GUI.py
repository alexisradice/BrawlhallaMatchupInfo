import tkinter as tk
import tkinter as ttk
from queue import Queue
from threading import Thread
from main import detect_brawlhalla
import requests


# response = requests.get("http://localhost:8080/api/brawl/Boomie&1700")
# apiResult = response.json()
# print(apiResult['resultJSON']['level'])

myBrawlID = 0

def infosBrawlRecuperation():

    if not q.empty():
        finalList = q.get()
        # print(finalList)
        #characterPlayer.set(finalList[0])
        characterPlayerEntry.delete(0, tk.END) #deletes the current value
        characterPlayerEntry.insert(0, finalList[0]) #inserts new value assigned by 2nd parameter

        #tagPlayer.set(finalList[1])
        tagPlayerEntry.delete(0, tk.END)
        tagPlayerEntry.insert(0, finalList[1])

        #namePlayer.set(finalList[2])
        namePlayerEntry.delete(0, tk.END)
        namePlayerEntry.insert(0, finalList[2])

        #clanPlayer.set(finalList[3])
        clanPlayerEntry.delete(0, tk.END)
        clanPlayerEntry.insert(0, finalList[3])

        q.task_done()

        print(myBrawlID)

        myElo = 1700

        try:
            link = "http://localhost:8080/api/brawl/{}&{}".format(finalList[2], myElo)
            response = requests.get(link)
            apiResult = response.json()
            levelPlayerAPI = apiResult['playerStatsJSON']['level']
            ratingPlayerAPI = apiResult['playerRankedJSON']['rating']


            levelPlayerEntry.delete(0, tk.END)
            levelPlayerEntry.insert(0, levelPlayerAPI)

            ratingPlayerEntry.delete(0, tk.END)
            ratingPlayerEntry.insert(0, ratingPlayerAPI)
        except Exception as e:
            print (e)


    root.after(100, infosBrawlRecuperation)




q = Queue()
t = Thread(target=detect_brawlhalla, args=(q,))
def validateBrawlID():
    t.start()

    global myBrawlID
    myBrawlID = brawlID.get()
    frame.pack_forget()
    mainFrame.pack()



root = tk.Tk()
root.title('Test GUI')
root.geometry("300x100")

frame = ttk.Frame(root)
frame.pack()

characterPlayer = tk.StringVar()
brawlIDLabel = ttk.Label(frame, width = 20, text = 'Enter your Brawlhalla ID : ')
brawlIDLabel.grid(column = 0, row = 0)
brawlID = tk.StringVar()
brawlIDEntry = ttk.Entry(frame, width = 20, textvariable = brawlID)
brawlIDEntry.grid(column = 0, row = 1)
validateButton = ttk.Button(frame, width = 20, text = 'Validate', command = validateBrawlID)
validateButton.grid(column = 0, row = 2)


mainFrame = ttk.Frame(root)


# OCR Infos

characterPlayer = tk.StringVar()
characterPlayerEntry = ttk.Entry(mainFrame, width = 20, textvariable = characterPlayer)
characterPlayerEntry.grid(column = 1, row = 0)
characterPlayerLabel = ttk.Label(mainFrame, width = 20, text = 'Character : ')
characterPlayerLabel.grid(column = 0, row = 0)

tagPlayer = tk.StringVar()
tagPlayerEntry = ttk.Entry(mainFrame, width = 20, textvariable = tagPlayer)
tagPlayerEntry.grid(column = 1, row = 1)
tagPlayerLabel = ttk.Label(mainFrame, width = 20, text = 'Tag : ')
tagPlayerLabel.grid(column = 0, row = 1)

namePlayer = tk.StringVar()
namePlayerEntry = ttk.Entry(mainFrame, width = 20, textvariable = namePlayer)
namePlayerEntry.grid(column = 1, row = 2)
namePlayerLabel = ttk.Label(mainFrame, width = 20, text = 'Player Name : ')
namePlayerLabel.grid(column = 0, row = 2)

clanPlayer = tk.StringVar()
clanPlayerEntry = ttk.Entry(mainFrame, width = 20, textvariable = clanPlayer)
clanPlayerEntry.grid(column = 1, row = 3)
clanPlayerLabel = ttk.Label(mainFrame, width = 20, text = 'Clan : ')
clanPlayerLabel.grid(column = 0, row = 3)

# API Infos

levelPlayer = tk.StringVar()
levelPlayerEntry = ttk.Entry(mainFrame, width = 20, textvariable = levelPlayer)
levelPlayerEntry.grid(column = 1, row = 4)
levelPlayerLabel = ttk.Label(mainFrame, width = 20, text = 'Level : ')
levelPlayerLabel.grid(column = 0, row = 4)

ratingPlayer = tk.StringVar()
ratingPlayerEntry = ttk.Entry(mainFrame, width = 20, textvariable = ratingPlayer)
ratingPlayerEntry.grid(column = 1, row = 5)
ratingPlayerLabel = ttk.Label(mainFrame, width = 20, text = 'Rating : ')
ratingPlayerLabel.grid(column = 0, row = 5)

infosBrawlRecuperation()


root.mainloop()

"""
import tkinter as tk
print("rrs")
root = tk.Tk()
root.minsize(900, 600)
root.geometry("1080x720")
root.title("TWIBOTCH")
root.mainloop()
"""