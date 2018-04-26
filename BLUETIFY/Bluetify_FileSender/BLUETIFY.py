from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
import bluetooth
import lightblue
import sys
from PyOBEX.client import Client
from kivy.uix.listview import ListView, ListItemButton

from kivy.adapters.dictadapter import ListAdapter


global fileName
nearby_devices = ()
nd = ()
lst = []
obex_port = None
target_address = None
s1 = ""

class RootWidget(BoxLayout):
	
	student_list = ObjectProperty()
	global s1	
	
	def submit_students(self):
		pass
	def delete_students(self):
		pass
	def replace_students(self):
		pass
	

	def fileSelected(self, path, filename):
		self.ids.label.text = str(filename)
	
	def getFile(self):
		global fileName
		print self.ids.label.text
		fileName = str((self.ids.label.text).encode('utf-8'))
		
	def getList(self):
	
		global lst
		print("searching devices")
		nearby_devices = bluetooth.discover_devices()
		for bdaddr in nearby_devices:
			lst.append(bluetooth.lookup_name(bdaddr))
		return lst
	def refreshList(self):
		global lst
		global nearby_devices
		print("searching devices")
		nearby_devices = bluetooth.discover_devices()
		for bdaddr in nearby_devices:
			lst.append(bluetooth.lookup_name(bdaddr))
		self.student_list.adapter._trigger_reset_populate()
		
	def getDevice(self):
		global s1
		if self.student_list.adapter.selection:
			print self.student_list.adapter.selection[0].text
			s1 = self.student_list.adapter.selection[0].text
		else:
			print "select a device first"	
			
	def getDeviceName(self):
		global s1
		if self.student_list.adapter.selection:
			s1 = str(self.student_list.adapter.selection[0].text)
			print s1
	def sendFile(self):
		print "sendFileCalled"
		global lst
		global s1
		global fileName
		global nearby_devices
		target_address = ""
		print "sending"
		print s1
		nearby_devices = bluetooth.discover_devices()
		print nearby_devices
		for bdaddr in nearby_devices:
			print bdaddr
			print bluetooth.lookup_name(bdaddr)
			print type(bluetooth.lookup_name(bdaddr))
			if(s1 == bluetooth.lookup_name(bdaddr)):
				print("found the target device !!")
				target_address = bdaddr
				print(target_address)
				
				print("searching for the object push service")
				services = lightblue.findservices(target_address)
				for service in services:
					if(service[2] == "OBEX Object Push"):
						obex_port = service[1]
						print("ok service '", service[2], "' is in port",service[1], "!")
						break
				print("sending a file")
				print fileName
				fileName = fileName.encode('utf-8')
				print type(fileName)
				l = len(fileName)
				fileName = fileName[3:l-2]
				print fileName
				lightblue.obex.sendfile(target_address, service[1], fileName)
				print("completed!\n")
				print("an error occurred while sending file\n")
					
						
						
						
						
				
		
		
		
		
		
	pass

class StudentListButton(ListItemButton):
	pass

class ServerApp(App):
    '''This is the main class of your app.
       Define any app wide entities here.
       This class can be accessed anywhere inside the kivy app as,
       in python::
         app = App.get_running_app()
         print (app.title)
       in kv language::
         on_release: print(app.title)
       Name of the .kv file that is auto-loaded is derived from the name
       of this class::
         MainApp = main.kv
         MainClass = mainclass.kv
       The App part is auto removed and the whole name is lowercased.
    '''

    def build(self):
        return RootWidget()



if '__main__' == __name__:

	ServerApp().run()
