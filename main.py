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

                linkAPI = "http://localhost:8080/api/brawl/{}&{}".format(
                    finalList[2], brawlIdClient)
                response = requests.get(linkAPI)
                apiResult = response.json()

                levelOpponent = apiResult['statsOpponentJSON']['level']
                ratingOpponent = apiResult['infosOpponentJSON']['rating']
                peakRatingOpponent = apiResult['infosOpponentJSON']['peak_rating']
                mainLevelCharacterOpponent = apiResult['miscOpponentJSON']['mainLevelCharacter']
                mainRankedCharacterOpponent = apiResult['miscOpponentJSON']['mainRankedCharacter']
                pictureMainRankedCharacterOpponent = apiResult['miscOpponentJSON']['pictureMainRankedCharacter']
                mainWeaponOpponent = apiResult['miscOpponentJSON']['mainWeapon']
                trueLevelOpponent = apiResult['miscOpponentJSON']['trueLevel']
                passiveAgressiveOpponent = apiResult['miscOpponentJSON']['passiveAgressive']
                timePlayedOpponent = apiResult['miscOpponentJSON']['timePlayed']

                levelClient = apiResult['statsClientJSON']['level']
                ratingClient = apiResult['rankedClientJSON']['rating']
                peakRatingClient = apiResult['rankedClientJSON']['peak_rating']
                mainLevelCharacterClient = apiResult['miscClientJSON']['mainLevelCharacter']
                mainRankedCharacterClient = apiResult['miscClientJSON']['mainRankedCharacter']
                pictureMainRankedCharacter = apiResult['miscClientJSON']['pictureMainRankedCharacter']
                mainWeaponClient = apiResult['miscClientJSON']['mainWeapon']
                trueLevelClient = apiResult['miscClientJSON']['trueLevel']
                passiveAgressiveClient = apiResult['miscClientJSON']['passiveAgressive']
                timePlayedClient = apiResult['miscClientJSON']['timePlayed']
                

                levelOpponentEntry.delete(0, tk.END)
                levelOpponentEntry.insert(0, levelOpponent)

                ratingOpponentEntry.delete(0, tk.END)
                ratingOpponentEntry.insert(0, ratingOpponent)

                peakRatingOpponentEntry.delete(0, tk.END)
                peakRatingOpponentEntry.insert(0, peakRatingOpponent)

                mainLevelCharacterOpponentEntry.delete(0, tk.END)
                mainLevelCharacterOpponentEntry.insert(0, mainLevelCharacterOpponent)

                mainRankedCharacterOpponentEntry.delete(0, tk.END)
                mainRankedCharacterOpponentEntry.insert(0, mainRankedCharacterOpponent)

                # pictureMainRankedCharacterOpponentEntry.delete(0, tk.END)
                # pictureMainRankedCharacterOpponentEntry.insert(0, pictureMainRankedCharacterOpponent)

                mainWeaponOpponentEntry.delete(0, tk.END)
                mainWeaponOpponentEntry.insert(0, mainWeaponOpponent)

                trueLevelOpponentEntry.delete(0, tk.END)
                trueLevelOpponentEntry.insert(0, trueLevelOpponent)

                passiveAgressiveOpponentEntry.delete(0, tk.END)
                passiveAgressiveOpponentEntry.insert(0, passiveAgressiveOpponent)

                timePlayedOpponentEntry.delete(0, tk.END)
                timePlayedOpponentEntry.insert(0, timePlayedOpponent)

            except Exception as e:
                print(e)

        root.after(100, infosBrawlRecuperation)

    window = tk.Tk()

    window.geometry("405x660")
    window.title("Brawlhalla Matchup Infos v1")
    window.configure(bg="#1F1A1A")

    # FontOfEntryList = tk.font.Font(family="Calibri", size=12)

    canvas = tk.Canvas(
    window,
    bg = "#1F1A1A",
    height = 660,
    width = 405,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        26.000000000000014,
        239.0,
        379.0,
        272.0,
        fill="#000000",
        width=2,
        outline="#847171")

    canvas.create_rectangle(
        26.000000000000014,
        285.0,
        379.0,
        318.0,
        fill="#000000",
        width=2,
        outline="#847171")

    canvas.create_rectangle(
        26.000000000000014,
        331.0,
        379.0,
        364.0,
        fill="#000000",
        width=2,
        outline="#847171")

    canvas.create_rectangle(
        26.000000000000014,
        377.0,
        379.0,
        410.0,
        fill="#000000",
        width=2,
        outline="#847171")

    canvas.create_rectangle(
        26.000000000000014,
        423.0,
        379.0,
        456.0,
        fill="#000000",
        width=2,
        outline="#847171")

    canvas.create_rectangle(
        26.000000000000014,
        469.0,
        379.0,
        502.0,
        fill="#000000",
        width=2,
        outline="#847171")

    canvas.create_rectangle(
        26.000000000000014,
        515.0,
        379.0,
        548.0,
        fill="#000000",
        width=2,
        outline="#847171")

    canvas.create_rectangle(
        26.000000000000014,
        561.0,
        379.0,
        594.0,
        fill="#000000",
        width=2,
        outline="#847171")

    canvas.create_rectangle(
        26.000000000000014,
        607.0,
        379.0,
        640.0,
        fill="#000000",
        width=2,
        outline="#847171")

    canvas.create_text(
        40.000000000000014,
        244.0,
        anchor="nw",
        text="Current Elo :",
        fill="#E9EE23",
        font=("ITCErasStd-Ultra", 18 * -1)
    )

    canvas.create_text(
        40.000000000000014,
        290.0,
        anchor="nw",
        text="Elo Max :",
        fill="#E9EE23",
        font=("ITCErasStd-Ultra", 18 * -1)
    )

    canvas.create_text(
        40.000000000000014,
        336.0,
        anchor="nw",
        text="Main Legend :",
        fill="#E9EE23",
        font=("ITCErasStd-Ultra", 18 * -1)
    )

    canvas.create_text(
        40.000000000000014,
        382.0,
        anchor="nw",
        text="Main Weapon :",
        fill="#E9EE23",
        font=("ITCErasStd-Ultra", 18 * -1)
    )

    canvas.create_text(
        40.000000000000014,
        428.0,
        anchor="nw",
        text="Level :",
        fill="#E9EE23",
        font=("ITCErasStd-Ultra", 18 * -1)
    )

    canvas.create_text(
        40.000000000000014,
        474.0,
        anchor="nw",
        text="True Level :",
        fill="#E9EE23",
        font=("ITCErasStd-Ultra", 18 * -1)
    )

    canvas.create_text(
        40.000000000000014,
        514.0,
        anchor="nw",
        text="Most Rated ",
        fill="#E9EE23",
        font=("ITCErasStd-Ultra", 18 * -1)
    )

    canvas.create_text(
        40.000000000000014,
        529.0,
        anchor="nw",
        text="Legend :",
        fill="#E9EE23",
        font=("ITCErasStd-Ultra", 18 * -1)
    )

    canvas.create_text(
        40.000000000000014,
        566.0,
        anchor="nw",
        text="Time Played :",
        fill="#E9EE23",
        font=("ITCErasStd-Ultra", 18 * -1)
    )

    canvas.create_text(
        39.934211730957045,
        605.0,
        anchor="nw",
        text="Passive / ",
        fill="#E9EE23",
        font=("ITCErasStd-Ultra", 18 * -1)
    )

    canvas.create_text(
        40.000000000000014,
        619.0,
        anchor="nw",
        text="Agressive :",
        fill="#E9EE23",
        font=("ITCErasStd-Ultra", 18 * -1)
    )












    ratingOpponent = tk.StringVar()
    entry_image_ratingOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_ratingOpponent = canvas.create_image(
        275.0,
        254.5,
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
        font=("ITCErasStd-Ultra", 18 * -1),
        highlightthickness=0
    )
    ratingOpponentEntry.place(
    x=174.0,
    y=241.0,
    width=202.0,
    height=25.0
    )

    peakRatingOpponent = tk.StringVar()
    entry_image_peakRatingOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_peakRatingOpponent = canvas.create_image(
        259.0,
        300.5,
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
        font=("ITCErasStd-Ultra", 18 * -1),
        highlightthickness=0
    )
    peakRatingOpponentEntry.place(
        x=142.0,
        y=287.0,
        width=234.0,
        height=25.0
    )

    mainLevelCharacterOpponent = tk.StringVar()
    entry_image_mainLevelCharacterOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_mainLevelCharacterOpponent = canvas.create_image(
        281.5,
        346.5,
        image=entry_image_mainLevelCharacterOpponent
    )
    mainLevelCharacterOpponentEntry = ttk.Entry(
        textvariable=mainLevelCharacterOpponent,
        bd=0,
        bg="#000000",
        # disabledbackground="#000000",
        fg="#ffffff",
        # disabledforeground="#ffffff",
        # state="readonly",
        # state="disabled",
        font=("ITCErasStd-Ultra", 18 * -1),
        highlightthickness=0
    )
    mainLevelCharacterOpponentEntry.place(
        x=187.0,
        y=333.0,
        width=189.0,
        height=25.0
    )

    mainWeaponOpponent = tk.StringVar()
    entry_image_mainWeaponOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_mainWeaponOpponent = canvas.create_image(
        285.0,
        392.5,
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
        font=("ITCErasStd-Ultra", 18 * -1),
        highlightthickness=0
    )
    mainWeaponOpponentEntry.place(
        x=194.0,
        y=379.0,
        width=182.0,
        height=25.0
    )
    levelOpponent = tk.StringVar()
    entry_image_levelOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_levelOpponent = canvas.create_image(
        244.5,
        438.5,
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
        font=("ITCErasStd-Ultra", 18 * -1),
        highlightthickness=0
    )
    levelOpponentEntry.place(
        x=113.00000000000001,
        y=425.0,
        width=263.0,
        height=25.0
    )

    trueLevelOpponent = tk.StringVar()
    entry_image_trueLevelOpponent = tk.PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_trueLevelOpponent = canvas.create_image(
        270.0,
        484.5,
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
        font=("ITCErasStd-Ultra", 18 * -1),
        highlightthickness=0
    )
    trueLevelOpponentEntry.place(
        x=164.0,
        y=471.0,
        width=212.0,
        height=25.0
    )

    mainRankedCharacterOpponent = tk.StringVar()
    entry_image_mainRankedCharacterOpponent = tk.PhotoImage(file=relative_to_assets("entry_7.png"))
    entry_bg_mainRankedCharacterOpponent = canvas.create_image(
        270.0,
        530.5,
        image=entry_image_mainRankedCharacterOpponent
    )
    mainRankedCharacterOpponentEntry = ttk.Entry(
        textvariable=mainRankedCharacterOpponent,
        bd=0,
        bg="#000000",
        # disabledbackground="#000000",
        fg="#ffffff",
        # disabledforeground="#ffffff",
        # state="readonly",
        # state="disabled",
        font=("ITCErasStd-Ultra", 18 * -1),
        highlightthickness=0
    )
    mainRankedCharacterOpponentEntry.place(
        x=164.0,
        y=517.0,
        width=212.0,
        height=25.0
    )
    
    timePlayedOpponent = tk.StringVar()
    entry_image_timePlayedOpponent = tk.PhotoImage(
    file=relative_to_assets("entry_8.png"))
    entry_bg_timePlayedOpponent = canvas.create_image(
        278.0,
        576.5,
    image=entry_image_timePlayedOpponent
    )
    timePlayedOpponentEntry = ttk.Entry(
        textvariable=timePlayedOpponent,
        bd=0,
        bg="#000000",
        # disabledbackground="#000000",
        fg="#ffffff",
        # disabledforeground="#ffffff",
        # state="readonly",
        # state="disabled",
        font=("ITCErasStd-Ultra", 18 * -1),
        highlightthickness=0
    )
    timePlayedOpponentEntry.place(
        x=180.0,
        y=563.0,
        width=196.0,
        height=25.0
    )

    passiveAgressiveOpponent = tk.StringVar()
    entry_image_passiveAgressiveOpponent = tk.PhotoImage(file=relative_to_assets("entry_9.png"))
    entry_bg_passiveAgressiveOpponent = canvas.create_image(
        265.0,
        622.5,
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
        font=("ITCErasStd-Ultra", 18 * -1),
        highlightthickness=0
    )
    passiveAgressiveOpponentEntry.place(
        x=154.0,
        y=609.0,
        width=222.0,
        height=25.0
    )










    canvas.create_rectangle(
        14.000000000000014,
        217.0,
        385.0,
        223.0,
        fill="#837171",
        outline="#847171")

    canvas.create_text(
        14.000000000000014,
        171.0,
        anchor="nw",
        text="PlayerName",
        fill="#FFFFFF",
        font=("ITCErasStd-Ultra", 36 * -1)
    )

    canvas.create_rectangle(
        325.0,
        14.0,
        385.0,
        74.0,
        fill="#201B1B",
        outline="#847171")

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
        outline="#847171")

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
root.title('Brawlhalla Matchup Infos v1')
root.geometry("410x150")

