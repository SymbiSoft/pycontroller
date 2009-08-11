""""
=======================
  RController 
=======================
(c) 2009 Marcel Caraciolo e Dimas Gabriel
Released under the GNU General Public License
"""



import appuifw, graphics, e32, sysinfo, os
from types import IntType
import rc_phone


ALWAYS_ASK_FOR_BLUETOOTH_DEVICE = False
TEMP_DIR = 'd:' + os.sep
CONFIG_FILE = os.sep.join(['c:', 'System', 'Apps', 'Python', 'rc_com.cfg'])




def main(interactive = True):
	print 'rc_controler.py start ...'
	server_sock = rc_phone.connect_phone2PC(CONFIG_FILE, interactive = interactive)
	
	


if __name__ == '__main__':
	main(ALWAYS_ASK_FOR_BLUETOOTH_DEVICE)