import cv2
import numpy as np
import pyautogui
import time
import easyocr

CharactersList = ["Ada",
                  "Artemis",
                  "Asuri",
                  "Azoth",
                  "Barraza",
                  "Bodvar",
                  "Brynn",
                  "Caspian",
                  "Cassidy",
                  "Cross",
                  "Diana",
                  "Dusk",
                  "Ember",
                  "Fait",
                  "Gnash",
                  "Hattori",
                  "Isaiah",
                  "Jaeyun",
                  "Jhala",
                  "Jiro",
                  "Kaya",
                  "Koji",
                  "Kor",
                  "Lin Fei",
                  "Lord Vraxx",
                  "Lucien",
                  "Magyar",
                  "Mako",
                  "Mirage",
                  "Mordex",
                  "Nix",
                  "Onyx",
                  "Orion",
                  "Petra",
                  "Queen Nai",
                  "Ragnir",
                  "Rayman",
                  "Reno",
                  "Scarlet",
                  "Sentinel",
                  "Sidra",
                  "Sir Roland",
                  "Teros",
                  "Thatch",
                  "Thor",
                  "Ulgrim",
                  "Val",
                  "Vector",
                  "Volkov",
                  "Wu Shang",
                  "Xull",
                  "Yumiko",
                  "Zariel",
                  "Shovel Knight",
                  "Black Knight",
                  "King Knight",
                  "Plague Knight",
                  "Specter Knight",
                  "Enchantress",
                  "Globox",
                  "Barbara",
                  "Hellboy",
                  "Gruagach",
                  "Daimio",
                  "Nimue",
                  "The Rock",
                  "John Cena",
                  "Xavier Woods",
                  "Becky Lynch",
                  "Macho Man",
                  "The Undertaker",
                  "Asuka",
                  "Roman Reigns",
                  "Finn",
                  "Jake",
                  "Princess Bubblegum",
                  "Stevonnie",
                  "Pearl",
                  "Amethyst",
                  "Garnet",
                  "Lara Croft",
                  "Four Arms",
                  "Diamondhead",
                  "Heatblast",
                  "Michonne",
                  "Rick",
                  "Daryl",
                  "Po",
                  "Tigress",
                  "Tai Lung",
                  "Leonardo",
                  "Donatello",
                  "Raphael",
                  "Michelangelo"]

TagsList = ["Veteran of Asgard I",
            "Veteran of Asgard |",
            "Veteran of Asgard !",
            "Veteran of Asgard II",
            "Veteran of Asgard III",
            "Veteran of Asgard IV",
            "Veteran of Asgard V",
            "Captain of Asgard I",
            "Great Witness",
            "Winter Watcher",
            "Spring Spectator",
            "Summer Superfan",
            "Autumn Observer",
            "Reveler",
            "Lucky Brawler",
            "Perennial Brawler",
            "Beach Brawler",
            "Jötunn",
            "Exalted Lion",
            "OG Metadev Asuri",
            "OG Metadev Bödvar",
            "OG Metadev Brynn",
            "OG Metadev Ember",
            "OG Metadev Orion",
            "Partnered Creator",
            "Developer",
            "S20 Kung Foot Player",
            "S21 Brawlball Player",
            "S20 Kung Foot Adept",
            "S21 Brawlball Adept",
            "S20 Kung Foot Veteran",
            "S21 Brawlball Veteran",
            "S20 Kung Foot Master",
            "S21 Brawlball Master",
            "Tournament Titles",
            "World Champion",
            "Winter Champion",
            "Spring Champion",
            "Summer Champion",
            "Autumn Champion",
            "CEO Champion",
            "CB Champion",
            "DH Austin Champion",
            "DH Summer Champion",
            "DH Valencia Champion",
            "DH Montreal Champion",
            "DH Winter Champion",
            "DH Dallas Champion",
            "DH Rotterdam Champion",
            "FR2019 Champion",
            "Low Tier City 7 Champion",
            "Shine Champion",
            "Great Brawl Champion",
            "Charged OG Champion",
            "LTC Online Champion",
            "Steel Series Champion",
            "Mammoth Cup Champion",
            "BCX Finalist",
            "SEA Challenger"]

reader = easyocr.Reader(['en'])  # need to run only once to load model into memory


def ocr_core(img):
    text = reader.readtext(img, detail = 0)
    return text


def get_greyscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def remove_noise(image):
    return cv2.medianBlur(image, 5)


def thresholding(image):
    #return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return cv2.threshold(image,55,255,cv2.THRESH_BINARY)
    #return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)


def detect_brawlhalla(queue=None):

    end = False
    while not end:
        try:
            ok = False
            # pathcode1 = "img/imgLoading.jpg"
            textarealocation = pyautogui.locateOnScreen(
                r"img/imgLoading.jpg", confidence=0.9)
            if textarealocation is not None:
                print("Detection OK")
                ok = True
                time.sleep(1)
                image = pyautogui.screenshot()
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                cv2.imwrite("img/imgBattle.jpg", image)
                #   pyautogui.write(code)

                imgBattle = cv2.imread('img/imgBattle.jpg')
                imgBattle = get_greyscale(imgBattle)
                # imgBattle = thresholding(imgBattle)
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



#detect_brawlhalla()

# TESTS

