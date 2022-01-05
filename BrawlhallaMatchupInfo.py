import tkinter as tk
import tkinter as ttk
from queue import Queue
from threading import Thread
import requests
from pathlib import Path
import easyocr
import os
import cv2
import numpy as np
import pyautogui
import time
from io import BytesIO
from PIL import ImageTk, Image
import ssl
import urllib.request
import json
from dotenv import load_dotenv
import shutil

load_dotenv()
API_LINK = os.environ.get("API_LINK")

playerNameClient = ""
levelClient = ""
regionClient = ""
ratingClient = ""
peakRatingClient = ""
globalRankClient = ""
regionRankClient = ""
mainLevelCharacterClient = ""
mainRankedCharacterClient = ""
pictureMainRankedCharacterClient = ""
mainWeaponClient = ""
trueLevelClient = ""
passiveAgressiveClient = ""
timePlayedClient = ""

playerNameOpponent = ""
levelOpponent = ""
regionOpponent = ""
ratingOpponent = ""
globalRankOpponent = ""
regionRankOpponent = ""
peakRatingOpponent = ""
mainLevelCharacterOpponent = ""
mainRankedCharacterOpponent = ""
pictureMainRankedCharacterOpponent = ""
pictureMainLevelCharacterOpponent = ""
mainWeaponOpponent = ""
trueLevelOpponent = ""
passiveAgressiveOpponent = ""
timePlayedOpponent = ""

pictureCharacterOpponent = None
pictureCharacterClient = None
firstLaunch = True
switchProfileBool = False

dir = os.path.dirname(os.path.abspath(__file__))

response = requests.get(API_LINK + "/api/brawl/img/imgLoading")
file = open(dir + "/img/imgLoading.jpg", "wb")
file.write(response.content)
file.close()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./img/assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



# need to run only once to load model into memory
reader = easyocr.Reader(['en'])

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
                time.sleep(2)
                image = pyautogui.screenshot()
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                cv2.imwrite(pathcodeBattle, image)

                imgBattle = cv2.imread(pathcodeBattle)
                imgBattle = get_greyscale(imgBattle)

                y = 300
                x = 950
                h = 80
                w = 800
                start_point = (1200, 264)
                end_point = (1250, 290)
                color = (0, 0, 0)
                thickness = -1
                crop = cv2.rectangle(imgBattle, start_point, end_point, color, thickness)
                crop = imgBattle[y:y + h, x:x + w]

                listInfoPlayer = ocr_core(crop)
                print(listInfoPlayer)

                persoPlayer = ""
                tagPlayer = ""
                namePlayer = ""
                clanPlayer = ""
                clanFounded = False

                for i in range(len(listInfoPlayer)):
                    if (listInfoPlayer[i][0] == '<' or listInfoPlayer[i][len(listInfoPlayer[i]) - 1] == '>'):
                        namePlayer = listInfoPlayer[i-1]
                        clanFounded = True



                if (clanFounded == False):
                    namePlayer = listInfoPlayer[len(listInfoPlayer) - 1]

                '''
                if (len(listInfoPlayer) == 5):
                    persoPlayer = listInfoPlayer[0].lower().capitalize()
                    tagPlayer = listInfoPlayer[1]
                    namePlayer = listInfoPlayer[2] + " | " +listInfoPlayer[3]
                    clanPlayer = listInfoPlayer[4]

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
                '''
                # print("Character Player: " + persoPlayer + ", Tag Player: " + tagPlayer + ", Name Player: " + namePlayer + ", Clan Player: " + clanPlayer)
                print("Name Player: " + namePlayer)
                finalList = [persoPlayer, tagPlayer, namePlayer, clanPlayer]

                queue.put(finalList)

                time.sleep(10)
        except Exception as e:
            print(e)


brawlIdClient = 0


