# server.py

import socket
import json
import multiprocessing


# Define a função que lida com a conexão de um cliente
def connection(conn_index, conn, ender, interval, resultPI, listCalcNumber, listOddNumber, listEvenNumber):
    # Exibe informações sobre a conexão
    print('\n\nClient:', (conn_index+1), '/ Interval:', interval)
    print('Connected at', ender)

    # Converte o intervalo em JSON e envia para o cliente
    json_data = json.dumps(interval)
    conn.sendall(json_data.encode()) 

    # Recebe os números calculados do cliente e os converte para float
    data = conn.recv(1024)
    numbers = data.decode().split()
    evenNumber = float(numbers[0])
    oddNumber = float(numbers[1])
    calcNumber = float(numbers[2])

    # Exibe os números recebidos e calculados
    print(calcNumber, "from", ender)
    print('Even:', evenNumber)
    print('Odd:', oddNumber)

    # Adiciona o resultado do cálculo à fila compartilhada
    resultPI.put(calcNumber)

    # Atualiza as listas compartilhadas com os resultados individuais
    listCalcNumber[conn_index] = calcNumber
    listEvenNumber[conn_index] = evenNumber
    listOddNumber[conn_index] = oddNumber

    # Fecha a conexão com o cliente
    print('Closing connection with', ender)
    conn.close()


# Função principal para iniciar o servidor
def start(HOST, PORT, num_connections, num_terms, finalResult_queue, listEnderNumber_queue, listInterval_queue, listCalcNumber_queue, listOddNumber_queue, listEvenNumber_queue):
    
    # Cria um gerenciador de contexto para objetos compartilhados
    manager = multiprocessing.Manager()

    # Inicializa listas compartilhadas para armazenar resultados e intervalos
    listCalcNumber = manager.list([0.0] * num_connections)
    listOddNumber = manager.list([0.0] * num_connections)
    listEvenNumber = manager.list([0.0] * num_connections)
    listInterval = []
    listEnderNumber = []

    # Cria um socket TCP/IP e o vincula ao endereço e porta fornecidos
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    # Cria uma fila de resultados finais
    resultPI = multiprocessing.Queue()

    # Inicia um loop para aceitar conexões dos clientes
    processes = []
    for i in range(0, num_connections):
        # Calcula os limites do intervalo para este cliente
        interval_Min = int((num_terms/num_connections) * i)
        interval_Max = int(((num_terms/num_connections) * (i+1))-1)

        # Aceita a conexão do cliente e adiciona o endereço e o intervalo às listas
        conn, ender = s.accept()
        listEnderNumber.append(ender)
        listInterval.append([interval_Min, interval_Max])

        # Inicia um processo para lidar com esta conexão
        process = multiprocessing.Process(target=connection, args=(i, conn, ender, [interval_Min, interval_Max], resultPI, listCalcNumber, listOddNumber, listEvenNumber))
        process.start()
        processes.append(process)

    # Espera todos os processos terminarem
    for process in processes:
        process.join()

    # Calcula o valor final de Pi somando os resultados parciais
    resultPI_value = 0.0
    for i in range(num_connections):
        resultPI_value += resultPI.get()

    # Adiciona o resultado final e outras listas à fila compartilhada
    finalResult_queue.put(resultPI_value)
    listEnderNumber_queue.put(listEnderNumber) 
    listInterval_queue.put(listInterval)
    listCalcNumber_queue.put(list(listCalcNumber))
    listOddNumber_queue.put(list(listOddNumber))
    listEvenNumber_queue.put(list(listEvenNumber))