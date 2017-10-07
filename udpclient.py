import socket

def UdpClient(vektor):
    localhostIP = "127.0.0.1"
    serverIP = "192.168.10.1"
    udpPort = 8000
    message  = ''.join(str(x)+',' for x in vektor).encode()

    print(''.join(str(x)+',' for x in vektor))
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP

    #Sende an Localhost, damit das Programm auch auf 1 Rechner läuft
    sock.sendto(message, (localhostIP, udpPort))
    #Sende an DHCP-Server(Lernmatrix)
    sock.sendto(message, (serverIP, udpPort))