def mainFrame():


    def switchProfile(origin):

        global switchProfileBool

        if (origin == "client"):
            switchProfileBool = True

        elif (origin == "opponent"):
            switchProfileBool = False
            switchPlayerButton["state"] = "active"
            switchPlayerButton["image"] = button_image_switchPlayer

        elif (origin == "command"):
            if (playerNamePlayerLabel.cget("text") == playerNameClient):
                switchProfileBool = False
            else:
                switchProfileBool = True


        if (switchProfileBool == True):

            picture["image"] = pictureCharacterClient
            picture.image = pictureCharacterClient

            playerNamePlayerLabel["text"] = playerNameClient
            globalRankPlayerLabel["text"] = "#" + str(globalRankClient)
            regionRankPlayerLabel["text"] = "#" + str(regionRankClient)
            regionRankPlayerTitleLabel["text"] = regionClient + " Rank :"

            levelPlayerEntry["state"] = "normal"
            levelPlayerEntry.delete(0, tk.END)
            levelPlayerEntry.insert(0, levelClient)
            levelPlayerEntry["state"] = "disabled"

            ratingPlayerEntry["state"] = "normal"
            ratingPlayerEntry.delete(0, tk.END)
            ratingPlayerEntry.insert(0, ratingClient)
            ratingPlayerEntry["state"] = "disabled"

            peakRatingPlayerEntry["state"] = "normal"
            peakRatingPlayerEntry.delete(0, tk.END)
            peakRatingPlayerEntry.insert(0, peakRatingClient)
            peakRatingPlayerEntry["state"] = "disabled"

            mainLevelCharacterPlayerEntry["state"] = "normal"
            mainLevelCharacterPlayerEntry.delete(0, tk.END)
            mainLevelCharacterPlayerEntry.insert(0, mainLevelCharacterClient)
            mainLevelCharacterPlayerEntry["state"] = "disabled"

            mainRankedCharacterPlayerEntry["state"] = "normal"
            mainRankedCharacterPlayerEntry.delete(0, tk.END)
            mainRankedCharacterPlayerEntry.insert(0, mainRankedCharacterClient)
            mainRankedCharacterPlayerEntry["state"] = "disabled"

            mainWeaponPlayerEntry["state"] = "normal"
            mainWeaponPlayerEntry.delete(0, tk.END)
            mainWeaponPlayerEntry.insert(0, mainWeaponClient)
            mainWeaponPlayerEntry["state"] = "disabled"

            trueLevelPlayerEntry["state"] = "normal"
            trueLevelPlayerEntry.delete(0, tk.END)
            trueLevelPlayerEntry.insert(0, trueLevelClient)
            trueLevelPlayerEntry["state"] = "disabled"

            passiveAgressivePlayerEntry["state"] = "normal"
            passiveAgressivePlayerEntry.delete(0, tk.END)
            passiveAgressivePlayerEntry.insert(0, passiveAgressiveClient)
            passiveAgressivePlayerEntry["state"] = "disabled"

            timePlayedPlayerEntry["state"] = "normal"
            timePlayedPlayerEntry.delete(0, tk.END)
            timePlayedPlayerEntry.insert(0, timePlayedClient)
            timePlayedPlayerEntry["state"] = "disabled"



        else:

            picture["image"] = pictureCharacterOpponent
            picture.image = pictureCharacterOpponent

            playerNamePlayerLabel["text"] = playerNameOpponent
            globalRankPlayerLabel["text"] = "#" + str(globalRankOpponent)
            regionRankPlayerLabel["text"] = "#" + str(regionRankOpponent)
            regionRankPlayerTitleLabel["text"] = regionOpponent + " Rank :"

            levelPlayerEntry["state"] = "normal"
            levelPlayerEntry.delete(0, tk.END)
            levelPlayerEntry.insert(0, levelOpponent)
            levelPlayerEntry["state"] = "disabled"

            ratingPlayerEntry["state"] = "normal"
            ratingPlayerEntry.delete(0, tk.END)
            ratingPlayerEntry.insert(0, ratingOpponent)
            ratingPlayerEntry["state"] = "disabled"

            peakRatingPlayerEntry["state"] = "normal"
            peakRatingPlayerEntry.delete(0, tk.END)
            peakRatingPlayerEntry.insert(0, peakRatingOpponent)
            peakRatingPlayerEntry["state"] = "disabled"

            mainLevelCharacterPlayerEntry["state"] = "normal"
            mainLevelCharacterPlayerEntry.delete(0, tk.END)
            mainLevelCharacterPlayerEntry.insert(0, mainLevelCharacterOpponent)
            mainLevelCharacterPlayerEntry["state"] = "disabled"

            mainRankedCharacterPlayerEntry["state"] = "normal"
            mainRankedCharacterPlayerEntry.delete(0, tk.END)
            mainRankedCharacterPlayerEntry.insert(0, mainRankedCharacterOpponent)
            mainRankedCharacterPlayerEntry["state"] = "disabled"

            mainWeaponPlayerEntry["state"] = "normal"
            mainWeaponPlayerEntry.delete(0, tk.END)
            mainWeaponPlayerEntry.insert(0, mainWeaponOpponent)
            mainWeaponPlayerEntry["state"] = "disabled"

            trueLevelPlayerEntry["state"] = "normal"
            trueLevelPlayerEntry.delete(0, tk.END)
            trueLevelPlayerEntry.insert(0, trueLevelOpponent)
            trueLevelPlayerEntry["state"] = "disabled"

            passiveAgressivePlayerEntry["state"] = "normal"
            passiveAgressivePlayerEntry.delete(0, tk.END)
            passiveAgressivePlayerEntry.insert(0, passiveAgressiveOpponent)
            passiveAgressivePlayerEntry["state"] = "disabled"

            timePlayedPlayerEntry["state"] = "normal"
            timePlayedPlayerEntry.delete(0, tk.END)
            timePlayedPlayerEntry.insert(0, timePlayedOpponent)
            timePlayedPlayerEntry["state"] = "disabled"



    def clientInfo():

        linkAPI = API_LINK + "/api/brawl/client/{}".format(brawlIdClient)
        response = requests.get(linkAPI)
        apiResult = response.json()

        global playerNameClient
        playerNameClient = apiResult['dataClientJSON']['playerName']
        global regionClient
        regionClient = apiResult['dataClientJSON']['region']
        global levelClient
        levelClient = apiResult['dataClientJSON']['level']
        global ratingClient
        ratingClient = apiResult['dataClientJSON']['rating']
        global peakRatingClient
        peakRatingClient = apiResult['dataClientJSON']['peakRating']
        global globalRankClient
        globalRankClient = apiResult['dataClientJSON']['globalRank']
        global regionRankClient
        regionRankClient = apiResult['dataClientJSON']['regionRank']
        global mainLevelCharacterClient
        mainLevelCharacterClient = apiResult['dataClientJSON']['mainLevelCharacter']
        global mainRankedCharacterClient
        mainRankedCharacterClient = apiResult['dataClientJSON']['mainRankedCharacter']
        global pictureMainRankedCharacterClient
        pictureMainRankedCharacterClient = apiResult['dataClientJSON']['pictureMainRankedCharacter']
        global mainWeaponClient
        mainWeaponClient = apiResult['dataClientJSON']['mainWeapon']
        global trueLevelClient
        trueLevelClient = apiResult['dataClientJSON']['trueLevel']
        global passiveAgressiveClient
        passiveAgressiveClient = apiResult['dataClientJSON']['passiveAgressive']
        global timePlayedClient
        timePlayedClient = apiResult['dataClientJSON']['timePlayed']

        try:
            URL = pictureMainRankedCharacterClient.split()[0] + "_" + pictureMainRankedCharacterClient.split()[1]
        except:
            URL = pictureMainRankedCharacterClient

        context = ssl._create_unverified_context()
        u = urllib.request.urlopen(URL, context=context)
        raw_data = u.read()
        u.close()

        im = Image.open(BytesIO(raw_data))
        im = im.resize((150,150),Image.ANTIALIAS)
        global pictureCharacterClient
        pictureCharacterClient = ImageTk.PhotoImage(im)

        switchProfile("client")



    def infosBrawlRecuperation():

        if not q.empty():
            finalList = q.get()


            q.task_done()

            try:

                linkAPI = API_LINK + "/api/brawl/opponent/{}&{}&{}".format(
                    finalList[2], ratingClient, regionClient)
                response = requests.get(linkAPI)
                apiResult = response.json()

                global playerNameOpponent
                playerNameOpponent = apiResult['dataOpponentJSON']['playerName']
                global levelOpponent
                levelOpponent = apiResult['dataOpponentJSON']['level']
                global regionOpponent
                regionOpponent = apiResult['dataOpponentJSON']['region']
                global ratingOpponent
                ratingOpponent = apiResult['dataOpponentJSON']['rating']
                global peakRatingOpponent
                peakRatingOpponent = apiResult['dataOpponentJSON']['peakRating']
                global globalRankOpponent
                globalRankOpponent = apiResult['dataOpponentJSON']['globalRank']
                global regionRankOpponent
                regionRankOpponent = apiResult['dataOpponentJSON']['regionRank']
                global mainLevelCharacterOpponent
                mainLevelCharacterOpponent = apiResult['dataOpponentJSON']['mainLevelCharacter']
                global mainRankedCharacterOpponent
                mainRankedCharacterOpponent = apiResult['dataOpponentJSON']['mainRankedCharacter']
                global pictureMainRankedCharacterOpponent
                pictureMainRankedCharacterOpponent = apiResult['dataOpponentJSON']['pictureMainRankedCharacter']
                global pictureMainLevelCharacterOpponent
                pictureMainLevelCharacterOpponent = apiResult['dataOpponentJSON']['pictureMainLevelCharacter']
                global mainWeaponOpponent
                mainWeaponOpponent = apiResult['dataOpponentJSON']['mainWeapon']
                global trueLevelOpponent
                trueLevelOpponent = apiResult['dataOpponentJSON']['trueLevel']
                global passiveAgressiveOpponent
                passiveAgressiveOpponent = apiResult['dataOpponentJSON']['passiveAgressive']
                global timePlayedOpponent
                timePlayedOpponent = apiResult['dataOpponentJSON']['timePlayed']

                global switchProfileBool
                switchProfileBool = False

                try:
                    URL = pictureMainLevelCharacterOpponent.split()[0] + "_" + pictureMainLevelCharacterOpponent.split()[1]
                except:
                    URL = pictureMainLevelCharacterOpponent

                context = ssl._create_unverified_context()
                u = urllib.request.urlopen(URL, context=context)
                raw_data = u.read()
                u.close()

                im = Image.open(BytesIO(raw_data))
                im = im.resize((150,150),Image.ANTIALIAS)
                global pictureCharacterOpponent
                pictureCharacterOpponent = ImageTk.PhotoImage(im)

                switchProfile("opponent")
                

            except Exception as e:
                print(e)

        root.after(100, infosBrawlRecuperation)


    window = tk.Tk()

    window.geometry("405x660")
    window.title("Brawlhalla Matchup Info v1")
    window.iconbitmap(dir + "/img/azoth.ico")
    window.configure(bg="#1F1A1A")


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






    #image=photo,
    picture = tk.Label(image="", compound="c",bg="#000000" )
    # picture.image = photo
    picture.place(
    x=15.0,
    y=15.0,
    width=154,
    height=154
    )




    ratingPlayer = tk.StringVar()
    entry_image_ratingPlayer = tk.PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_ratingPlayer = canvas.create_image(
        275.0,
        254.5,
        image=entry_image_ratingPlayer
    )
    ratingPlayerEntry = ttk.Entry(
        textvariable=ratingPlayer,
        bd=0,
        bg="#000000",
        disabledbackground="#000000",
        fg="#ffffff",
        disabledforeground="#ffffff",
        state="disabled",
        font=("ITCErasStd-Ultra", 20 * -1),
        highlightthickness=0
    )
    ratingPlayerEntry.place(
    x=174.0,
    y=244.0,
    width=202.0,
    height=25.0
    )

    peakRatingPlayer = tk.StringVar()
    entry_image_peakRatingPlayer = tk.PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_peakRatingPlayer = canvas.create_image(
        259.0,
        300.5,
        image=entry_image_peakRatingPlayer
    )
    peakRatingPlayerEntry = ttk.Entry(
        textvariable=peakRatingPlayer,
        bd=0,
        bg="#000000",
        disabledbackground="#000000",
        fg="#ffffff",
        disabledforeground="#ffffff",
        state="disabled",
        font=("ITCErasStd-Ultra", 20 * -1),
        highlightthickness=0
    )
    peakRatingPlayerEntry.place(
        x=142.0,
        y=290.0,
        width=234.0,
        height=25.0
    )

    mainLevelCharacterPlayer = tk.StringVar()
    entry_image_mainLevelCharacterPlayer = tk.PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_mainLevelCharacterPlayer = canvas.create_image(
        281.5,
        346.5,
        image=entry_image_mainLevelCharacterPlayer
    )
    mainLevelCharacterPlayerEntry = ttk.Entry(
        textvariable=mainLevelCharacterPlayer,
        bd=0,
        bg="#000000",
        disabledbackground="#000000",
        fg="#ffffff",
        disabledforeground="#ffffff",
        state="disabled",
        font=("ITCErasStd-Ultra", 20 * -1),
        highlightthickness=0
    )
    mainLevelCharacterPlayerEntry.place(
        x=187.0,
        y=336.0,
        width=189.0,
        height=25.0
    )

    mainWeaponPlayer = tk.StringVar()
    entry_image_mainWeaponPlayer = tk.PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_mainWeaponPlayer = canvas.create_image(
        285.0,
        392.5,
        image=entry_image_mainWeaponPlayer
    )
    mainWeaponPlayerEntry = ttk.Entry(
        textvariable=mainWeaponPlayer,
        bd=0,
        bg="#000000",
        disabledbackground="#000000",
        fg="#ffffff",
        disabledforeground="#ffffff",
        state="disabled",
        font=("ITCErasStd-Ultra", 20 * -1),
        highlightthickness=0
    )
    mainWeaponPlayerEntry.place(
        x=194.0,
        y=382.0,
        width=182.0,
        height=25.0
    )
    levelPlayer = tk.StringVar()
    entry_image_levelPlayer = tk.PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_levelPlayer = canvas.create_image(
        244.5,
        438.5,
        image=entry_image_levelPlayer
    )
    levelPlayerEntry = ttk.Entry(
        textvariable=levelPlayer,
        bd=0,
        bg="#000000",
        disabledbackground="#000000",
        fg="#ffffff",
        disabledforeground="#ffffff",
        state="disabled",
        font=("ITCErasStd-Ultra", 20 * -1),
        highlightthickness=0
    )
    levelPlayerEntry.place(
        x=113.00000000000001,
        y=428.0,
        width=263.0,
        height=25.0
    )

    trueLevelPlayer = tk.StringVar()
    entry_image_trueLevelPlayer = tk.PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_trueLevelPlayer = canvas.create_image(
        270.0,
        484.5,
        image=entry_image_trueLevelPlayer
    )
    trueLevelPlayerEntry = ttk.Entry(
        textvariable=trueLevelPlayer,
        bd=0,
        bg="#000000",
        disabledbackground="#000000",
        fg="#ffffff",
        disabledforeground="#ffffff",
        state="disabled",
        font=("ITCErasStd-Ultra", 20 * -1),
        highlightthickness=0
    )
    trueLevelPlayerEntry.place(
        x=164.0,
        y=474.0,
        width=212.0,
        height=25.0
    )

    mainRankedCharacterPlayer = tk.StringVar()
    entry_image_mainRankedCharacterPlayer = tk.PhotoImage(file=relative_to_assets("entry_7.png"))
    entry_bg_mainRankedCharacterPlayer = canvas.create_image(
        270.0,
        530.5,
        image=entry_image_mainRankedCharacterPlayer
    )
    mainRankedCharacterPlayerEntry = ttk.Entry(
        textvariable=mainRankedCharacterPlayer,
        bd=0,
        bg="#000000",
        disabledbackground="#000000",
        fg="#ffffff",
        disabledforeground="#ffffff",
        state="disabled",
        font=("ITCErasStd-Ultra", 20 * -1),
        highlightthickness=0
    )
    mainRankedCharacterPlayerEntry.place(
        x=164.0,
        y=519.0,
        width=212.0,
        height=25.0
    )
    
    timePlayedPlayer = tk.StringVar()
    entry_image_timePlayedPlayer = tk.PhotoImage(
    file=relative_to_assets("entry_8.png"))
    entry_bg_timePlayedPlayer = canvas.create_image(
        278.0,
        576.5,
    image=entry_image_timePlayedPlayer
    )
    timePlayedPlayerEntry = ttk.Entry(
        textvariable=timePlayedPlayer,
        bd=0,
        bg="#000000",
        disabledbackground="#000000",
        fg="#ffffff",
        disabledforeground="#ffffff",
        state="disabled",
        font=("ITCErasStd-Ultra", 20 * -1),
        highlightthickness=0
    )
    timePlayedPlayerEntry.place(
        x=180.0,
        y=566.0,
        width=196.0,
        height=25.0
    )

    passiveAgressivePlayer = tk.StringVar()
    entry_image_passiveAgressivePlayer = tk.PhotoImage(file=relative_to_assets("entry_9.png"))
    entry_bg_passiveAgressivePlayer = canvas.create_image(
        265.0,
        622.5,
        image=entry_image_passiveAgressivePlayer
    )
    passiveAgressivePlayerEntry = ttk.Entry(
        textvariable=passiveAgressivePlayer,
        bd=0,
        bg="#000000",
        disabledbackground="#000000",
        fg="#ffffff",
        disabledforeground="#ffffff",
        state="disabled",
        font=("ITCErasStd-Ultra", 20 * -1),
        highlightthickness=0
    )
    passiveAgressivePlayerEntry.place(
        x=156.0,
        y=611.0,
        width=222.0,
        height=25.0
    )

    globalRankPlayerTitleLabel = tk.Label(
        text = "Global Rank :",
        bd=0,
        bg="#1F1A1A",
        fg="#ffffff",
        font=("ITCErasStd-Ultra", 16 * -1),
        anchor="w"
    )
    globalRankPlayerTitleLabel.place(
        x=175,
        y=30.0,
        width=350.0,
        height=40.0
    )

    regionRankPlayerTitleLabel = tk.Label(
        text = "Region Rank :",
        bd=0,
        bg="#1F1A1A",
        fg="#ffffff",
        font=("ITCErasStd-Ultra", 16 * -1),
        anchor="w"
    )
    regionRankPlayerTitleLabel.place(
        x=175,
        y=90.0,
        width=350.0,
        height=40.0
    )

    globalRankPlayerLabel = tk.Label(
        text = "#2624969",
        bd=0,
        bg="#1F1A1A",
        fg="#ffffff",
        font=("ITCErasStd-Ultra", 30 * -1),
        anchor="w"
    )
    globalRankPlayerLabel.place(
        x=175,
        y=55.0,
        width=350.0,
        height=40.0
    )

    regionRankPlayerLabel = tk.Label(
        text = "#2624969",
        bd=0,
        bg="#1F1A1A",
        fg="#ffffff",
        font=("ITCErasStd-Ultra", 30 * -1),
        anchor="w"
    )
    regionRankPlayerLabel.place(
        x=175,
        y=115.0,
        width=350.0,
        height=40.0
    )

    canvas.create_rectangle(
        14.000000000000014,
        217.0,
        385.0,
        223.0,
        fill="#837171",
        outline="#847171")

    playerNamePlayerLabel = tk.Label(
        text = "PlayerName",
        bd=0,
        bg="#1F1A1A",
        fg="#ffffff",
        font=("ITCErasStd-Ultra", 36 * -1),
        anchor="w"
    )
    playerNamePlayerLabel.place(
        x=14.000000000000014,
        y=173.0,
        width=350.0,
        height=40.0
    )

    button_image_switchPlayer = tk.PhotoImage(file=relative_to_assets("button_1.png"))
    entry_bg_switchPlayer = canvas.create_image(
        265.0,
        622.5,
        image=button_image_switchPlayer,
        state = "hidden"
    )
    switchPlayerButton = tk.Button(
        image="",
        borderwidth=0,
        highlightthickness=0,
        bg = "#1F1A1A",
        activebackground = "#1F1A1A",
        state = "disabled",
        command=lambda: switchProfile("command"),
        relief="flat"
    )
    switchPlayerButton.place(
        x=345.0,
        y=5.0,
        width=60.0,
        height=60.0
    )
    # switchPlayerButton.pack_forget()

    window.resizable(False, False)

    clientInfo()
    infosBrawlRecuperation()
    window.mainloop()
    global end
    end = True





