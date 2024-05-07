#client.py

import socket
import json

#FUNÇÃO PARA CÁLCULO
def leibniz(interval):
    resultNumber = 0.0
    evenNumber = 0.0
    oddNumber = 0.0
    for i in range(interval[0], interval[1]):
        number = (-1) ** i / ((2 * i) + 1)
        resultNumber += number

        if (i%2==0):
            evenNumber += number
        else:
            oddNumber += number
    return (resultNumber * 4), (evenNumber * 4), (oddNumber * 4) 

#CONECTA AO SERVIDOR
def connect(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    #RECEBE INTERVALO
    data = s.recv(1024)
    received_data = json.loads(data.decode())  

    #REALIZA OS CÁLCULOS
    calc_Number, even_Number, odd_Number = leibniz(received_data)

    #ENVIA OS DADOS PARA O SERVIDOR
    s.sendall(f"{even_Number} {odd_Number} {calc_Number}".encode())