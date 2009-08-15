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
import key_codes


ALWAYS_ASK_FOR_BLUETOOTH_DEVICE = False
#TEMP_DIR = 'd:' + os.sep
CONFIG_FILE = os.sep.join(['c:', 'DATA', 'python', 'rc_com.cfg'])


class ClientGui(object):
	def __init__(self,server):
		self.server = server
		
		appuifw.app.title = u'RController'
		appuifw.app.screen = 'full'
		appuifw.app.exit_key_handler = lambda: False
		
		self._canvas = appuifw.Canvas(redraw_callback = self.OnCanvasUpdate, event_callback = self.OnCanvasEvent)
		self._dblbuf = graphics.Image.new(sysinfo.display_pixels())
		self._sprite = graphics.Image.open("c:\\DATA\\python\\IpodBotoes.png")
		self.set_font()
		
	
		appuifw.app.body = self._canvas
		
		self.set_menu()
		self._lock = e32.Ao_lock()
	
	
	def OnCanvasEvent(self,event):
		self.server.command('cmd', event)
	
	def OnCanvasUpdate(self, rect):
		if(self._canvas and self._dblbuf):
			self._canvas.blit(self._dblbuf)
	
	
	default_font = {
		'size' : 6,
		'font' : 'normal',
		'bold' : -1,
		'italic' : -1,
		'fill' : 0x000000,
	}
	
	def set_font(self, **kwargs):
		self.font = {}
		for key in ClientGui.default_font.keys():
			if kwargs.has_key(key):
				self.font[key] = kwargs[key]
			else:
				self.font[key] = ClientGui.default_font[key]				
				
	text_align = {
		'left' : 0,
		'right' : -1,
		'center' : -0.5,
		'top' : 0.8,
		'bottom' : -0.2,
		'middle' : 0.3,
	}
			  
	box_align = {
		'left' : 0,
		'right' : -1,
		'center' : -0.5,
		'top' : 0,
		'bottom' : -1,
		'middle' : -0.5,
	}
			  
	def draw_text(self, text, x, y, h_align = 'left', v_align = 'middle', outline = False):
		lines = text.split('\n')
		bold = (self.font['bold'] != -1) * graphics.FONT_BOLD
		italic = (self.font['italic'] != -1) * graphics.FONT_ITALIC
		#font = (self.font['font'], int(self.font['size'] * 2.5), bold|italic|graphics.FONT_ANTIALIAS)
		font = 'dense' # TODO: tempoary fix, until tuple font specifications work when drawing on image
		text_width = 0
		font_height = 0
		for line in lines:
			text_box, cursor_move, max_chars = self._dblbuf.measure_text(line, font = font)
			text_width = max(text_width, text_box[2] - text_box[0])
			font_height = max(font_height, text_box[3] - text_box[1])
		x += int(text_width * ClientGui.text_align[h_align])
		line_height = font_height * 1.2 # 20% space between the lines
		y += line_height * (len(lines) - 1) * ClientGui.box_align[v_align]
		y += line_height * ClientGui.text_align[v_align]     # set y to the top of the area to draw the text in
		for line in lines:
			if outline: # draw outline in opposite color to increase contrast
		   		self._dblbuf.text((x - 1, int(y) - 1), line, fill = 0xffffff - self.font['fill'], font = font)
		   		self._dblbuf.text((x + 1, int(y) + 1), line, fill = 0xffffff - self.font['fill'], font = font)
			self._dblbuf.text((x , int(y)), line, fill = self.font['fill'], font = font)
			y += line_height
			
	
	def drawScreen(self,pressed):
			self._dblbuf.clear()
			x, y = sysinfo.display_pixels()
			if not pressed:
				self._dblbuf.blit(self._sprite,target=(int(x/3)+5, int(y/3)), source=(0,0,100,97))
			else:
				self._dblbuf.blit(self._sprite,target=(int(x/3)+5, int(y/3)), source=(0,97,100,194))
			
			self.OnCanvasUpdate(None)
			#self._dblbuf.rectangle((0,0))
			
			#self._iCanvas.rectangle((0,0,240,320), outline = 0xFFFFFF, width=240)
		
		
	def OnMenu(self, menu_cmd):
 		self.server.command(*menu_cmd.split(' '))
	
	def run(self):
	 	self._dblbuf.clear()
	 	self.OnCanvasUpdate(None)
		self._lock.wait()
		
	def OnExit(self):
	 	self.server.quit()
		self._lock.signal()
	
	
	def _parseMenuList(self, entries):
		menu = ()
		for (menu_text, menu_cmd) in entries:
			if type(menu_cmd) == str:
				menu += ((unicode(menu_text), lambda self=self, menu_cmd=menu_cmd: self.OnMenu(menu_cmd)),)
			else:
				menu += ((unicode(menu_text), self._parseMenuList(menu_cmd)),)
		return menu
	
	def set_menu(self, entries = []):
		#appuifw.app.menu = list(self._parseMenuList(entries))
		appuifw.app.menu = entries
		appuifw.app.menu.append((u'Exit', self.OnExit))
	
	
	
	
class BluetoothClient(object):
	
	def __init__(self,sock):
		self.command = e32.ao_callgate(self.send_command)
		self.write_lock = None
		self.sock = sock
		self.pressed = False
		self.event = False
		self.timeI = 0
	
	def checkPressed(self):
		if self.event:
			self.timeI = 0
			self.event = False
			self.pressed = True
		elif self.pressed:
			self.timeI += 1
			
		if self.timeI == 10:
			self.pressed = False
	
	def run(self,gui):
		self.gui = gui
		self.finished = False
		
		try:
			while not self.finished:
				#do something here
				self.checkPressed()
				self.gui.drawScreen(self.pressed)
				e32.ao_yield()
		except:
			if not self.finished:  #dont show errors when closing down the connection
				import traceback
				traceback.print_exc()
	
	def send_command(self,cmd,event):
		if self.write_lock:
			self.write_lock.acquire()
		try:
			if cmd == 'bye':
				self.sock.send('bye')
			elif cmd == 'cmd':
				if (event['type'] == appuifw.EEventKeyDown) and event['scancode'] == key_codes.EScancodeSelect:
					self.event = True
					self.sock.send(str(key_codes.EScancodeSelect))
					#print 'Select pressed!'
		
		except Exception, e:
			print 'something wrong sending data...'
	
		if self.write_lock:
			self.write_lock.release()
		
	
	def quit(self):
		self.send_command('bye',None)
		self.finished = True
	
	

def main(interactive = True):
	print 'rc_controler.py start ...'
	server_sock = rc_phone.connect_phone2PC(CONFIG_FILE, interactive = interactive)
	if server_sock:
		print 'Connected...'
		try:
			client = BluetoothClient(sock = server_sock)
			gui = ClientGui(client)
			x, y = sysinfo.display_pixels()
			gui.draw_text(u'RController\nwaiting for connection...', int(x/2), int(y/2),'center','middle')
			gui.OnCanvasUpdate(None)
			client.run(gui)
		except:
			print 'rc_controler.py: run failed.'
			import traceback
			traceback.print_exc()
		server_sock.close()
	else:
		print 'rc_controller.py: could not connect.'
	print 'rc_controller.py done.'

if __name__ == '__main__':
	main(ALWAYS_ASK_FOR_BLUETOOTH_DEVICE)
	