q = Queue()
t = Thread(target=detect_brawlhalla, args=(q,))

user_config = os.environ.get('USERPROFILE') + '\\.BrawlhallaMatchupInfo\\config.json'
user_config_test = os.environ.get('USERPROFILE') + '\\.BrawlhallaMatchupInfo'

if os.path.exists(user_config) and os.path.isfile(user_config):
    config_path = user_config
else:
    config_path = dir + '/config.json'
    os.mkdir(user_config_test)
    shutil.copy(config_path, user_config_test)

with open(config_path) as fp:
    config = json.load(fp)
    print(user_config, config_path, config)


def validateBrawlID():
    global brawlIdClient
    brawlIdClient = brawlID.get()

    linkAPI = API_LINK + "/api/brawl/test/{}".format(brawlIdClient)
    response = requests.get(linkAPI)
    apiResult = response.json()
    try:
        int(brawlIdEntry.get())
        # try:
        if(apiResult["result"]["correctID"] == True):
            t.start()
            brawlIdEntryText = {"brawlIdClient" : brawlIdClient}

            file = open(user_config, "w")
            text = json.dumps(brawlIdEntryText)
            file.write(text)
            file.close()
            # frame.pack_forget()
            root.destroy()
            mainFrame()
            # clientInfo(brawlIdClient)
        # except Exception:
        else:
            waitingTime = apiResult["result"]["waitingTime"]
            errorIdLabel["text"] = "Error: ID is incorrect, try again in " + str(waitingTime) + " seconds"
            validateButton["state"] = "disabled"
            var = tk.IntVar()
            root.after(waitingTime*1000, var.set, 1)
            print("waiting...")
            root.wait_variable(var)
            errorIdLabel["text"] = ""
            validateButton["state"] = "normal"

    except ValueError:
        errorIdLabel["text"] = "Error: this is not a number, try again"