# frame = ttk.Frame(root)
# frame.pack()

canvas = tk.Canvas(
    root,
    bg = "#201B1B",
    height = 150,
    width = 410,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

brawlID = tk.StringVar()
canvas.place(x = 0, y = 0)
entry_image_brawlID = tk.PhotoImage(
    file=relative_to_assets("entry_0.png"))
entry_bg_brawlID = canvas.create_image(
    205.0,
    75.5,
    image=entry_image_brawlID
)
brawlIDEntry = ttk.Entry(
    textvariable = brawlID,
    bd=0,
    bg="#000000",
    # disabledbackground="#000000",
    fg="#ffffff",
    # disabledforeground="#ffffff",
    # state="readonly",
    # state="disabled",
    font=("ITCErasStd-Ultra", 40 * -1),
    justify='center',
    highlightthickness=0
)
brawlIDEntry.place(
    x=67.0,
    y=55.0,
    width=276.0,
    height=43.0
)

canvas.create_rectangle(
    155.0,
    114.0,
    255.0,
    140.0,
    fill="#201B1B",
    outline="")


button_1 = tk.Button(
    # image=button_image_0,
    borderwidth=0,
    highlightthickness=0,
    command = validateBrawlID,
    relief="flat",
    text = "Validate",
    font=("ITCErasStd-Ultra", 24 * -1)
)
button_1.place(
    x=150.0,
    y=114.0,
    width=110.0,
    height=26.0
)

canvas.create_text(
    31.999999999999996,
    14.0,
    anchor="nw",
    text="Enter your Brawlhalla ID :",
    fill="#FFFFFF",
    font=("ITCErasStd-Ultra", 24 * -1)
)
root.resizable(False, False)
root.mainloop()


# characterPlayer = tk.StringVar()
# brawlIDLabel = ttk.Label(frame, width = 20, text = 'Enter your Brawlhalla ID : ')
# brawlIDLabel.grid(column = 0, row = 0)
# brawlID = tk.StringVar()
# brawlIDEntry = ttk.Entry(frame, width = 20, textvariable = brawlID)
# brawlIDEntry.grid(column = 0, row = 1)
# validateButton = ttk.Button(frame, width = 20, text = 'Validate', command = validateBrawlID)
# validateButton.grid(column = 0, row = 2)

# root.mainloop()

