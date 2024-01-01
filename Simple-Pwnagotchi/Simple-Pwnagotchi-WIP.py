from scapy.all import *
from wifi import Cell

def wifi_scan():
    print("Scanning for Wi-Fi networks...")
    ssid_list = set()

    # Use Scapy to sniff Wi-Fi packets
    sniff(iface="wlan0", prn=process_packet, timeout=10)  # Adjust iface as per your Wi-Fi interface

    # Use the wifi library to get available networks
    networks = Cell.all('wlan0')  # Adjust 'wlan0' to your Wi-Fi interface
    for network in networks:
        ssid_list.add(network.ssid)

    return ssid_list

def process_packet(pkt):
    if pkt.haslayer(Dot11Beacon):
        ssid = pkt[Dot11Elt].info.decode()
        ssid_list.add(ssid)
        print(f"SSID: {ssid}")

if __name__ == "__main__":
    wifi_networks = wifi_scan()
    print("Available Wi-Fi Networks:")
    for network in wifi_networks:
        print(network)

    # Write discovered SSIDs to a file
    with open("wifi_networks.txt", "w") as file:
        file.write("\n".join(wifi_networks))

    print("Discovered networks saved to wifi_networks.txt")