root = tk.Tk()
root.title('Brawlhalla Matchup Info v1')
root.geometry("410x165")
root.iconbitmap(dir + "/img/azoth.ico")



canvas = tk.Canvas(
    root,
    bg = "#201B1B",
    height = 165,
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
brawlIdEntry = ttk.Entry(
    textvariable = brawlID,
    bd=0,
    bg="#000000",
    # disabledbackground="#000000",
    fg="#ffffff",
    # disabledforeground="#ffffff",
    # state="readonly",
    # state="disabled",
    insertbackground="#ffffff",
    font=("ITCErasStd-Ultra", 40 * -1),
    justify='center',
    highlightthickness=0
)
brawlIdEntry.place(
    x=67.0,
    y=55.0,
    width=276.0,
    height=43.0
)

errorIdLabel = tk.Label(
    text = "",
    bd=0,
    bg="#1F1A1A",
    fg="red",
    font=("ITCErasStd-Ultra", 16 * -1),
    anchor="w"
)
errorIdLabel.place(
    x=5,
    y=105.0,
    width=400.0,
    height=20.0
)

canvas.create_rectangle(
    155.0,
    130.0,
    255.0,
    140.0,
    fill="#201B1B",
    outline="")

validateButton = tk.Button(
    # image=button_image_0,
    borderwidth=0,
    highlightthickness=0,
    command = validateBrawlID,
    relief="flat",
    text = "Validate",
    font=("ITCErasStd-Ultra", 24 * -1)
)
validateButton.place(
    x=150.0,
    y=130.0,
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


def readInFile():
    f = open(config_path, 'r')
    if f.mode=='r':
        # id= f.read()
        json_data = json.load(f)
        id = json_data["brawlIdClient"]
        brawlIdEntry.insert(0,id)

readInFile()


root.mainloop()