if __name__ == '__main__':

    imgTest1 = cv2.imread('img/imgBattle.jpg')

    imgTest1 = get_greyscale(imgTest1)
    # imgTest1 = thresholding(imgTest1)
    # imgTest1 = remove_noise(imgTest1)

    y = 263
    x = 1208
    h = 80
    w = 280
    start_point = (1200, 264)
    end_point = (1250, 290)
    color = (0, 0, 0)
    thickness = -1
    crop = cv2.rectangle(imgTest1, start_point, end_point, color, thickness)
    crop = imgTest1[y:y + h, x:x + w]
    #crop = cv2.resize(crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # ret,crop = cv2.threshold(crop,120,255,cv2.THRESH_BINARY)
    cv2.imshow('Image', crop)
    cv2.waitKey(0)


    imgTest2 = cv2.imread('img/imgTest2.jpg')

    imgTest2 = get_greyscale(imgTest2)
    # imgTest2 = thresholding(imgTest2)
    # imgTest2 = remove_noise(imgTest2)

    y = 263
    x = 1208
    h = 80
    w = 280
    start_point = (1200, 264)
    end_point = (1250, 290)
    color = (0, 0, 0)
    thickness = -1
    crop2 = cv2.rectangle(imgTest2, start_point, end_point, color, thickness)
    crop2 = imgTest2[y:y + h, x:x + w]
    crop2 = cv2.resize(crop2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # ret,crop2 = cv2.threshold(crop,120,255,cv2.THRESH_BINARY)
    cv2.imshow('Image', crop2)
    cv2.waitKey(0)

    imgTest1 = cv2.imread('img/imgTest1.jpg')
    y = 50
    x = 860
    h = 580
    w = 200
    crop3 = imgTest1[y:y + h, x:x + w]
    cv2.imshow('Image', crop3)
    cv2.waitKey(0)
    # cv2.imwrite('imgLoading.jpg',crop3) #for saving the crop image

    listInfoJ1 = ocr_core(crop)
    listInfoJ2 = ocr_core(crop2)
    detectImageLoading = ocr_core(crop3)

    print(listInfoJ1)
    print(listInfoJ2)

    persoJ1 = ""
    tagJ1 = ""
    nameJ1 = ""
    clanJ1 = ""
    persoJ2 = ""
    tagJ2 = ""
    nameJ2 = ""
    clanJ2 = ""





    # J1

    listInfoTempJ1 = listInfoJ1

    if (len(listInfoJ1) == 4):
        persoJ1 = listInfoJ1[0].lower().capitalize()
        tagJ1 = listInfoJ1[1]
        nameJ1 = listInfoJ1[2]
        clanJ1 = listInfoJ1[3]

    if (len(listInfoJ1) == 3):
        for i in range(len(listInfoJ1)):
            for z in range(len(TagsList)):
                if (TagsList[z] in listInfoJ1[i]):  # a changer en contient (.find)
                    tagJ1 = listInfoJ1[i]
            for y in range(len(CharactersList)):
                if (CharactersList[y].upper() in listInfoJ1[i]):
                    persoJ1 = CharactersList[y]
                    persoTempJ1 = listInfoJ1[i]

            if (listInfoJ1[i][0] == '<' and listInfoJ1[i][len(listInfoJ1[i]) - 1] == '>'):
                clanJ1 = listInfoJ1[i]

    if (len(listInfoJ1) == 2):
        persoJ1 = listInfoJ1[0].lower().capitalize()
        nameJ1 = listInfoJ1[1]
        tagJ1 = "None"
        clanJ1 = "None"

    if (len(listInfoJ1) == 3):
        listInfoTempJ1.remove(persoTempJ1)

    try:
        listInfoTempJ1.remove(clanJ1)
    except ValueError:
        clanJ1 = "None"

    try:
        listInfoTempJ1.remove(tagJ1)
    except ValueError:
        tagJ1 = "None"

    nameJ1 = listInfoTempJ1[0]







    # J2
    listInfoTempJ2 = listInfoJ2

    if (len(listInfoJ2) == 4):
        persoJ2 = listInfoJ2[0].lower().capitalize()
        tagJ2 = listInfoJ2[1]
        nameJ2 = listInfoJ2[2]
        clanJ2 = listInfoJ2[3]

    if (len(listInfoJ2) == 3):
        for i in range(len(listInfoJ2)):
            for z in range(len(TagsList)):
                if (TagsList[z] in listInfoJ2[i]):  # a changer en contient (.find)
                    tagJ2 = listInfoJ2[i]
            for y in range(len(CharactersList)):
                if (CharactersList[y].upper() in listInfoJ2[i]):
                    persoJ2 = CharactersList[y]
                    persoTempJ2 = listInfoJ2[i]

            if (listInfoJ2[i][0] == '<' and listInfoJ2[i][len(listInfoJ2[i]) - 1] == '>'):
                clanJ2 = listInfoJ2[i]

    if (len(listInfoJ2) == 2):
        persoJ2 = listInfoJ2[0].lower().capitalize()
        nameJ2 = listInfoJ2[1]
        tagJ2 = "None"
        clanJ2 = "None"

    if (len(listInfoJ1) == 3):
        listInfoTempJ2.remove(persoTempJ2)

    try:
        listInfoTempJ2.remove(clanJ2)
    except ValueError:
        clanJ2 = "None"

    try:
        listInfoTempJ2.remove(tagJ2)
    except ValueError:
        tagJ2 = "None"

    nameJ2 = listInfoTempJ2[0]

    print("Character J1: " + persoJ1 + ", Tag J1: " + tagJ1 + ", Name J1: " + nameJ1 + ", Clan J1: " + clanJ1)
    print("Character J2: " + persoJ2 + ", Tag J2: " + tagJ2 + ", Name J2: " + nameJ2 + ", Clan J2: " + clanJ2)

