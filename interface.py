#interface.py

import tkinter as tk
from tkinter import ttk

import client
import server
import multiprocessing

HOST_SERVER = 'localhost'
HOST_CLIENT = '127.0.0.1'
PORT = 50000


def createInterface():
    def start_connections():
        NUM_CONNECTIONS = int(connections_entry.get())
        NUM_TERMS = int(terms_entry.get())

        result_queue = multiprocessing.Queue()
        ender_queue = multiprocessing.Queue()
        interval_queue = multiprocessing.Queue()
        number_queue = multiprocessing.Queue()
        odd_queue = multiprocessing.Queue()
        even_queue = multiprocessing.Queue()
        server_process = multiprocessing.Process(target=server.start, args=(HOST_SERVER, PORT, NUM_CONNECTIONS, NUM_TERMS, result_queue, ender_queue, interval_queue, number_queue, odd_queue, even_queue))
        server_process.start()


        print('Connections:')
        for i in range(NUM_CONNECTIONS):
            client.connect(HOST_CLIENT, PORT)
        server_process.join()

        result_server = result_queue.get()
        ender_server = ender_queue.get()
        interval_server = interval_queue.get()
        number_server = number_queue.get() #O ERRO ESTÁ AQUI
        odd_server = odd_queue.get() #O ERRO ESTÁ AQUI
        even_server = even_queue.get() #O ERRO ESTÁ AQUI

        print('\n\nPI result:', result_server)

        resultlabel2.config(text=f"{result_server}")
        for i in range(NUM_CONNECTIONS):
            connection_frame = ttk.LabelFrame(canvas, text=f'CONEXÃO {i+1}')
            canvas.create_window((0, i*140), window=connection_frame, anchor="nw")

            address_label = ttk.Label(connection_frame, text="Endereço:")
            address_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")

            address_entry = ttk.Label(connection_frame, text=f"{ender_server[i]}")
            address_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

            interval_label = ttk.Label(connection_frame, text="Intervalo:")
            interval_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")

            interval_entry = ttk.Label(connection_frame, text=f"{interval_server[i]}")
            interval_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

            even_label = ttk.Label(connection_frame, text="Pares:")
            even_label.grid(row=2, column=0, padx=5, pady=2, sticky="w")

            even_entry = ttk.Label(connection_frame, text=f"{even_server[i]}")
            even_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

            odd_label = ttk.Label(connection_frame, text="Ímpares:")
            odd_label.grid(row=3, column=0, padx=5, pady=2, sticky="w")

            odd_entry = ttk.Label(connection_frame, text=f"{odd_server[i]}")
            odd_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

            pi_label = ttk.Label(connection_frame, text="Valor:")
            pi_label.grid(row=4, column=0, padx=5, pady=2, sticky="w")

            pi_entry = ttk.Label(connection_frame, text=f"{number_server[i]}")
            pi_entry.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scrollbar.set)
        scrollbar.grid(row=4, column=2, sticky="ns")

    root = tk.Tk()
    root.title("Connection Details")
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

    connections_label = ttk.Label(main_frame, text="Número de conexões:")
    connections_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    connections_entry = ttk.Entry(main_frame)
    connections_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    terms_label = ttk.Label(main_frame, text="Número de termos:")
    terms_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    terms_entry = ttk.Entry(main_frame)
    terms_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    resultlabel = ttk.Label(main_frame, text="Resultado Final:")
    resultlabel.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    resultlabel2 = ttk.Label(main_frame)
    resultlabel2.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    start_button = ttk.Button(main_frame, text="Start Connections", command=start_connections)
    start_button.grid(row=3, column=0, columnspan=2, pady=10)
    canvas = tk.Canvas(main_frame)
    canvas.grid(row=4, column=0, columnspan=2, sticky="nsew")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scrollbar.set)
    root.mainloop()


if __name__ == "__main__":
    createInterface()