from scapy.all import sniff, wrpcap

# Define the packet capture function
def packet_capture(packet):
    wrpcap('packet_capture.pcap', packet, append=True)

# Start capturing packets on the specified interface
interface_name = 'en0'  # Replace this with your interface name
sniff(iface=interface_name, prn=packet_capture)
