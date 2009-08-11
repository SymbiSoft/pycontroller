""""
=======================
  RController 
=======================
(c) 2009 Marcel Caraciolo e Dimas Gabriel
Released under the GNU General Public License
"""

import os, socket, struct

def connect_phone2PC(config_file_path, interactive = True):
	"""
	config_file_path: Stores the services names, addresses and ports of previous connections
	interactive: If false Addresses from the config file are tried out
	             If None of them works, a service discovery is started and the user is prompted to choose a service
	"""
	
	try:
		config = eval(open(config_file_path,'r').read())
	except:
		config = {'default_services':[]}
		
	default_services = config.get('default_services',[])
	
	#interactive connect
	service = discover_address()
	
	print service


def discover_address():
	"""
		the user is prompted to select device and service
	"""
	import appuifw
	print "Discovering..."
	address, services = socket.bt_discover()
	print "Discovered: %s, %s" % (address, services)
	if len(services) > 1: #if this host offers more than one service, let the user choose the right one
		service_names = services.keys()
		service_names.sort()
		service_list = [unicode(name) for name in service_names]
		choice = appuifw.popup_menu(service_list, u'Choose service:')
		if choice == None:
			return None
		service_name = service_names[choice]
		port = services[service_name]
	else:
		service_name, port  = services.popitem()
	
	return (service_name,address, port)