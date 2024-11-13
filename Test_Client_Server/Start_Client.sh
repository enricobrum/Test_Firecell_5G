#!/bin/bash
chmod +x Lettura_File_Config.sh
source Lettura_File_Config.sh
#____________________________________________
ip_server=$(ini_get_value server ip)
echo "$ip_server"
port_tcp=$(ini_get_value  port_tcp)
port_udp=$(ini_get_value  port_udp)
intervals=$(ini_get_value intervals)
traffic=$(ini_get_value  traffic)
payload=$(ini_get_value  payload)
#____________________________________________

python3 Client.py --server_host "$ip_server" --tcp_port "$port_tcp" --udp_port "$port_udp" --interval "$intervals" --traffic "$traffic" --payload "$payload"
wait $!
