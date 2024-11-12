#!/bin/bash
chmod +x Lettura_File_Config.sh
source Lettura_File_Config.sh
#____________________________________________
ip_server=$(ini_get_value server ip)
port_tcp=$(ini_get_value server port_tcp)
port_udp=$(ini_get_value server port_udp)
traffic=$(ini_get_value client traffic)

#____________________________________________
python3 Client.py --server_host "$ip_server" --tcp_port 8080 --udp_port 8081 --traffic "$traffic"
wait $!
