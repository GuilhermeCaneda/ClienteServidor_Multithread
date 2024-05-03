
#client.py

import socket
import json

#FUNÇÃO PARA CÁLCULO
def leibniz(numbers):
    resultNumber = 0.0
    evenNumber = 0.0
    oddNumber = 0.0
    for i in range(numbers[0], numbers[1]):
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

    #CALCULA E ENVIA RESULTADO LEIBNIZ
    pi_Number, even_Number, odd_Number = leibniz(received_data)
    s.sendall(str(even_Number).encode()) #ENVIA OS NUMEROS PARES
    s.sendall(str(odd_Number).encode()) #ENVIA OS NUMEROS IMPARES
    s.sendall(str(pi_Number).encode()) #ENVIA O VALOR DE PI