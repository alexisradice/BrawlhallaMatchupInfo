import tkinter as tk
import tkinter as ttk
from queue import Queue
from threading import Thread
# from main import detect_brawlhalla
import requests
from pathlib import Path
import os
import cv2
import numpy as np
import pyautogui
import time
import easyocr


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./img/assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# need to run only once to load model into memory
reader = easyocr.Reader(['en'])

dir = os.path.dirname(os.path.abspath(__file__))

def ocr_core(img):
    text = reader.readtext(img, detail=0)
    return text

def get_greyscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


end = False

def detect_brawlhalla(queue=None):

    while not end:
        try:
            ok = False
            pathcodeLoading = dir + "/img/imgLoading.jpg"
            pathcodeBattle = dir + "/img/imgBattle.jpg"

            textarealocation = pyautogui.locateOnScreen(
                pathcodeLoading, confidence=0.9)
            if textarealocation is not None:
                print("Detection OK")
                ok = True
                time.sleep(1)
                image = pyautogui.screenshot()
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                cv2.imwrite(pathcodeBattle, image)

                imgBattle = cv2.imread(pathcodeBattle)
                imgBattle = get_greyscale(imgBattle)

                y = 263
                x = 1208
                h = 80
                w = 280
                start_point = (1200, 264)
                end_point = (1250, 290)
                color = (0, 0, 0)
                thickness = -1
                crop = cv2.rectangle(imgBattle, start_point, end_point, color, thickness)
                crop = imgBattle[y:y + h, x:x + w]
                # crop = cv2.resize(crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

                listInfoPlayer = ocr_core(crop)

                persoPlayer = ""
                tagPlayer = ""
                namePlayer = ""
                clanPlayer = ""

                if (len(listInfoPlayer) == 4):
                    persoPlayer = listInfoPlayer[0].lower().capitalize()
                    tagPlayer = listInfoPlayer[1]
                    namePlayer = listInfoPlayer[2]
                    clanPlayer = listInfoPlayer[3]

                if (len(listInfoPlayer) == 3):
                    persoPlayer = listInfoPlayer[0].lower().capitalize()
                    for i in range(len(listInfoPlayer)):
                        if (listInfoPlayer[2][0] == '<' and listInfoPlayer[2][len(listInfoPlayer[i]) - 1] == '>'):
                            clanPlayer = listInfoPlayer[2]
                            namePlayer = listInfoPlayer[1]
                            tagPlayer = "/"
                        else:
                            tagPlayer = listInfoPlayer[1]
                            namePlayer = listInfoPlayer[2]
                            clanPlayer = "/"

                if (len(listInfoPlayer) == 2):
                    persoPlayer = listInfoPlayer[0].lower().capitalize()
                    namePlayer = listInfoPlayer[1]
                    tagPlayer = "/"
                    clanPlayer = "/"

                print("Character Player: " + persoPlayer + ", Tag Player: " + tagPlayer + ", Name Player: " + namePlayer + ", Clan Player: " + clanPlayer)
                finalList = [persoPlayer, tagPlayer, namePlayer, clanPlayer]

                queue.put(finalList)

                time.sleep(10)
        except Exception as e:
            print(e)
            print("bug main")


brawlIdClient = 0

def mainFrame():

    def infosBrawlRecuperation():

        if not q.empty():
            finalList = q.get()
            # print(finalList)


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
                mainCharacterOpponent = apiResult['playerOtherJSON']['mainCharacter']
                mainWeaponOpponent = apiResult['playerOtherJSON']['mainWeapon']
                trueLevelOpponent = apiResult['playerOtherJSON']['trueLevel']
                passiveAgressiveOpponent = apiResult['playerOtherJSON']['passiveAgressive']

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

                trueLevelOpponentEntry.delete(0, tk.END)
                trueLevelOpponentEntry.insert(0, trueLevelOpponent)

                passiveAgressiveOpponentEntry.delete(0, tk.END)
                passiveAgressiveOpponentEntry.insert(0, passiveAgressiveOpponent)

            except Exception as e:
                print(e)

        root.after(100, infosBrawlRecuperation)

    window = tk.Tk()

    window.geometry("406x570")
    window.title("Brawlhalla Matchup Infos")
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

    # canvas.itemcongig(playerNameText, text="text has changed!")

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
        226.5,
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
        x=146.0,
        y=242.0,
        width=161.0,
        height=25.0
    )

    peakRatingOpponent = tk.StringVar()
    entry_image_peakRatingOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_peakRatingOpponent = canvas.create_image(
        200.5,
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
        x=120.00000000000001,
        y=288.0,
        width=161.0,
        height=25.0
    )

    mainCharacterOpponent = tk.StringVar()
    entry_image_mainCharacterOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_mainCharacterOpponent = canvas.create_image(
        241.5,
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
        x=161.0,
        y=334.0,
        width=161.0,
        height=25.0
    )

    mainWeaponOpponent = tk.StringVar()
    entry_image_mainWeaponOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_mainWeaponOpponent = canvas.create_image(
        247.5,
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
        x=167.0,
        y=380.0,
        width=161.0,
        height=25.0
    )
    levelOpponent = tk.StringVar()
    entry_image_levelOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_levelOpponent = canvas.create_image(
        180.5,
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
        x=100.00000000000001,
        y=426.0,
        width=161.0,
        height=25.0
    )

    trueLevelOpponent = tk.StringVar()
    entry_image_trueLevelOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_trueLevelOpponent = canvas.create_image(
        222.5,
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
        x=142.0,
        y=472.0,
        width=161.0,
        height=25.0
    )

    passiveAgressiveOpponent = tk.StringVar()
    entry_image_passiveAgressiveOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_7.png"))
    entry_bg_passiveAgressiveOpponent = canvas.create_image(
        295.5,
        528.5,
        image=entry_image_passiveAgressiveOpponent
    )
    passiveAgressiveOpponentEntry = ttk.Entry(
        textvariable=passiveAgressiveOpponent,
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
    passiveAgressiveOpponentEntry.place(
        x=215.0,
        y=518.0,
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
    global end
    end = True

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
root.title('Brawlhalla Matchup Infos')
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

