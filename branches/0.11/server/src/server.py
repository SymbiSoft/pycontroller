""""
=======================
  macMote - Server
=======================
(c) 2009 Marcel Caraciolo and Dimas Gabriel
e-mail: caraciol@gmail.com , dimas@dimasgabriel.net
Released under the GNU General Public License
"""

import lightblue

s = lightblue.socket()
s.bind(("",0))
s.listen(1)
lightblue.advertise("MacMote Server", s , lightblue.RFCOMM)
print "Server started..."
conn,addr = s.accept()
print "Connected by", addr

while 1:
	packet = conn.recv(1024)
 	if packet == "bye":
		break
	elif packet != None:
		print packet

conn.close()
s.close()
