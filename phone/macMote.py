""""
=======================
  macMote 
=======================
(c) 2009 Marcel Caraciolo and Dimas Gabriel
e-mail: caraciol@gmail.com , dimas@dimasgabriel.net
Released under the GNU General Public License
"""

import os
import rc_phone
import time


from e32 import pys60_version
if ((pys60_version.split())[0] >= '1.9.1'):
	CONFIG_FILE = os.sep.join(['c:','Personal files','python','rc_com.cfg'])
else:
	CONFIG_FILE = os.sep.join(['e:','python','rc_com.cfg'])
   


def main():
	print "macMote.py start..."
	server_sock = rc_phone.connect_phone2PC(CONFIG_FILE)
	if server_sock:
		print 'Connected...'
		try:
			time.sleep(1)
			server_sock.send('Hello PC')
			time.sleep(2)
			server_sock.send('bye')
		except Exception,e:
			print 'something wrong sending data...'
			import traceback
			traceback.print_exc()
		server_sock.close()
	else:
		print 'macMote.py: could not connect.'
	print 'macMote3.py done.'

if __name__ == '__main__':
	main()