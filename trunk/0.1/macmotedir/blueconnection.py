# -*- coding: utf-8 -*-
"""
MacMote
Copyright (C) 2010  Marcel Caraciolo & Dimas Gabriel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.


MacMote
Copyright (C) 2010  Marcel Caraciolo & Dimas Gabriel
This program comes with ABSOLUTELY NO WARRANTY; for details see 
about box.
This is free software, and you are welcome to redistribute it
under certain conditions; see about box for details.
"""



import os,struct

import btsocket as socket


def connect_phone2PC(config):
	'''
		Connect the phone to PC
		Parameters:
			config: Stores the services names, adressses and ports of previous connections
		Returns:
			the socket connection and the previous configuration
	'''
	service = config['services'][0]
	sock = connect2service(service)
	if sock:
		return (sock,config)
	else:
		return (None,None)
	

def connect_new_phone2PC():
	'''
		Makes a new connection
		Returns:
			the socket connection and configuration
	'''
	import appuifw
	config = {'services':[] }
	
	try:
		service = discover_address()
	except Exception:
		appuifw.note(u'No device chosen','error')
		return (None,None)
	
	if service:
		config['services'].append(service)
		sock = connect2service(service)
		return (sock,config)	
	else:
		appuifw.note(u'No service chosen','error')
		return (None,None)
	
			

def discover_address():
	"""
		the user is prompted to select device and service

	"""
	import appuifw
	#print "Discovering..."
	address, services = socket.bt_discover()
	#print "Discovered: %s, %s" %(address, services)
	if len(services) > 1: #if this host offers more than one service, let the user choose the right one
		service_names = services.keys()
		service_names.sort()
		service_list =[unicode(name) for name in service_names]
		choice = appuifw.popup_menu(service_list, u"Choose service:")
		if choice == None:
			return None
		service_name = service_names[choice]
		port  = services[service_name]
	else:
		service_name,port = services.popitem()

	return (service_name,address, port)	


def connect2service(service):
	import appuifw
	"""
	Connects to the service
	Parameters:
		service: (name,addr,port)
	Returns:
		the socket connection
	"""
	#print 'Connecting to %s on %s port %d ...' %service
	try:
		sock = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
		sock.connect(service[-2:])
		return sock
		#sock.connect(service)
	except Exception, e:
		appuifw.note(u'Failed to connect to the service', 'error')
		#print 'Failed to connect: %s' %e
		return None


		port  = services[service_name]
	else:
		service_name,port = services.popitem()
	
	return (service_name,address, port)	
	