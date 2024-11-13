#!/bin/bash
#Programma utilizzato per l'avvio dei server da lato core 5G posti 
#sul nodo centrale della rete 5G Firecell. Inoltre e' anche configurato
#l'applicazione wireshark al fine di ottenere i valori dei time-stamp 
#relativi ai pacchetti scambiati nella fase di test della rete.
#_______________________________________________________________________________
#Importo i file contenenti le funzioni utilizzate per avviare e controllare
#i Client e server, la lettura del file di configurazione,
#la configurazione di client e server iperf e la configurazione dell'ascolto
#effettuato da wireshark.
chmod +x Lettura_File_Config.sh 
source Lettura_File_Config.sh #Lettura del file di configurazione contenenti
                              #i valori utilizzati per i test
ini_printdb
#_______________________________________________________________________________
ip_server=$(ini_get_value  ip) #indirizzo IP del server di echo
port_tcp=$(ini_get_value  port_tcp) #port in cui si pone il server di echo
port_udp=$(ini_get_value  port_udp)
#avvio del server con i parametri ottenuti da file di configurazione

python3 Server.py --server_host "$ip_server" --tcp_port 8080 --udp_port 8081 
wait $!

