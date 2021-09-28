import socket
import time

# Constants
HOST  = '10.0.0.1'
PORT  = 12000
ALPHA = 0.125
BETA  = 0.25

# Variables
est_rtt = 0
dev_rtt = 0
packet_loss = 0
min_rtt = 0
max_rtt = 0
avg_rtt = 0
timeout_interval = 0

# Create socket object. SOCK_DGRAM parameter makes it a UDP Socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

    # A total of 10 PINGS will be sent from client to server.
    for x in range(1,11):

        try:

            data = "Ping" + str(x)
            # Send data to server encoded in byte format
            print('Mesg sent: ' + data)
            start_time = time.time()
            sock.sendto(data.encode(), (HOST, PORT))
            
            # Raise exception if socket takes more than one second to come back
            sock.settimeout(1)

            # Decode data into string and display data received from server 
            data = sock.recv(1024).decode()
            end_time = time.time()
            rtt = (end_time - start_time) * 1000

            # First RTT is set as the minimum RTT. If the next RTT is less 
            # than the current Min RTT then it's set as the new Min RTT
            if min_rtt == 0:
                min_rtt = rtt
            else:
                if min_rtt > rtt:
                    min_rtt = rtt

            # First RTT is set as the maximum RTT. If the next RTT is greater
            # than the current Max RTT then it's set as the new Max RTT
            if max_rtt == 0:
                max_rtt = rtt
            else:
                if max_rtt < rtt:
                    max_rtt = rtt

            # First Est RTT is set as the first RTT. Then the next est 
            # Est RTT's are calculated with the formula provided.
            if est_rtt == 0:
                est_rtt = rtt
            else:
                est_rtt = (1.0 - ALPHA) * est_rtt + ALPHA * rtt

            # First Dev RTT is set as the first RTT divided by 2. Then the  
            # next Dev RTT's are calculated with the formula provided.
            if dev_rtt == 0:
                dev_rtt = rtt / 2
            else:
                dev_rtt = ((1.0 - BETA) * dev_rtt) + (BETA * abs(rtt - est_rtt))

            # Total average RTT is first calculated by adding all the incoming RTTs.
            # Then it's divided by the number requests that weren't dropped. 
            avg_rtt += rtt

            # Values printed are: Message received, RTT, Estimated RTT and Deviation RTT.
            print('Mesg rcvd: ' + data)
            print('PONG ' + str(x) + ' RTT: ', str(rtt), 'ms')
            print('Est rtt: ', est_rtt, 'ms')
            print('Dev rtt: ', dev_rtt, "ms\n")

        # If packet is dropped increase count of packets lost.
        except Exception as e:
            print(e)
            print('No Mesg rcvd.')
            print('Timeout: Packet was lost.\n')
            packet_loss = packet_loss + 1

# After all pings are sent, avergae RTT, drop percentage, and timeout interval are calculated.
avg_rtt = avg_rtt / (10 - packet_loss)
percentage = 100 * float(packet_loss)/float(10)
timeout_interval = est_rtt + 4 * dev_rtt

# Values calculated above are printed.
print('MinRTT: ', min_rtt, " ms")
print('MaxRTT: ', max_rtt, " ms")
print('Packet Loss: ', percentage, "%")
print('Average RTT: ', avg_rtt, " ms")
print('Timeout Interval: ', timeout_interval)