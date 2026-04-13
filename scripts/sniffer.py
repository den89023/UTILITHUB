# UtilHub Sniffer
# Simulates packet sniffing

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hub_api import hub_print
import time

def main():
    hub_print("Starting packet sniffer...", "blue")
    time.sleep(1)
    packets = [
        "HTTP GET /index.html",
        "DNS query for example.com",
        "TCP SYN from 192.168.1.10",
        "UDP packet to port 53"
    ]
    for packet in packets:
        hub_print(f"Captured: {packet}", "yellow")
        time.sleep(0.5)
    hub_print("Sniffing stopped.", "green")

if __name__ == "__main__":
    main()