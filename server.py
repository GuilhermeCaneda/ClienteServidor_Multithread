# server.py

import socket
import json
import multiprocessing

#resultPI = multiprocessing.Value('f', 0.0)

def connection(conn_index, conn, ender, interval, resultPI, listCalcNumber, listOddNumber, listEvenNumber):
    print('\n\nClient:', (conn_index+1), '/ Interval:', interval)
    print('Connected at', ender)

    json_data = json.dumps(interval)
    conn.sendall(json_data.encode()) # MANDA O INTERVALO

    data = conn.recv(1024)
    numbers = data.decode().split()
    evenNumber = float(numbers[0])
    oddNumber = float(numbers[1])
    calcNumber = float(numbers[2])

    print(calcNumber, "from", ender)
    print('Even:', evenNumber)
    print('Odd:', oddNumber)

    #with resultPI.get_lock():
    #    resultPI.value += calcNumber
    #    print('PI: ', resultPI.value)

    resultPI.put(calcNumber)

    listCalcNumber[conn_index] = calcNumber
    listEvenNumber[conn_index] = evenNumber
    listOddNumber[conn_index] = oddNumber
    print('Closing connection with', ender)
    conn.close()

def start(HOST, PORT, num_connections, num_terms, finalResult_queue, listEnderNumber_queue, listInterval_queue, listCalcNumber_queue, listOddNumber_queue, listEvenNumber_queue):
    manager = multiprocessing.Manager()
    listCalcNumber = manager.list([0.0] * num_connections)
    listOddNumber = manager.list([0.0] * num_connections)
    listEvenNumber = manager.list([0.0] * num_connections)
    listInterval = []
    listEnderNumber = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    resultPI = multiprocessing.Queue()

    processes = []
    for i in range(0, num_connections):
        interval_Min = int((num_terms/num_connections) * i)
        interval_Max = int(((num_terms/num_connections) * (i+1))-1)
        conn, ender = s.accept()
        
        listEnderNumber.append(ender)
        listInterval.append([interval_Min, interval_Max])

        process = multiprocessing.Process(target=connection, args=(i, conn, ender, [interval_Min, interval_Max], resultPI, listCalcNumber, listOddNumber, listEvenNumber))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    resultPI_value = 0.0
    for i in range(num_connections):
        resultPI_value += resultPI.get()

    finalResult_queue.put(resultPI_value)
    listEnderNumber_queue.put(listEnderNumber) 
    listInterval_queue.put(listInterval)
    listCalcNumber_queue.put(list(listCalcNumber))
    listOddNumber_queue.put(list(listOddNumber))
    listEvenNumber_queue.put(list(listEvenNumber))