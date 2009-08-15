import lightblue
import objc

s = lightblue.socket()
s.bind(("",0))
s.listen(1)
lightblue.advertise("Test Drive", s , lightblue.RFCOMM)
conn,addr = s.accept()
print "Connected by", addr

bndl = objc.loadBundle('CoreGraphics', globals(), '/System/Library/Frameworks/ApplicationServices.framework')
objc.loadBundleFunctions(bndl, globals(), [('CGPostMouseEvent', 'v{CGPoint=ff}III')])

while 1:
	packet = conn.recv(1024)
	if packet == "167":
		CGPostMouseEvent((300, 300), 1, 1, 1)
		CGPostMouseEvent((300, 300), 1, 1, 0)
	elif packet == "bye":
		break
		
conn.close()
s.close()
