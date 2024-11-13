#!/bin/bash
chmod +x Lettura_File_Config.sh
source Lettura_File_Config.sh
#____________________________________________
ip_server=$(ini_get_value server ip)
port_tcp=$(ini_get_value server port_tcp)
port_udp=$(ini_get_value server port_udp)
intervals=$(ini_get_value client intervals)
traffic=$(ini_get_value client traffic)
payload=$(ini_get_value client payload)
#____________________________________________
python Client.py --server_host "$ip_server" --tcp_port "$port_tcp" --udp_port "$port_udp" --interval "$intervals" --traffic "$traffic" --payload "$payload"
wait $!
