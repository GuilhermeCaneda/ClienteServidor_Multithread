# server.py

import socket
import json
import multiprocessing

resultPI = multiprocessing.Value('f', 0.0)

def connection(conn_number, conn, ender, interval, resultPI, listNumbers, listOdd, listEven):
    print('\n\nClient:', conn_number, '/ Interval:', interval)
    print('Connected at', ender)

    json_data = json.dumps(interval)
    conn.sendall(json_data.encode()) # MANDA O INTERVALO

    data = conn.recv(1024)
    even_number = float(data.decode()) # RECEBE OS PARES

    data = conn.recv(1024)
    odd_number = float(data.decode()) # RECEBE Os impares

    data = conn.recv(1024)
    pi_number = float(data.decode()) # RECEBE O RESULTADO DO PI
    

    print(pi_number, "from", ender)
    print('Even:', even_number)
    print('Odd:', odd_number)

    with resultPI.get_lock():
        resultPI.value += pi_number
        print('PI: ', resultPI.value)

    listNumbers[conn_number] = pi_number
    listEven[conn_number] = even_number
    listOdd[conn_number] = odd_number

    print('Closing connection with', ender)
    conn.close()

def start(HOST, PORT, num_connections, num_terms, result_queue, ender_queue, interval_queue, number_queue, odd_queue, even_queue):
    manager = multiprocessing.Manager()
    listNumbers = manager.list([0.0] * num_connections)
    listOdd = manager.list([0.0] * num_connections)
    listEven = manager.list([0.0] * num_connections)
    listInterval = []
    listEnder = []


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()


    processes = []
    for i in range(0, num_connections):
        interval_Min = int((num_terms/num_connections) * i)
        interval_Max = int(((num_terms/num_connections) * (i+1))-1)
        conn, ender = s.accept()
        
        listEnder.append(ender)
        listInterval.append([interval_Min, interval_Max])

        process = multiprocessing.Process(target=connection, args=(i, conn, ender, [interval_Min, interval_Max], resultPI, listNumbers, listOdd, listEven))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    result_queue.put(resultPI.value)
    ender_queue.put(listEnder) 
    interval_queue.put(listInterval)
    number_queue.put(list(listNumbers))
    odd_queue.put(list(listOdd))
    even_queue.put(list(listEven))