# -*- coding: utf-8 -*-
"""
MacMote
Copyright (C) 2010  Marcel Caraciolo & Dimas Gabriel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.


MacMote
Copyright (C) 2010  Marcel Caraciolo & Dimas Gabriel
This program comes with ABSOLUTELY NO WARRANTY; for details see 
about box.
This is free software, and you are welcome to redistribute it
under certain conditions; see about box for details.
"""

from appuifw import *
import e32
from stopwatch import *
import key_codes
import pickle
import graphics
import os
import blueconnection


__all__= ['MacMote']
__author__ = 'Marcel Caraciolo (caraciol@gmail.com)'
__author__ += 'Dimas Gabriel (dimas.gabriel@dimagabriel.net)'
__version__ = '0.1.0'
__copyright__ = 'Copyright (c) 2010 - Marcel/Dimas'
__license__ = 'GPLv3'

WHITE = (255,255,255)
BLACK = (0,0,0)


class ClientGui(object):
	def __init__(self,server,macmote):
		self.server = server
		self.macmote = macmote
		self._canvas = None
		self._dblbuf = None
		self.lb = None
		self.main_menu()
		
	def OnCanvasEvent(self,event):
		if event['type'] == key_codes.EButton1Up:
			if event['pos'][0] < 260 and event['pos'][0] > 90 and event['pos'][1] > 70 and event['pos'][1] < 250:
				self.server.send_command('up',None)
			elif event['pos'][0] < 260 and event['pos'][0] > 90 and event['pos'][1] > 320 and event['pos'][1] < 480:
				self.server.send_command('down',None)
				
	def OnCanvasUpdate(self,rect):
		if (self._canvas and self._dblbuf):
			self._canvas.blit(self._dblbuf)
	
	def start_clock(self):
		self.clock.toggle()
		
	def reset_clock(self):
		self.clock.reset_counter()
	
	def shout(self):
		index = self.lb.current()
		if index == 0: #KeyNote
			app.screen = 'large'
			self._canvas = Canvas(redraw_callback = self.OnCanvasUpdate, event_callback = self.OnCanvasEvent)
			self._dblbuf = graphics.Image.new(self._canvas.size)
			app.body = self._canvas
			self._canvas.clear(BLACK)
			menu = [(u'Start/Pause',self.start_clock),
					(u'Reset/Stop',self.reset_clock),
	 				(u'Back To Menu',self.back_main_menu)]
			app.menu = menu
			self.clock = StopWatch()
			self.clock.set_msec(False)
			self.clock.magic_delta = 0
			w,h = self._canvas.size
			self.clock.set_position(w/3,h/10)
			self.server.send_command('key',None)
			self.server.run(self)
	
	def draw_clock(self):
		self.clock.update(self._dblbuf)
		self.OnCanvasUpdate(None)
		
	def draw_keys(self,pressed):
		self._dblbuf.clear(BLACK)
		if pressed == 'up':
			self._dblbuf.blit(self.macmote.icons[3],target=(50,50))
		elif pressed == 'down':
			self._dblbuf.blit(self.macmote.icons[2],target=(50,50))
		else:
			self._dblbuf.blit(self.macmote.icons[1],target=(50,50))
			
	def disconnect(self):
		self.server.quit()
		self.server.sock.close()
		self.macmote.first_menu()
	
	def about_mm(self):
		self.macmote.about_mm()
		
	def back_main_menu(self):
		self.server.closeApp()
		self.main_menu()
			
	
	def main_menu(self):
		app.title = u'MacMote'
		app.screen = 'normal'
		entries = [u'Slides', u'Front Row', u'Mouse']
		app.body = self.lb = Listbox(entries,self.shout)
		menu = [(u'Disconnect',self.disconnect),
 				(u'About',self.about_mm)]
		app.menu = menu
		

