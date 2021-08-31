import tkinter as tk
import tkinter as ttk
from queue import Queue
from threading import Thread
from main import detect_brawlhalla
import requests
from pathlib import Path


# response = requests.get("http://localhost:8080/api/brawl/Boomie&1700")
# apiResult = response.json()
# print(apiResult['resultJSON']['level'])

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./img/assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

brawlIdClient = 0

def mainFrame():

    def infosBrawlRecuperation():

        if not q.empty():
            finalList = q.get()
            # print(finalList)
            #characterPlayer.set(finalList[0])
            # characterPlayerEntry.delete(0, tk.END) #deletes the current value
            # characterPlayerEntry.insert(0, finalList[0]) #inserts new value assigned by 2nd parameter

            # #tagPlayer.set(finalList[1])
            # tagPlayerEntry.delete(0, tk.END)
            # tagPlayerEntry.insert(0, finalList[1])

            # #namePlayer.set(finalList[2])
            # namePlayerEntry.delete(0, tk.END)
            # namePlayerEntry.insert(0, finalList[2])

            # #clanPlayer.set(finalList[3])
            # clanPlayerEntry.delete(0, tk.END)
            # clanPlayerEntry.insert(0, finalList[3])

            q.task_done()

            print(brawlIdClient)

            try:

                linkEloClient = "https://brawlhalla-api.herokuapp.com/v1/ranked/id?brawlhalla_id={}".format(
                    brawlIdClient)
                responseEloClient = requests.get(linkEloClient)
                apiResultEloClient = responseEloClient.json()
                EloClient = apiResultEloClient["data"]["rating"]
                print(finalList[2], EloClient, brawlIdClient)

                linkAPI = "http://localhost:8080/api/brawl/{}&{}&{}".format(
                    finalList[2], EloClient, brawlIdClient)
                response = requests.get(linkAPI)
                apiResult = response.json()
                levelOpponent = apiResult['playerStatsJSON']['level']
                ratingOpponent = apiResult['playerRankedJSON']['rating']
                peakRatingOpponent = apiResult['playerRankedJSON']['peak_rating']
                mainCharacterOpponent = apiResult['playerOtherJSON']['mainCharacterFinal']
                mainWeaponOpponent = apiResult['playerOtherJSON']['mainWeaponFinal']

                levelOpponentEntry.delete(0, tk.END)
                levelOpponentEntry.insert(0, levelOpponent)

                ratingOpponentEntry.delete(0, tk.END)
                ratingOpponentEntry.insert(0, ratingOpponent)

                peakRatingOpponentEntry.delete(0, tk.END)
                peakRatingOpponentEntry.insert(0, peakRatingOpponent)

                mainCharacterOpponentEntry.delete(0, tk.END)
                mainCharacterOpponentEntry.insert(0, mainCharacterOpponent)

                mainWeaponOpponentEntry.delete(0, tk.END)
                mainWeaponOpponentEntry.insert(0, mainWeaponOpponent)

            except Exception as e:
                print(e)

        root.after(100, infosBrawlRecuperation)

    window = tk.Tk()

    window.geometry("406x570")
    window.configure(bg="#1F1A1A")

    # FontOfEntryList = tk.font.Font(family="Calibri", size=12)

    canvas = tk.Canvas(
        window,
        bg="#1F1A1A",
        height=570,
        width=406,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    playerNameText = canvas.create_text(
        14.000000000000014,
        165.0,
        anchor="nw",
        text="PlayerName",
        fill="#FFFFFF",
        font=("Roboto", 36 * -1)
    )

    canvas.itemcongig(playerNameText, text="text has changed!")

    canvas.create_rectangle(
        26.000000000000014,
        515.0,
        379.0,
        548.0,
        fill="#000000",
        outline="")

    canvas.create_text(
        39.934211730957045,
        521.0,
        anchor="nw",
        text="Passive / Agressive :",
        fill="#E9EE23",
        font=("Roboto Bold", 18 * -1)
    )

    canvas.create_rectangle(
        26.000000000000014,
        469.0,
        379.0,
        502.0,
        fill="#000000",
        outline="")

    canvas.create_text(
        39.934211730957045,
        475.0,
        anchor="nw",
        text="True Level :",
        fill="#E9EE23",
        font=("Roboto Bold", 18 * -1)
    )

    canvas.create_rectangle(
        26.000000000000014,
        423.0,
        379.0,
        456.0,
        fill="#000000",
        outline="")

    canvas.create_text(
        39.934211730957045,
        429.0,
        anchor="nw",
        text="Level :",
        fill="#E9EE23",
        font=("Roboto Bold", 18 * -1)
    )

    canvas.create_rectangle(
        26.000000000000014,
        377.0,
        379.0,
        410.0,
        fill="#000000",
        outline="")

    canvas.create_text(
        39.934211730957045,
        383.0,
        anchor="nw",
        text="Main Weapon :",
        fill="#E9EE23",
        font=("Roboto Bold", 18 * -1)
    )

    canvas.create_rectangle(
        26.000000000000014,
        331.0,
        379.0,
        364.0,
        fill="#000000",
        outline="")

    canvas.create_text(
        39.934211730957045,
        337.0,
        anchor="nw",
        text="Main Legend :",
        fill="#E9EE23",
        font=("Roboto Bold", 18 * -1)
    )

    canvas.create_rectangle(
        26.000000000000014,
        285.0,
        379.0,
        318.0,
        fill="#000000",
        outline="")

    canvas.create_text(
        39.934211730957045,
        291.0,
        anchor="nw",
        text="Elo Max :",
        fill="#E9EE23",
        font=("Roboto Bold", 18 * -1)
    )

    canvas.create_rectangle(
        26.000000000000014,
        239.0,
        379.0,
        272.0,
        fill="#000000",
        outline="")

    ratingOpponent = tk.StringVar()
    entry_image_ratingOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_ratingOpponent = canvas.create_image(
        298.5,
        252.5,
        image=entry_image_ratingOpponent
    )
    ratingOpponentEntry = ttk.Entry(
        textvariable=ratingOpponent,
        bd=0,
        bg="#000000",
        # disabledbackground="#000000",
        fg="#ffffff",
        # disabledforeground="#ffffff",
        # state="readonly",
        # state="disabled",
        font=("Calibri", 20),
        highlightthickness=0
    )
    ratingOpponentEntry.place(
        x=218.0,
        y=239.0,
        width=161.0,
        height=25.0
    )

    peakRatingOpponent = tk.StringVar()
    entry_image_peakRatingOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_peakRatingOpponent = canvas.create_image(
        298.5,
        298.5,
        image=entry_image_peakRatingOpponent
    )
    peakRatingOpponentEntry = ttk.Entry(
        textvariable=peakRatingOpponent,
        bd=0,
        bg="#000000",
        # disabledbackground="#000000",
        fg="#ffffff",  
        # disabledforeground="#ffffff",
        # state="readonly",
        # state="disabled",
        font=("Calibri", 20),
        highlightthickness=0
    )
    peakRatingOpponentEntry.place(
        x=218.0,
        y=285.0,
        width=161.0,
        height=25.0
    )

    mainCharacterOpponent = tk.StringVar()
    entry_image_mainCharacterOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_mainCharacterOpponent = canvas.create_image(
        298.5,
        344.5,
        image=entry_image_mainCharacterOpponent
    )
    mainCharacterOpponentEntry = ttk.Entry(
        textvariable=mainCharacterOpponent,
        bd=0,
        bg="#000000",
        # disabledbackground="#000000",
        fg="#ffffff",
        # disabledforeground="#ffffff",
        # state="readonly",
        # state="disabled",
        font=("Calibri", 20),
        highlightthickness=0
    )
    mainCharacterOpponentEntry.place(
        x=218.0,
        y=331.0,
        width=161.0,
        height=25.0
    )

    mainWeaponOpponent = tk.StringVar()
    entry_image_mainWeaponOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_mainWeaponOpponent = canvas.create_image(
        298.5,
        390.5,
        image=entry_image_mainWeaponOpponent
    )
    mainWeaponOpponentEntry = ttk.Entry(
        textvariable=mainWeaponOpponent,
        bd=0,
        bg="#000000",
        # disabledbackground="#000000",
        fg="#ffffff",
        # disabledforeground="#ffffff",
        # state="readonly",
        # state="disabled",
        font=("Calibri", 20),
        highlightthickness=0
    )
    mainWeaponOpponentEntry.place(
        x=218.0,
        y=377.0,
        width=161.0,
        height=25.0
    )
    levelOpponent = tk.StringVar()
    entry_image_levelOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_levelOpponent = canvas.create_image(
        298.5,
        436.5,
        image=entry_image_levelOpponent
    )
    levelOpponentEntry = ttk.Entry(
        textvariable=levelOpponent,
        bd=0,
        bg="#000000",
        # disabledbackground="#000000",
        fg="#ffffff",
        # disabledforeground="#ffffff",
        # state="readonly",
        # state="disabled",
        font=("Calibri", 20),
        highlightthickness=0
    )
    levelOpponentEntry.place(
        x=218.0,
        y=423.0,
        width=161.0,
        height=25.0
    )

    trueLevelOpponent = tk.StringVar()
    entry_image_trueLevelOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_trueLevelOpponent = canvas.create_image(
        298.5,
        482.5,
        image=entry_image_trueLevelOpponent
    )
    trueLevelOpponentEntry = ttk.Entry(
        textvariable=trueLevelOpponent,
        bd=0,
        bg="#000000",
        # disabledbackground="#000000",
        fg="#ffffff",
        # disabledforeground="#ffffff",
        # state="readonly",
        # state="disabled",
        font=("Calibri", 20),
        highlightthickness=0
    )
    trueLevelOpponentEntry.place(
        x=218.0,
        y=469.0,
        width=161.0,
        height=25.0
    )


    entry_image_7 = tk.PhotoImage(
        file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(
        298.5,
        528.5,
        image=entry_image_7
    )
    entry_7 = ttk.Entry(
        bd=0,
        bg="#000000",
        highlightthickness=0
    )
    entry_7.place(
        x=218.0,
        y=515.0,
        width=161.0,
        height=25.0
    )

    canvas.create_text(
        39.934211730957045,
        245.0,
        anchor="nw",
        text="Current Elo :",
        fill="#E9EE23",
        font=("Roboto Bold", 18 * -1)
    )

    canvas.create_rectangle(
        325.0,
        14.0,
        385.0,
        74.0,
        fill="#000000",
        outline="")

    button_image_1 = tk.PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = tk.Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=325.0,
        y=14.0,
        width=60.0,
        height=60.0
    )

    canvas.create_rectangle(
        19.000000000000014,
        18.0,
        169.0,
        161.0,
        fill="#837171",
        outline="")

    canvas.create_rectangle(
        14.000000000000014,
        217.0,
        385.0,
        223.0,
        fill="#837171",
        outline="")

    window.resizable(False, False)

    infosBrawlRecuperation()
    window.mainloop()


q = Queue()
t = Thread(target=detect_brawlhalla, args=(q,))

def validateBrawlID():
    t.start()

    global brawlIdClient
    brawlIdClient = brawlID.get()
    # frame.pack_forget()
    root.destroy()
    mainFrame()
    



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

root.mainloop()
# mainFrame = tk.Frame(root)



# characterPlayer = tk.StringVar()
# characterPlayerEntry = ttk.Entry(mainFrame, width = 20, textvariable = characterPlayer)
# characterPlayerEntry.grid(column = 1, row = 0)
# characterPlayerLabel = ttk.Label(mainFrame, width = 20, text = 'Character : ')
# characterPlayerLabel.grid(column = 0, row = 0)

# tagPlayer = tk.StringVar()
# tagPlayerEntry = ttk.Entry(mainFrame, width = 20, textvariable = tagPlayer)
# tagPlayerEntry.grid(column = 1, row = 1)
# tagPlayerLabel = ttk.Label(mainFrame, width = 20, text = 'Tag : ')
# tagPlayerLabel.grid(column = 0, row = 1)

# namePlayer = tk.StringVar()
# namePlayerEntry = ttk.Entry(mainFrame, width = 20, textvariable = namePlayer)
# namePlayerEntry.grid(column = 1, row = 2)
# namePlayerLabel = ttk.Label(mainFrame, width = 20, text = 'Player Name : ')
# namePlayerLabel.grid(column = 0, row = 2)

# clanPlayer = tk.StringVar()
# clanPlayerEntry = ttk.Entry(mainFrame, width = 20, textvariable = clanPlayer)
# clanPlayerEntry.grid(column = 1, row = 3)
# clanPlayerLabel = ttk.Label(mainFrame, width = 20, text = 'Clan : ')
# clanPlayerLabel.grid(column = 0, row = 3)

# # API Infos

# levelPlayer = tk.StringVar()
# levelPlayerEntry = ttk.Entry(mainFrame, width = 20, textvariable = levelPlayer)
# levelPlayerEntry.grid(column = 1, row = 4)
# levelPlayerLabel = ttk.Label(mainFrame, width = 20, text = 'Level : ')
# levelPlayerLabel.grid(column = 0, row = 4)

# ratingPlayer = tk.StringVar()
# ratingPlayerEntry = ttk.Entry(mainFrame, width = 20, textvariable = ratingPlayer)
# ratingPlayerEntry.grid(column = 1, row = 5)
# ratingPlayerLabel = ttk.Label(mainFrame, width = 20, text = 'Rating : ')
# ratingPlayerLabel.grid(column = 0, row = 5)




"""
import tkinter as tk
print("rrs")
root = tk.Tk()
root.minsize(900, 600)
root.geometry("1080x720")
root.title("TWIBOTCH")
root.mainloop()
"""
