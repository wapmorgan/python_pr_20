from appJar import gui
from data import images_folders, signs, sources
from net import getFromOrakul, getFromMail

currentSource=list(sources.keys())[0]
currentHoroscope=list(sources[currentSource]["horoscopes"].keys())[0]

def clickImage(imageLabel):
    sign_i = int(imageLabel[5:-4])
    sign_label = tuple(signs[currentHoroscope].keys())[sign_i]
    sign_conf = signs[currentHoroscope][sign_label]
    print("Click on " + sign_label)
    # Need to firstly update the label, then image.
    app.setLabel("selected_sign_label", sign_label)
    app.setMessage("selected_sign_prediction", "Получение данных ...")
    app.setImage("selected_sign_img", images_folders[currentHoroscope] + "/" + sign_conf[0] + ".gif")
    if currentSource == "orakul.com":
        prediction=getFromOrakul(sources[currentSource]["horoscopes"][currentHoroscope], sources[currentSource][currentHoroscope][sign_label])
    elif currentSource == "horo.mail.ru":
        prediction=getFromMail(sources[currentSource]["horoscopes"][currentHoroscope], sources[currentSource][currentHoroscope][sign_label])
    app.setMessage("selected_sign_prediction", prediction)

def changeSource(optionBox):
    global currentSource
    newSource = app.getOptionBox(optionBox)
    if newSource != currentSource:
        currentSource = newSource
        print("Changed current source to " + currentSource)
        # Change horoscope if new source doesn't have the selected one
        if currentHoroscope not in sources[currentSource]["horoscopes"].keys():
            app.setOptionBox("Гороскоп", list(sources[currentSource]["horoscopes"].keys())[0])
        else:
            sign_label = app.getLabel("selected_sign_label")
            # Or update the prediction if sign has been selected
            if sign_label != "":
                sign_i = tuple(signs[currentHoroscope].keys()).index(sign_label)
                clickImage("sign_" + str(sign_i) + "_img")

def changeHoroscope(optionBox):
    global currentHoroscope
    newHoroscope = app.getOptionBox(optionBox)
    if newHoroscope != currentHoroscope:
        currentHoroscope = newHoroscope
        print("Changed current horoscope to " + currentHoroscope)
        # Clear prediction for new horoscope
        app.setImage("selected_sign_img", images_folders[currentHoroscope] + "/back.gif")
        app.setLabel("selected_sign_label", "")
        app.setMessage("selected_sign_prediction", "Выберите знак")
        i=0
        for sign_label, sign_conf in signs[currentHoroscope].items():
            app.setImage("sign_" + str(i) + "_img", images_folders[currentHoroscope] + "/" + sign_conf[0] + ".gif")
            app.setLabel("sign_" + str(i) + "_label", getSignLabel(sign_label))
            i= i + 1

def getSignLabel(sign_label):
    if currentHoroscope == "Зодиакальный":
        label = signs[currentHoroscope][sign_label][1][2:] + "." + signs[currentHoroscope][sign_label][1][:2] + " - " + \
                signs[currentHoroscope][sign_label][2][2:] + "." + signs[currentHoroscope][sign_label][2][:2]
    elif currentHoroscope == "Китайский":
        label = repr(signs[currentHoroscope][sign_label][1][-3:-1])
    return label

def main():
    app.addLabelOptionBox("Источник", ["orakul.com", "horo.mail.ru"], 0, 0)
    app.setOptionBoxChangeFunction("Источник", changeSource)

    app.addLabelOptionBox("Гороскоп", sources[currentSource]["horoscopes"].keys(), 0, 1, 2)
    app.setOptionBoxChangeFunction("Гороскоп", changeHoroscope)

    app.decreaseLabelFont()

    current_row=0
    current_column=0
    i=0
    app.startLabelFrame("Знаки", 1, 0, rowspan=3)
    for sign_label, sign_conf in signs[currentHoroscope].items():
        app.addImage("sign_" + str(i) + "_img", images_folders[currentHoroscope] + "/" + sign_conf[0] + ".gif", (current_row * 2) + 1, current_column)
        app.addLabel("sign_" + str(i) + "_label", getSignLabel(sign_label), current_row * 2 + 2, current_column)
        app.setImageSubmitFunction("sign_" + str(i) + "_img", clickImage)

        if current_column == 3:
            current_row = current_row + 1
            current_column = 0
        else:
            current_column = current_column + 1
        i=i+1
    app.stopLabelFrame()

    app.addImage("selected_sign_img", images_folders[currentHoroscope] + "/back.gif", 1, 1, 2)
    app.addLabel("selected_sign_label", "", 2, 1, 2)
    app.addMessage("selected_sign_prediction", "Выберите знак", 3, 1, 2)

    # bottom slice - START the GUI
    app.go()


# top slice - CREATE the GUI
app = gui("Гороскоп")
app.setImageLocation("images/")
app.setStretch("both")
app.setResizable(False)
app.setBg("white")
main()