class BluetoothClient(object):
	def __init__(self,sock):
		self.command = e32.ao_callgate(self.send_command)
		self.write_lock = None
		self.sock = sock
		self.state = 'idle'
		self.timeI = 0

		
	def run(self,gui):
		self.gui = gui
		self.finished = False

		try:
			while not self.finished:
				self.check_pressed()
				self.gui.draw_keys(self.state)
				self.gui.draw_clock()
				e32.ao_yield()

		except:
			if not self.finished:
				note(u'Problems in the execution! Restart the app!', 'error')
	
	def check_pressed(self):
		if self.state == 'up' or self.state == 'down':
			self.timeI += 1
		
		if self.timeI == 5:
			self.timeI = 0
			self.state = 'idle'
		

	def send_command(self,cmd,event):
		if self.write_lock:
			self.write_lock.acquire()
		
		try:
			if cmd == 'bye':
				self.sock.send('bye')
			elif cmd == 'key':
				self.sock.send('key')
			elif cmd == 'main':
				self.sock.send('main')
			elif cmd == 'up':
				self.state = 'up'
				self.sock.send('up')
			elif cmd == 'down':
				self.state = 'down'
				self.sock.send('down')
		except Exception, e:
				pass
				
		if self.write_lock:
			self.write_lock.release()

	def quit(self):
		self.send_command('bye',None)
		self.finished = True
		
	def closeApp(self):
		self.send_command('main',None)
		self.finished = True



class MacMote(object):
	MMDEFDIR = u''
	MMDBNAME = u''
	MMICONNAME= u''
	MMVERSION = u'0.1.0'
	NL = u'\u2029'
	
	def __init__(self,path=u'e:\\python'):
		MacMote.MMDEFDIR = path
		MacMote.MMDBNAME = os.path.join(path,u'macmote.bin')
		MacMote.MSICONNAME = os.path.join(path,u'macmote.mif')
		app.exit_key_handler = self.close_app
		app.orientation = 'portrait'
		self.client = None
		self.loadIcons()
		self.first_menu()
		self.lock = e32.Ao_lock()
	
	def first_menu(self):
		app.screen = 'large'
		self.sock = None
		app.directional_pad = False
		menu = [(u'Connect',self.connect),
 				(u'About',self.about_mm)]
		self.img = None
		self.body_canvas = Canvas(redraw_callback = self.handle_redraw)
		self.img = graphics.Image.new(self.body_canvas.size)
		app.body = self.body_canvas
		self.body_canvas.clear(WHITE)
		self.showMainLogo()
		self.handle_redraw(None)
		app.menu = menu
		app.title = u'MacMote'
	
	
	def showMainLogo(self):
		w,h = self.body_canvas.size
		self.img.blit(self.icons[0],target=(w/5,h/4))
	
	def handle_redraw(self,rect):
		if self.img:
			self.body_canvas.blit(self.img)
	
	def load_cfg(self):
		try:
			f = open(MacMote.MMDBNAME,'rb')
			config = pickle.load(f)
			f.close()
			return config
		except Exception, e:
			if os.path.exists(MacMote.MMDBNAME):
				note(u'Impossible to load config from ' + 
						MacMote.MMDBNAME + u". " + unicode(str(e)),"error")
			return None

	def save_cfg(self,config):
		try:
			f = open(MacMote.MMDBNAME,'wb')
			pickle.dump(config,f)
			f.close()
		except Exception,e:
			note(u'Impossible to save config to file ' +
					MacMote.MMDBNAME + 
					u'. ' + unicode(str(e)), 'error')
					
	def connect(self):
		config = self.load_cfg()
		if config:  #It has a connection saved
			msg = u'Do you want to try the last connection saved\n from ' + unicode(config['services'][0]) + u' ?'
			op = query(msg,'query')
			if op is not None:
				sock, config = blueconnection.connect_phone2PC(config)
			else:
				sock, config = blueconnection.connect_new_phone2PC()
				if sock != None and config != None:
					self.save_cfg(config)
		else:  #New connection
			sock, config = blueconnection.connect_new_phone2PC()
			if sock != None and config != None:
				self.save_cfg(config)
		
		if sock:
			self.sock = sock
			#try:
			self.client = BluetoothClient(sock)
			gui = ClientGui(self.client,self)
			
			#client.quit()
			#except Exception,e:
			#	note(u'Lost the connection.','error')
			#sock.close()
			
	
	def about_mm(self):
		note(u'MacMote by:\n' +
		 	 u'Marcel Caraciolo and\n' +
			 u'Dimas Gabriel','info')

	def close_app(self):
		if self.sock:
			self.client.quit()
			self.sock.close()
		self.lock.signal()
		app.menu = []
		app.body = None
		self.body_canvas = None
		
	def loadIcons(self):
		imgs = [u'logo.png', u'keys.png', u'keysD.png', u'keysU.png']
		self.icons = []
		for img in imgs:
			self.icons.append(graphics.Image.open(os.path.join(MacMote.MMDEFDIR,img)))
	
	def run(self):
		self.lock.wait()
	

if __name__ == '__main__':
	import os
	dirF = os.sep.join(['c:','Data','python'])
	mm = MacMote(unicode(dirF))
	mm.run()