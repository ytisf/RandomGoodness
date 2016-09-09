#!/usr/bin/env python
'''Remove GTP layer from PCAP file'''
import dpkt, struct, time, re, socket
import platform
import sys

# Check for arguments
if len(sys.argv) < 3 or len(sys.argv) > 3:
    print "Usage:\n", sys.argv[0], "input.pcap", "output.pcap"
    sys.exit()

# Open files for input and output
try:
    fi = open(sys.argv[1],'r')
    fo = open(sys.argv[2],'w')

    # Prepare PCAP reader and writter
    pcapin = dpkt.pcap.Reader(fi)
    pcapout = dpkt.pcap.Writer(fo)

    for ts, buf in pcapin:
        # make sure we are dealing with IP traffic
        # ref: http://www.iana.org/assignments/ethernet-numbers
        try: eth = dpkt.ethernet.Ethernet(buf)
        except: continue
        if eth.type != 2048: continue

        # make sure we are dealing with UDP
        # ref: http://www.iana.org/assignments/protocol-numbers/
        try: ip = eth.data
        except: continue
        if ip.p != 17: continue

        # filter on UDP assigned ports for GTP User
        # ref: http://www.iana.org/assignments/port-numbers
        try: udp = ip.data
        except: continue
        try:
            if udp.dport != 2152: continue
        except: continue

        # extract GTP flags to detect header length
        gtpflags = udp.data[:1]
        try:
            if gtpflags == '\x30': payload = udp.data[8:]
            elif gtpflags == '\x32': payload = udp.data[12:]
            else: continue
        except: continue

        # at this point we have a confirmed ETH/IP/UDP/GTP packet structure
        # UDP payload is GTP header + real user payload
        try:
            # append real user payload to ethernet layer and writeout
            eth.data = payload
            pcapout.writepkt(eth, ts)
        except: continue

    fi.close()
    fo.close()

except IOError as (errno, strerror):
    print "I/O error({0}): {1}".format(errno, strerror)
