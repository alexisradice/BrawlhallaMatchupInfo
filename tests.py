import os
import cv2
import numpy as np
import pyautogui
import time
import easyocr

reader = easyocr.Reader(['en'])  # need to run only once to load model into memory
dir = os.path.dirname(os.path.abspath(__file__))

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
            pathcodeLoading = dir + "/img/imgLoading.jpg"
            pathcodeBattle = dir + "/img/imgBattle.jpg"
            
            textarealocation = pyautogui.locateOnScreen(pathcodeLoading, confidence=0.9)
            if textarealocation is not None:
                print("Detection OK")
                ok = True
                time.sleep(1)
                image = pyautogui.screenshot()
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                cv2.imwrite(pathcodeBattle, image)
                #   pyautogui.write(code)

                imgBattle = cv2.imread(pathcodeBattle)
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

# if __name__ == '__tests__':

# dir_path = os.path.dirname(os.path.realpath(__file__))

dir = os.path.dirname(os.path.abspath(__file__))
pathcodeLoading = dir + "/img/imgLoading.jpg"
pathcodeBattle = dir + "/img/imgBattle.jpg"
pathcodeTest1 = dir + "/img/imgTest1.jpg"
pathcodeTest2 = dir + "/img/imgTest2.jpg"
imgTest1 = cv2.imread(pathcodeBattle)
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



imgTest2 = cv2.imread(pathcodeTest2)
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



imgTest1 = cv2.imread(pathcodeTest1)
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

if (len(listInfoJ1) == 4):
    persoJ1 = listInfoJ1[0].lower().capitalize()
    tagJ1 = listInfoJ1[1]
    nameJ1 = listInfoJ1[2]
    clanJ1 = listInfoJ1[3]
if (len(listInfoJ1) == 3):
    persoJ1 = listInfoJ1[0].lower().capitalize()
    for i in range(len(listInfoJ1)):
        if (listInfoJ1[2][0] == '<' and listInfoJ1[2][len(listInfoJ1[i]) - 1] == '>'):
            clanJ1 = listInfoJ1[2]
            nameJ1 = listInfoJ1[1]
            tagJ1 = "/"
        else:
            tagJ1 = listInfoJ1[1]
            nameJ1 = listInfoJ1[2]
            clanJ1 = "/"
if (len(listInfoJ1) == 2):
    persoJ1 = listInfoJ1[0].lower().capitalize()
    nameJ1 = listInfoJ1[1]
    tagJ1 = "/"
    clanJ1 = "/"







# J2

if (len(listInfoJ2) == 4):
    persoJ2 = listInfoJ2[0].lower().capitalize()
    tagJ2 = listInfoJ2[1]
    nameJ2 = listInfoJ2[2]
    clanJ2 = listInfoJ2[3]
if (len(listInfoJ2) == 3):
    persoJ2 = listInfoJ2[0].lower().capitalize()
    for i in range(len(listInfoJ2)):
        if (listInfoJ2[2][0] == '<' and listInfoJ2[2][len(listInfoJ2[i]) - 1] == '>'):
            clanJ2 = listInfoJ2[2]
            nameJ2 = listInfoJ2[1]
            tagJ2 = "/"
        else:
            tagJ2 = listInfoJ2[1]
            nameJ2 = listInfoJ2[2]
            clanJ2 = "/"
if (len(listInfoJ2) == 2):
    persoJ2 = listInfoJ2[0].lower().capitalize()
    nameJ2 = listInfoJ2[1]
    tagJ2 = "/"
    clanJ2 = "/"


print("Character J1: " + persoJ1 + ", Tag J1: " + tagJ1 + ", Name J1: " + nameJ1 + ", Clan J1: " + clanJ1)
print("Character J2: " + persoJ2 + ", Tag J2: " + tagJ2 + ", Name J2: " + nameJ2 + ", Clan J2: " + clanJ2)







# SAVE GUI NOT USED
# root.minsize(900, 600)

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





