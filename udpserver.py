from PyQt4 import QtCore
import socket

class UdpServer(QtCore.QObject):
    recieved = QtCore.pyqtSignal(list)

    @QtCore.pyqtSlot()
    def listen(self):
        BIND_IP = '0.0.0.0'
        BIND_PORT = 8000

        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((BIND_IP, BIND_PORT))
        print("Waiting on port: " + str(BIND_PORT))
#try
#exept pass
        while 1:
            # eingabeListe jedes mal neu definieren
            eingabe = [-1] * 20
            data, addr = server.recvfrom(1024)

            # String wird ggf. um \n gekürzt und jede -1 oder 1 wird in eine Liste umgeparst
            # Wenn Übertragungsfehler auftreten (etwas, was nicht 1 oder -1 ist wird empfangen)
            # wird es automatisch als -1 (d.h. leer) interpretiert
            recievedString = data.decode("utf-8").split('\n')[0]
            recievedList = [int(x) if x == '1' else -1 for x in recievedString.split(',')]

            # damit die Eingabeliste sicher immer 20 lang ist (Übertragungsfehler)
            # wird die empfangene Liste auf die vorher definierte Eingabeliste draufgeschrieben
            # damit nicht über die Liste hinaus geschrieben wird, wird es auf 20 limitiert
            for i in range(min(len(recievedList),20)):
                eingabe[i] = recievedList[i]

            print(eingabe)
            self.recieved.emit(eingabe)