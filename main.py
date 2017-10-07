import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import QPushButton, QProgressBar

from mainwindow import Ui_MainWindow
from eingabewindow import Ui_EingabeWindow
from beispielgewichte import beispielgewichte
import udpserver
import udpclient

anzahlNeuronen = 10
anzahlGewichte = 20
eingabevektor = [-1]*anzahlGewichte
proto_eingabevektor = [-1]*anzahlGewichte


class Neuron:

    def __init__(self):
        self.gewicht = [0]*anzahlGewichte
        self.output = 0

    def Anlernen(self):
        for i in range(anzahlGewichte):
            self.gewicht[i] = eingabevektor[i]
            maingui.repaint()

    def Vergessen(self):
        for i in range(anzahlGewichte):
            self.gewicht[i] = 0

    def ReturnOutput(self):
        self.output = 0
        for i in range(anzahlGewichte):
            self.output += eingabevektor[i] * self.gewicht[i]

        return self.output

        print("upgedated")

class MainWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        myWindowWidth = self.width()
        myWindowHeight = self.height()
        self.setMinimumSize(myWindowWidth, myWindowHeight)
        self.setMaximumSize(myWindowWidth, myWindowHeight)
        self.anlernenButton.clicked.connect(Anlernen)
        self.beispielButton.clicked.connect(BspAnlernen)
        self.vergessenButton.clicked.connect(Vergessen)
        #self.showFullScreen()
        self.setBuchstabenVisible(all=True,visible=False)
        self.update()
        self.show()

    def paintEvent(self, QPaintEvent):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.zeichneEingabevektor(qp)
        self.zeichneLernmatrix(qp)
        qp.end()

    def zeichneEingabevektor(self,qp):
        color = QtGui.QColor(0, 0, 0)
        qp.setPen(color)

        for i in range(20):

            if (eingabevektor[i] == 1):
                qp.setBrush(QtGui.QColor(255, 170, 0))
            else:
                qp.setBrush(QtGui.QColor(150, 150, 150))

            qp.drawRect(22+i*38, 28, 33, 33)

    def zeichneLernmatrix(self, qp):
        color = QtGui.QColor(0, 0, 0)
        qp.setPen(color)

        for zeile in range (10):
            for spalte in range(20):

                if(Neuronen[zeile].gewicht[spalte] == 1):
                    qp.setBrush(QtGui.QColor(255, 170, 0))
                else:
                    qp.setBrush(QtGui.QColor(150, 150, 150))

                qp.drawRect(133 + spalte * 25, 125+zeile*26, 20, 20)

    def setBuchstabenVisible(self,index=0, all=False, visible=True):
        buchstaben = ["label_A", "label_E", "label_I", "label_O", "label_U", "label_a", "label_e", "label_i", "label_o",
                      "label_u"]
        selectedLabel = self.groupBox_Beispiel.findChild(QtGui.QLabel, buchstaben[index])
        selectedLabel.setVisible(visible)

        if (all):
            for i in range(0, 10):
                selectedLabel = self.groupBox_Beispiel.findChild(QtGui.QLabel, buchstaben[i])
                selectedLabel.setVisible(visible)

class EingabeWindow(QtGui.QWidget,Ui_EingabeWindow):
    def __init__(self):
        super(EingabeWindow, self).__init__()
        uic.loadUi('eingabewindow.ui', self)
        myWindowWidth = self.width()
        myWindowHeight = self.height()
        self.setMinimumSize(myWindowWidth, myWindowHeight)
        self.setMaximumSize(myWindowWidth, myWindowHeight)
        self.resetButton.clicked.connect(ResetEingabe)
        for child in self.gridLayoutWidget_2.findChildren(QPushButton):
           child.clicked.connect(UpdateButtons)
        self.show()

def PrintEingabe():
    for wert in eingabevektor:
        print(wert, end=',', flush=True)
    print("")

def ResetEingabe():

    #Eingabevektor auf -1 setzen
    for i in range(0, len(eingabevektor)):
        eingabevektor[i] = -1

    #jeden Button entklicken
    for child in eingabegui.gridLayoutWidget_2.findChildren(QPushButton):
        child.setChecked(False)

    ResetProgress()
    maingui.repaint()

def ResetProgress():
    # Progressbars auf 0 setzen
    for progressbar in maingui.groupBox_Kannphase.findChildren(QProgressBar):
        progressbar.setValue(0)

def UpdateButtons():
    i=0
    PrintEingabe()
    for child in eingabegui.gridLayoutWidget_2.findChildren(QPushButton):
        if (child.isChecked()):
            proto_eingabevektor[i] = 1
        else:
            proto_eingabevektor[i] = -1

        i=i+1

    PrintEingabe()
    Erkennen()
    maingui.repaint()
    udpclient.UdpClient(proto_eingabevektor)

def Anlernen():
    #Überprüfen, welcher Neuron-Radiobutton ausgewählt wurde
    radios = ["b0", "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9"]
    for i in range(0, 10):
        selected_radio = maingui.groupBox_Lernphase.findChild(QtGui.QRadioButton, radios[i])
        #i läuft durch und entspricht gerade dem ausgewählten Radiobutton
        if selected_radio.isChecked():
            #Alle Radiobuttons unchecken
            #selected_radio.setAutoExclusive(False)
            #selected_radio.setChecked(False)
            #selected_radio.setAutoExclusive(True)

            #die nächste Bedeutung auswählen
            if (i < 9):
                next_radio = maingui.groupBox_Lernphase.findChild(QtGui.QRadioButton, radios[i+1])
                next_radio.setChecked(True)

            #Beispiel Buchstabe ausblenden
            maingui.setBuchstabenVisible(index=i,visible=False)
            Neuronen[i].Anlernen()
            break
    PrintEingabe()
    ResetEingabe()

    maingui.repaint()

def BspAnlernen():

    for i in range(anzahlNeuronen):
        # i läuft durch und entspricht gerade dem ausgewählten Label
        maingui.setBuchstabenVisible(index=i)


        for j in range(anzahlGewichte):
            eingabevektor[j]=beispielgewichte[i][j]
        Neuronen[i].Anlernen()

def Erkennen():
    barcounter = 0
    for progressbar in maingui.groupBox_Kannphase.findChildren(QProgressBar):
        progressbar.setValue(max(0, Neuronen[barcounter].ReturnOutput() * 5))
        print("Neuron", barcounter, "sagt", Neuronen[barcounter].ReturnOutput())
        barcounter += 1

def Vergessen():
    for Neuron in Neuronen:
        Neuron.Vergessen()

    ResetEingabe()
    maingui.setBuchstabenVisible(visible=False,all=True)

def udpRecievedEvent(recievedEingabe):
    eingabevektor[:] = recievedEingabe
    Erkennen()
    maingui.repaint()

#Neuronen initialisieren
Neuronen = list()
for i in range(anzahlNeuronen):
        Neuronen.append(Neuron())

#Guis initialisieren
app = QtGui.QApplication(sys.argv)
maingui = MainWindow()
eingabegui = EingabeWindow()

#Eigenen Thread für Server erstellen
serverThread = QtCore.QThread()
einServer = udpserver.UdpServer()
einServer.recieved.connect(udpRecievedEvent)
einServer.moveToThread(serverThread)
serverThread.started.connect(einServer.listen)
serverThread.start()

sys.exit(app.exec_())