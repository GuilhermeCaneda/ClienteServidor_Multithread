#interface.py

import tkinter as tk
from tkinter import ttk

import client
import server
import multiprocessing
import time

# Constantes para o endereço do servidor e porta
HOST_SERVER = 'localhost'
HOST_CLIENT = '127.0.0.1'
PORT = 50000

# Função para criar a interface gráfica
def createInterface():

    # Função para iniciar as conexões quando o botão for clicado
    def start_connections():
        # Captura o tempo inicial
        initialTime = time.time()

        # Obtém o número de conexões e o número de termos dos campos de entrada
        NUM_CONNECTIONS = int(connections_entry.get())
        NUM_TERMS = int(terms_entry.get())

        # Inicializa filas compartilhadas para os resultados e dados de conexão
        finalResult_queue = multiprocessing.Queue()
        listEnderNumber_queue = multiprocessing.Queue()
        listInterval_queue = multiprocessing.Queue()
        listCalcNumber_queue = multiprocessing.Queue()
        listOddNumber_queue = multiprocessing.Queue()
        listEvenNumber_queue = multiprocessing.Queue()

        # Inicia um processo para o servidor
        server_process = multiprocessing.Process(target=server.start, args=(HOST_SERVER, PORT, NUM_CONNECTIONS, NUM_TERMS, finalResult_queue, listEnderNumber_queue, listInterval_queue, listCalcNumber_queue, listOddNumber_queue, listEvenNumber_queue))
        server_process.start()

        # Realiza as conexões com o cliente
        print('Connections:')
        for i in range(NUM_CONNECTIONS):
            client.connect(HOST_CLIENT, PORT)
        server_process.join()

        # Obtém os resultados e dados de conexão do servidor a partir das filas compartilhadas
        finalResult_server = finalResult_queue.get()
        listEnderNumber_server = listEnderNumber_queue.get()
        listInterval_server = listInterval_queue.get()
        listCalcNumber_server = listCalcNumber_queue.get() 
        listOddNumber_server = listOddNumber_queue.get()
        listEvenNumber_server = listEvenNumber_queue.get() 

        # Captura o tempo final e calcula o tempo decorrido
        endTime = time.time()
        print('\n\nFinal Result:', finalResult_server)
        print('Elapsed time (s):', (endTime-initialTime))

        # Atualiza os rótulos na interface com os resultados obtidos
        finalResult_label_value.config(text=f"{finalResult_server}")
        elapsedTime_label_value.config(text=f"{(endTime-initialTime)}")
        
        # Atualiza a interface com os detalhes de conexão para cada cliente
        for i in range(NUM_CONNECTIONS):
            connection_frame = ttk.LabelFrame(canvas, text=f'CONEXÃO {i+1}')
            canvas.create_window((0, i*140), window=connection_frame, anchor="nw")

            address_label_name = ttk.Label(connection_frame, text="Endereço:")
            address_label_name.grid(row=0, column=0, padx=5, pady=2, sticky="w")

            address_entry_value = ttk.Label(connection_frame, text=f"{listEnderNumber_server[i]}")
            address_entry_value.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

            interval_label_name= ttk.Label(connection_frame, text="Intervalo:")
            interval_label_name.grid(row=1, column=0, padx=5, pady=2, sticky="w")

            interval_label_value = ttk.Label(connection_frame, text=f"{listInterval_server[i]}")
            interval_label_value.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

            even_label_name = ttk.Label(connection_frame, text="Pares:")
            even_label_name.grid(row=2, column=0, padx=5, pady=2, sticky="w")

            even_label_value = ttk.Label(connection_frame, text=f"{listEvenNumber_server[i]}")
            even_label_value.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

            odd_label_name = ttk.Label(connection_frame, text="Ímpares:")
            odd_label_name.grid(row=3, column=0, padx=5, pady=2, sticky="w")

            odd_label_value = ttk.Label(connection_frame, text=f"{listOddNumber_server[i]}")
            odd_label_value.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

            number_label_name = ttk.Label(connection_frame, text="Valor:")
            number_label_name.grid(row=4, column=0, padx=5, pady=2, sticky="w")

            calcNumber_label_value = ttk.Label(connection_frame, text=f"{listCalcNumber_server[i]}")
            calcNumber_label_value.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        # Atualiza a visualização da tela e a configuração da barra de rolagem
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scrollbar.set)
        scrollbar.grid(row=5, column=2, sticky="ns")

    # Cria a janela principal
    root = tk.Tk()
    root.title("Connection Details")
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

    # Adiciona widgets à janela principal
    connections_label = ttk.Label(main_frame, text="Número de conexões:")
    connections_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    connections_entry = ttk.Entry(main_frame)
    connections_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    terms_label = ttk.Label(main_frame, text="Número de termos:")
    terms_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    terms_entry = ttk.Entry(main_frame)
    terms_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    finalResult_label_name = ttk.Label(main_frame, text="Resultado Final:")
    finalResult_label_name.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    finalResult_label_value = ttk.Label(main_frame)
    finalResult_label_value.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    elapsedTime_label_name = ttk.Label(main_frame, text="Tempo Decorrido (s):")
    elapsedTime_label_name.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    elapsedTime_label_value = ttk.Label(main_frame)
    elapsedTime_label_value.grid(row=3, column=1, padx=10, pady=5, sticky="ew")


    start_button = ttk.Button(main_frame, text="Start Connections", command=start_connections)
    start_button.grid(row=4, column=0, columnspan=2, pady=10)
    canvas = tk.Canvas(main_frame)
    canvas.grid(row=5, column=0, columnspan=2, sticky="nsew")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scrollbar.set)
    root.mainloop()


if __name__ == "__main__":
    createInterface()