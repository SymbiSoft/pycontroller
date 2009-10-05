""""
=======================
  macMote 
=======================
(c) 2009 Marcel Caraciolo and Dimas Gabriel
e-mail: caraciol@gmail.com , dimas@dimasgabriel.net
Released under the GNU General Public License
"""

import os,struct

from e32 import pys60_version
if ((pys60_version.split())[0] >= '1.9.1'):
    import btsocket as socket
else:
   import socket



def connect_phone2PC(config_file_path):
	import appuifw
	"""
	config_file_path: Stores the services names, adresses and ports of previous connections
	"""
	try:
		config = eval(open(config_file_path,'r').read())
	except:
		config = {'default_services': []}
	
	default_services = config.get('default_services',[])
	
	if len(default_services) > 0:
		selected = appuifw.popup_menu([u"Connect to the last saved", u"New device"])
		if selected == 0:
			#LastDevice
			service = default_services[0]
			sock = connect2service(service)
			if sock:
				return sock
		elif selected == None:
			print 'No device choosen'
			return None
	try:
		service = discover_address()
	except Exception:
		print "No device chosen"
		return None
		
	if service:
		config['default_services'].append(service)
		#Make sure the configuration file exists
		if not os.path.isdir(os.path.dirname(config_file_path)):
			os.makedirs(os.path.dirname(config_file_path))
		#store the configuration file
		open(config_file_path,"w").write(repr(config))
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
		sock = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
		sock.connect(service[-2:])
		return sock
		#sock.connect(service)
	except Exception, e:
		print 'Failed to connect: %s' %e
		return None

def discover_address():
	"""
		the user is prompted to select device and service
		
	"""
	import appuifw
	print "Discovering..."
	address, services = socket.bt_discover()
	print "Discovered: %s, %s" %(address, services)
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
	