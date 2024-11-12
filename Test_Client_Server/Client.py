# Autore: Enrico Brunelli
# Data Creazione: 12/11/2024
# Data Ultima Modifica: 12/11/2024
# 
# Titolo: "Client per test su Firecell Labkit"
#____________________________________________________________

# Librerie utilizzate 
import ntplib # Libreria per l'utilizzo di server NTP 
import socket 
import time
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
    except Exception as e:
        print(f"Errore nella connessione:{e}")
        response = 0
    return response 
#___________________________________________________________    
# Funzione che implementa il test tramite connessione TCP
def test_tcp(client_socket,ntp_client,file):
    # Richiesta al server NTP prima di mandare il messaggio 
    # di test
    payload_size = 10 # Dimensione in Byte del messaggio 
                      # pari a quella del pacchetto di 
                      # risposta del server NTP per 
                      # mantenere la coerenza
    client_send_timestamp = get_ntp_timestamp(ntp_client)
    if client_send_timestamp != 0: # Se la richiesta al 
                                   # al server è andata a
                                   # buon fine
        message = "X" * payload_size # Generazione di un
                                     # pacchetto da 10 Bytes
        try:
            client_socket.sendall(message)
            response = client_socket.recv(1024)
            client_recv_timestamp = get_ntp_timestamp(ntp_client)
            if client_recv_timestamp != 0:
                file.write('TCP'+','+traffic+','+str(client_send_timestamp)+','+str(client_recv_timestamp)+'\n')
        except Exception as e:
            print(f"Errore nella connessione:{e}")

#___________________________________________________________    
#Funzione per la connessione TCP con il server
def connect_to_server(host, port):
    """
    Crea e stabilisce una connessione TCP con il server specificato.

    Args:
        host (str): Indirizzo IP del server.
        port (int): Porta su cui il server e' in ascolto.

    Returns:
        socket: Oggetto socket connesso al server.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connesso al server {host}:{port}")
    return client_socket
#_____________________________________________________________
#Funzione di test che permette l'invio di messaggi UDP.
def test_udp(host, port, ntp_client):
    """
    Esegue un test UDP inviando pacchetti al server e ricevendo risposte.

    Args:
        host (str): Indirizzo IP del server.
        port (int): Porta su cui il server UDP e' in ascolto.
        file (File): File .csv per il salvataggio dei dati
        traffic (str): scenario di traffico del test corrente 
    """
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_send_timestamp = get_ntp_timestamp(ntp_client)
    udp_socket.sendto(client_send_timestamp.tx_time.encode(), (host, port))
    response = udp_socket.recvfrom(1024)
    client_recv_timestamp = get_ntp_timestamp(ntp_client)
    udp_socket.close()
    return client_recv_timestamp.tx_time,client_send_timestamp.tx_time
#_____________________________________________________________________
# Programma principale che permette la gestione del test, le connessioni 
# con i vari protocolli e la ricezione di parametri in ingresso all'avvio
def run_test_cycle(host, tcp_port, udp_port,traffic):
    """
    Esegue un ciclo di test di rete per ciascun intervallo specificato.

    Args:
        host (str): Indirizzo IP del server.
        tcp_port (int): Porta del server TCP.
        udp_port (int): Porta del server UDP.
        traffic (str): Scenario di traffico del test corrente
    """
    n_test=5
    ntp_client =ntplib.NTPClient()
    data_corrente = datetime.now()
    data_stringa = data_corrente.strftime("%Y-%m-%d")
    filecsv="istanti_temporali_"+data_stringa+".csv"
    file=open(filecsv,"a")
    if file.tell()==0:
        file.write("Protocollo,Traffico,client_send_timestamp,client_recv_timestamp\n")
        print("File csv creato.")
    while True:
        print("\nSeleziona un test da eseguire:")
        print("1. Protocollo TCP")
        print("2. Protocollo UDP")
        print("3. Terminazione del test.")
        scelta = input("Inserisci il numero del test da eseguire: ")
        if scelta == '1':
            print("\nEsecuzione Test con protocollo TCP:")
            client_socket = connect_to_server(host, tcp_port)
            try:
                for _ in range(n_test):
                    test_tcp(client_socket,ntp_client,file)
                    time.sleep(1)
            finally:
                client_socket.close()
                print("Connessione al server chiusa dopo il test")

        elif scelta == '2':
            print("\nEsecuzione Test con protocollo UDP:")
            for _ in range(n_test):
                    client_send_timestamp,client_recv_timestamp = test_udp(host,udp_port,ntp_client)
                    file.write('UDP'+','+traffic+','+str(client_send_timestamp)+','+str(client_recv_timestamp)+'\n')
        elif scelta == '3':
            file.close()
            print("Uscita dal programma.")
            break
        else:
            print("Selezione non valida. Per favore, riprova.")
            
#Funzione principale che all'avvio del programma tramite l'oggetto "parser" consente di eseguire il codice
#specificando gli argomenti necessari alla realizzazione del test. Dopo aver aggiunto tutti gli argomenti
#passati al lancio del programma python, viene eseguita la funzione "run_test_cycle" e si entra nella fase
#di test. 
if __name__ == "__main__":
    """
        server_host: Indirizzo IP del server
        tcp_port: Porta del server TCP
        udp_port: Porta del server UDP
        intervals: Intervalli di tempo tra i messaggi
        traffic: Scenario di traffico del test
        payload: Dimensioni crescenti del payload per test
    
    """
    parser = argparse.ArgumentParser(description='Client TCP e UDP per il test della connessione.')
    parser.add_argument('--server_host', type=str, required=True, help='Indirizzo IP del server')
    parser.add_argument('--tcp_port', type=int, required=True, help='Porta del server TCP')
    parser.add_argument('--udp_port', type=int, required=True, help='Porta del server UDP')
    parser.add_argument('--traffic', type=str, required=True, help="Scenario di traffico del test")
    args = parser.parse_args()

    run_test_cycle(args.server_host, args.tcp_port, args.udp_port, args.traffic)
