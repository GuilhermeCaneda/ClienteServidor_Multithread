#client.py

import socket
import json

# Função para cálculo
def leibniz(interval):
    # Inicializa variáveis para armazenar os resultados dos cálculos
    resultNumber = 0.0
    evenNumber = 0.0
    oddNumber = 0.0

    # Itera sobre o intervalo dado
    for i in range(interval[0], interval[1]):
        # Calcula o termo da série de Leibniz para o índice i
        number = (-1) ** i / ((2 * i) + 1)
        resultNumber += number

        # Divide os termos em números pares e ímpares
        if (i%2==0):
            evenNumber += number
        else:
            oddNumber += number

    # Retorna os resultados dos cálculos
    return (resultNumber * 4), (evenNumber * 4), (oddNumber * 4) 

# Conecta o cliente ao servidor
def connect(HOST, PORT):
    # Cria um socket e conecta ao servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Recebe o intervalo do servidor, no formato [min, max]
    data = s.recv(1024)
    received_data = json.loads(data.decode())  

    # Realiza os cálculos
    calc_Number, even_Number, odd_Number = leibniz(received_data)

    # Envia os resultados para o servidor
    s.sendall(f"{even_Number} {odd_Number} {calc_Number}".encode())