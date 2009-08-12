import lightblue

s = lightblue.socket()
s.bind(("",0))
s.listen(1)
lightblue.advertise("Test Drive", s , lightblue.RFCOMM)
conn,addr = s.accept()
print "Connected by", addr
while 1:
	packet = conn.recv(1024)
	print packet
#conn.close()
#s.close()
