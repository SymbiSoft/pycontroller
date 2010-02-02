""""
=======================
  macMote - Server
=======================
(c) 2009 Marcel Caraciolo and Dimas Gabriel
e-mail: caraciol@gmail.com , dimas@dimasgabriel.net
Released under the GNU General Public License
"""

try:
	import lightblue
except ImportError:
	print 'You have to install the lightblue library (http://lightblue.sourceforge.net/) before executing this program'
	exit()

try:
	import objc
except:
	print 'If you are having problems to execute this, check your MAC OS version (>=1.5) and run: /usr/bin/python server.py'
	exit()


s = lightblue.socket()
s.bind(("",0))
s.listen(1)
lightblue.advertise("MacMote Server", s , lightblue.RFCOMM)
print "Server started..."
conn,addr = s.accept()
print "Connected by", addr

bndl = objc.loadBundle('CoreGraphics', globals(), '/System/Library/Frameworks/ApplicationServices.framework')
objc.loadBundleFunctions(bndl, globals(), [('CGPostKeyboardEvent', 'iSSi')])
objc.loadBundleFunctions(bndl, globals(), [('CGPostMouseEvent', 'v{CGPoint=ff}III')])

state = 'main'
while 1:
	packet = conn.recv(1024)
	
	if packet == 'key':
		state = 'key'
	
	elif packet == 'main':
		state = 'main'
	
	if state == 'key' and packet == 'up':
		CGPostMouseEvent((300, 300), 1, 1, 1)
		CGPostMouseEvent((300, 300), 1, 1, 0)
			
	elif state == 'key' and packet == 'down':
		CGPostKeyboardEvent(0, 35, 1)
		CGPostKeyboardEvent(0, 35, 0)
			
	if packet == 'bye':
		print 'exiting...'
		break
		
conn.close()
s.close()
