import psutil
import time

UPDATE_DELAY = 1 # in seconds

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024


# Network information
print("="*40, "Network Information", "="*40)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"==== Interface: {interface_name} ====")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast MAC: {address.broadcast}")

print(" ")            

# get the network I/O stats from psutil
io = psutil.net_io_counters()
# extract the total bytes sent and received
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv


# get the stats again
io_2 = psutil.net_io_counters()
# new - old stats gets us the speed
us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
# print the total download/upload along with current speeds
print( f"    Total Upload: {get_size(io_2.bytes_sent)}   "
    f", Total Download: {get_size(io_2.bytes_recv)}   "
    f", Upload Speed: {get_size(us / UPDATE_DELAY)}/s   "
    f", Download Speed: {get_size(ds / UPDATE_DELAY)}/s      ", end="\r")