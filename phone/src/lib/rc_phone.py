""""
=======================
  RController 
=======================
(c) 2009 Marcel Caraciolo e Dimas Gabriel
Released under the GNU General Public License
"""

import os, btsocket, struct

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
	
	if not interactive:
		#try all previous services
		for service in default_services:
			sock = connect2service(service)
			if sock:
				return sock
				
	#interactive connect
	service = discover_address()
	
	if service:
		config['default_services'].append(service)
		#Make sure the configuration file exists
		if not os.path.isdir(os.path.dirname(config_file_path)):
			os.makedirs(os.path.dirname(config_file_path))
		#store the configuration file
		open(config_file_path,'wt').write(repr(config))
		return connect2service(service)
	else:
		print 'No service choosen'
		return None
		
def connect2service(service):
	"""
	service: (name,addr,port)
	"""
	print 'Connecting to %s on %s port %d ...' %service
	try:
		sock = btsocket.socket(btsocket.AF_BT, btsocket.SOCK_STREAM)
		#sock.connect(service)
		sock.connect(service[-2:])
		return sock
	except Exception, e:
		print 'Failed to connect: %s' % e
		return None
	

def discover_address():
	"""
		the user is prompted to select device and service
	"""
	import appuifw
	print "Discovering..."
	address, services = btsocket.bt_discover()
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