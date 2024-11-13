# Autore: Enrico Brunelli
# Data Creazione: 12/11/2024
# Data Ultima Modifica: 12/11/2024
# 
# Titolo: "Client per test su Firecell Labkit"
#____________________________________________________________

# Librerie utilizzate 
import ntplib # Libreria per l'utilizzo di server NTP 
import socket # Libreria per la gestione delle comunicaioni
import threading # Permette la gestione di più funzioni 
                # contemporaneamente
import argparse # Permette di avviare il programma passando
                # dei parametri 
from datetime import datetime # Permette di riconoscere il 
                              # formato dei timestamp
#___________________________________________________________  
# Funzione per l'ottenimento del timestamp dal server NTP
def get_ntp_timestamp(ntp_client): # ntp_client: oggetto per 
                                   # la comunicazione con il 
                                   # server
    server = 'ntp1.inrim.it' # Nome di del server 
                             # NTP di riferimento
    try:
        response = ntp_client.request(server, version=3,
                                      timeout=1)
        response=response.tx_time
    except Exception as e:
        print(f"Errore nella connessione:{e}")
        response = 0
    return response 
#___________________________________________________________
# Funzione per la gestione della connessione TCP
def handle_tcp_connection(server_socket,client_address,ntp_client,file):
    """
    Gestisce una connessione TCP con il client.

    Args:
        client_socket (socket): Il socket connesso al client.
        client_address (tuple): L'indirizzo del client.
        ntp_client : Oggetto client ntp per la richiesta al server
    """
    print(f"TCP Connection from {client_address}")
    try:
        while True:
            data, _ = server_socket.recvfrom(1024)
            if not data:
                break
            print(f"Messaggio ricevuto: {data.decode()}")
            # Ottieni il timestamp NTP attuale
            server_recv_timestamp = get_ntp_timestamp(ntp_client)
            # Risponde al client con il timestamp del server
            server_send_timestamp = get_ntp_timestamp(ntp_client)
            server_socket.sendto(str(server_send_timestamp).encode(), client_address)
            print(f"Messaggio mandato: {str(server_send_timestamp)}")
            file.write('TCP'+','+str(server_send_timestamp)+','+str(server_recv_timestamp)+'\n')
    except Exception as e:
        print(f"Errore nella connessione TCP: {e}")
    finally:
        server_socket.close()
        file.close()
        print(f"Connessione chiusa con:{client_address}")

#_______________________________________________________________________
#Funzione per l'avvio del server TCP sull'indirizzo IP e porta passati come 
#argomenti, rispettivamente, host e port
def tcp_server(host, port):
    """
    Avvia un server TCP.

    Args:
        host (str): Indirizzo IP su cui il server e' in ascolto.
        port (int): Porta su cui il server e' in ascolto.
    """
    ntp_client = ntplib.NTPClient()
    data_corrente = datetime.now()
    data_stringa = data_corrente.strftime("%Y-%m-%d")
    filecsv="server_istanti_temporali_"+data_stringa+".csv"
    file=open(filecsv,"a")
    if file.tell()==0:
        file.write("server_send_timestamp,server_recv_timestamp\n")
        print("File csv creato.")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server TCP in ascolto su {host}:{port}")
    file.close()
    try:
        while True:
            file=open(filecsv,"a")
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_tcp_connection,args=(client_socket, client_address, ntp_client,file)).start()
    except KeyboardInterrupt:
        print("\nArrtesto del server TCP")
    finally:
        file.close()
        server_socket.close()
    
#_____________________________________________________________________________
#Funzione per l'avvio del server UDP sull'indirizzo IP e porta passati come 
#argomenti, rispettivamente, host e port
def udp_server(host, port):
    """
    Avvia un server UDP.

    Args:
        host (str): Indirizzo IP su cui il server e' in ascolto.
        port (int): Porta su cui il server e' in ascolto.
    """
    ntp_client =ntplib.NTPClient()
    data_corrente = datetime.now()
    data_stringa = data_corrente.strftime("%Y-%m-%d")
    filecsv="server_istanti_temporali_"+data_stringa+".csv"
    file=open(filecsv,"a")
    if file.tell()==0:
        file.write("server_send_timestamp,server_recv_timestamp\n")
        print("File csv creato.")
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host, port))
    print(f"Server UDP in ascolto su {host}:{port}")

    try:
        while True:
            data, client_address = udp_socket.recvfrom(1024)
            server_recv_timestamp = get_ntp_timestamp(ntp_client)
            print(f"Ricevuto messaggio da {client_address}: {data.decode()}")
            server_send_timestamp = get_ntp_timestamp(ntp_client)
            udp_socket.sendto(data, client_address)
            file.write('UDP'+','+str(server_send_timestamp.tx_time)+','+str(server_recv_timestamp.tx_time)+'\n')
    except KeyboardInterrupt:
        print("\nArresto del server UDP.")
    finally:
        udp_socket.close()
    
#__________________________________________________________________________________
# Funzione principale per l'avvio del programma server
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Client TCP e UDP per il test della connessione.')
    parser.add_argument('--server_host', type=str, required=True, help='Indirizzo IP del server')
    parser.add_argument('--tcp_port', type=int, required=True, help='Porta del server TCP')
    parser.add_argument('--udp_port', type=int, required=True, help='Porta del server UDP')

    args = parser.parse_args()

    threading.Thread(target=tcp_server, args=(args.server_host, args.tcp_port)).start()
    threading.Thread(target=udp_server, args=(args.server_host, args.udp_port)).start()
