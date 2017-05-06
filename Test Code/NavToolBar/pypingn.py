import os
import sys
import time
import socket
import struct
import select
from datetime import datetime


start = datetime.now()

if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

# From /usr/include/linux/icmp.h; your milage may vary.
ICMP_ECHO_REQUEST = 8  # Seems to be the same on Solaris.


def checksum(source_string):
    """
    I'm not too confident that this is right but testing seems
    to suggest that it gives the same answers as in_cksum in ping.c
    """
    sum_sc = 0
    count_to = (len(source_string) / 2) * 2
    count = 0
    while count < count_to:
        this_val = ord(source_string[count + 1]) * 256 + ord(source_string[count])
        sum_sc = sum_sc + this_val
        sum_sc = sum_sc & 0xffffffff  # Necessary?
        count = count + 2

    if count_to < len(source_string):
        sum_sc = sum_sc + ord(source_string[len(source_string) - 1])
        sum_sc = sum_sc & 0xffffffff  # Necessary?

    sum_sc = (sum_sc >> 16) + (sum_sc & 0xffff)
    sum_sc = sum_sc + (sum_sc >> 16)
    answer = ~sum_sc
    answer = answer & 0xffff

    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def receive_one_ping(my_socket, ps_id, timeout):
    """
    receive the ping from the socket.
    """
    time_left = timeout
    while True:
        started_select = default_timer()
        what_ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = (default_timer() - started_select)
        if not what_ready[0]:  # Timeout
            return

        time_received = default_timer()
        rec_packet, addr = my_socket.recvfrom(1024)
        icmp_header = rec_packet[20:28]
        ps_type, code, checksum, packet_id, sequence = struct.unpack(
            "bbHHh", icmp_header
        )
        # Filters out the echo request itself.
        # This can be tested by pinging 127.0.0.1
        # You'll see your own request
        if ps_type != 8 and packet_id == ps_id:
            bytes_in_double = struct.calcsize("d")
            time_sent = struct.unpack("d", rec_packet[28:28 + bytes_in_double])[0]
            return time_received - time_sent

        time_left = time_left - how_long_in_select
        if time_left <= 0:
            return


def send_one_ping(my_socket, dest_addr, ps_id):
    """
    Send one ping to the given >dest_addr<.
    """
    dest_addr = socket.gethostbyname(dest_addr)

    # Header is ps_type (8), code (8), checksum (16), ps_id (16), sequence (16)
    my_checksum = 0

    # Make a dummy heder with a 0 checksum.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ps_id, 1)
    bytes_in_double = struct.calcsize("d")
    data = (192 - bytes_in_double) * "Q"
    data = struct.pack("d", default_timer()) + data

    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ps_id, 1
    )
    packet = header + data
    my_socket.sendto(packet, (dest_addr, 1))  # Don't know about the 1


def ping(dest_addr, timeout):
    """
    Returns either the delay (in seconds) or none on timeout.
    """
    icmp = socket.getprotobyname("icmp")
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error, (errno, msg):
        if errno == 1:
            # Operation not permitted
            msg = msg + (
                " - Note that ICMP messages can only be sent from processes"
                " running as root."
            )
            raise socket.error(msg)
        raise  # raise the original error
    my_id = os.getpid() & 0xFFFF
    send_one_ping(my_socket, dest_addr, my_id)
    delay = receive_one_ping(my_socket, my_id, timeout)
    my_socket.close()
    return (datetime.now() - start).total_seconds(), delay*1000


import admin
#
# def run():
#     if not admin.isUserAdmin():
#         print "You're not an admin.", os.getpid(), "params: ", sys.argv
#         rc = admin.runAsAdmin()
#     else:
#         print "You're an admin.", os.getpid(), "params: ", sys.argv
#         rc = 0
#         print ping("104.160.131.3", 2)
#     x = raw_input('Press Enter to exit.')
#     return rc
#
#
# if __name__ == '__main__':
#     sys.exit(run())


