#!/usr/bin/env python

import socket
import struct
import re
import sys
#import pprint
#import binascii
#import datetime
#import itertools
from BeautifulSoup import BeautifulSoup as Soup
import xml.etree.ElementTree as ET


MCAST_GRP_START = '239.0.2.129'
MCAST_PORT = 3937

def getxmlfile(MCAST_GRP,MCAST_PORT,DISCNAME):
	xmldata=""
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.settimeout(3)
	sock.bind(('', MCAST_PORT))
	mreq = struct.pack("=4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	while True:
		data = sock.recv(1500)
		start = data.find("<?xml")
		if(start!=-1):
			isourservice=data.find(DISCNAME)
			if(isourservice!=-1):
				xmldata+=data[start:]
				#print data[start:],
				while True:
					data = sock.recv(1500)
					start = data.find("</ServiceDiscovery>")
					if(start!=-1):
						xmldata+=data[12:start+19]
						#print data[13:start+19],
						return(xmldata)
					else:
						xmldata+=data[12:]
					#print data[13:],
				

if len(sys.argv) < 2:
	print "USO: imagenio.py TUPROVINCIA"
	print "Donde tu provincia es el numero que corresponda de los siguientes:"
	print "24. Galicia"
	print "19. Madrid"
	print "1. Cataluna"
	print "15. Andalucia"
	print "34. Aragon"
	print "13. Asturias"
	print "29. Cantabria"
	print "38. Castilla la Mancha"
	print "4. Castilla y Leon"
	print "6. Comunidad Valenciana"
	print "32. Extremadura"
	print "10. Islas Baleares"
	print "37. Islas Canarias"
	print "31. La Rioja"
	print "12. Murcia"
	print "35. Navarra"
	print "36. Pais Vasco"
	sys.exit(1)

provincia=sys.argv[1]

# conseguir la ip de servicio de la provincia
xmlfile=getxmlfile(MCAST_GRP_START,MCAST_PORT,'ServiceProviderDiscovery')
regexp = re.compile("DEM_" + str(provincia) +  "\..*?Address\=\\\"(.*?)\\\".*?",re.DOTALL)
ipprovincia = regexp.findall(xmlfile)[0]

# conseguir la lista de canales
xmlfile=getxmlfile(ipprovincia,MCAST_PORT,'BroadcastDiscovery')

#soup = Soup(Soup(xmlfile).prettify())
#print soup
#soup=Soup(xmlfile)

#channel= soup.findAll('singleservice')
#print channel
#for channel in  soup.findAll('singleservice'):
#	print channel
root = ET.fromstring(xmlfile)


for child in root.findall(".//{urn:dvb:ipisdns:2006}ServiceDiscovery"):
	print child.tag
	print child.attrib

