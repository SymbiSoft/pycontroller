
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
along with this program. If not, see <http://www.gnu.org/licenses/>

MacMote
Copyright (C) 2010  Marcel Caraciolo & Dimas Gabriel
This program comes with ABSOLUTELY NO WARRANTY; for details see 
about box.
This is free software, and you are welcome to redistribute it
under certain conditions; see about box for details.


A stopwatch, used to control timer for presentation.


I AM NOT THE WRITTER OF THIS CODE! THIS CODE WAS TAKEN FROM:
	http://snippets.dzone.com/posts/show/776


"""
import time
import appuifw
import graphics
import e32

class StopWatch(object):
	running = False
	time_start = None
	elap = 0.0
	acanvas = None
	x = 0
	y = 20
	blank_width = 85
	sleep_time = 0.2
	hsec_prec = True
	magic_delta = 25
		
	def update(self,canvas=None):
		''' Updates the clock in canvas
		'''
		if canvas != None:
			self.acanvas = canvas
		if self.running:
			self.elap = time.clock() - self.time_start
			e32.ao_sleep(self.sleep_time,self.update)
		t = self.elap
		min = int(t/60)
		hour = int(t/(60*60))
		sec =  int(t - min*60)
		hsec = int((t - min*60 - sec)*100)	
		if self.acanvas != None:
			if self.hsec_prec:
				self.acanvas.rectangle((self.x, 0,
										(self.x + self.blank_width),
										(self.y + 1)), fill = (0,0,0))
				self.acanvas.text((self.x, self.y),
									u"%02d:%02d:%02d:%02d" % (hour,min,sec,hsec),
									font='title',
									fill = 0x0000FF)
			else:
				self.acanvas.rectangle((self.x + self.magic_delta, 0,
 										(self.x + self.blank_width),
										(self.y + 1)), fill = (0,0,0))
				self.acanvas.text((self.x + self.magic_delta, self.y),
 									u"%02d:%02d:%02d" % (hour,min,sec),
									font='title',
									fill = 0x0000FF)

	
	def set_msec(self,flag):
		''' Turn off milliseconds precision '''
		
		if flag:
			self.sleep_time = 0.25
			self.hsec_prec = True
			self.blank_width = 85
		else:
			self.sleep_time = 1.0
			self.hsec_prec = False
			self.blank_width = 54
		if self.running:
			if self.acanvas != None:
				self.acanvas.clear()

 	def toggle(self):
		''' Set/unset timer '''
		if self.running:
			self.running = False
			self.elap = time.clock() - self.time_start
		else:
			self.running = True
			self.time_start = time.clock() - self.elap
 			self.update()
	
	def reset_counter(self):
		''' Reset only the counter '''
		self.elap = 0.0
		self.time_start = time.clock()	
		
	def reset(self):
		''' Resets all internal class data '''
		self.running = 0
		self.elap = 0.0
		self.time_start = None
		self.acanvas = None
		self.x = 0
		self.y = 20
    
	def set_blank_width(self, length):
		''' Sets length of blanking rectangle'''
		if length > 70:
			self.blank_width = length
 

	def set_position(self, x, y):
		''' Sets position where stopwatch is drawn'''
		if (x > -1) and (y > 19):
			self.x = x
			self.y = y
	def create_submenu_lst(self):
		'''Returns a menu subitem to control stopwatch '''
		
		sub_menu_lst = (u'Stopwatch',
						((u'Reset', self.reset_counter),
						(u'Toggle', self.toggle)))
		return sub_menu_lst


#def test(param):
#	global tc, clock
#	clock.update(tc)



#clock = StopWatch()
#clock.toggle()
#tc = appuifw.Canvas(test)
#tc.clear((255,255,255))
#appuifw.app.body = tc
#appuifw.app.screen = 'large'
#lock = e32.Ao_lock()

#def _exit():
#	lock.signal()


#appuifw.app.menu = [ clock.create_submenu_lst(),
#                      (u'Exit', _exit)]

#clock.set_position(250,20)
#lock.wait()