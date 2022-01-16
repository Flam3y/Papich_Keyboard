import keyboard as kb
import soundfile as sf
import soundcard as sc
import wx
import wx.adv
import os
import subprocess
import ctypes

TRAY_TOOLTIP = 'Papich keyboard'
TRAY_ICON = 'icon.png'

def create_menu_item(menu, label, func):
	item = wx.MenuItem(menu, -1, label)
	menu.Bind(wx.EVT_MENU, func, id=item.GetId())
	menu.Append(item)
	return item


class TaskBarIcon(wx.adv.TaskBarIcon):
	def __init__(self, frame):
		wx.adv.TaskBarIcon.__init__(self)
		self.myapp_frame = frame
		self.set_icon(TRAY_ICON)
		self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

	def CreatePopupMenu(self):
		menu = wx.Menu()
		create_menu_item(menu, 'Papich keyboard', self.on_presed)
		menu.AppendSeparator()
		create_menu_item(menu, 'Start', self.on_start)
		create_menu_item(menu, 'Stop', self.on_stop)
		menu.AppendSeparator()
		create_menu_item(menu, 'Exit', self.on_exit)
		return menu

	def set_icon(self, path):
		icon = wx.Icon(wx.Bitmap(path))
		self.SetIcon(icon, TRAY_TOOLTIP)

	def on_left_down(self, event):
		print('Tray icon was left-clicked.')

	def on_presed(self, event):
		default_speaker = sc.default_speaker()
		samples, samplerate = sf.read('Sounds\KillAll.wav')
		default_speaker.play(samples, samplerate=samplerate)

	def on_exit(self, event):
		self.myapp_frame.Close()

	def on_start(self, event):
		global task
		u = ctypes.windll.LoadLibrary("user32.dll")
		pf = getattr(u, "GetKeyboardLayout")
		print(hex(pf(0)))
		if hex(pf(0)) == "0x4090409":
			task = subprocess.Popen([r"aditional_en.exe"])
		if hex(pf(0)) == "0x4190419":
			task = subprocess.Popen([r"aditional_ru.exe"])
	def on_stop(self, event):
		os.system("taskkill /im aditional_en.exe /f")
		os.system("taskkill /im aditional_ru.exe /f")

class My_Application(wx.Frame):

# ----------------------------------------------------------------------
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "", size=(1, 1))
		panel = wx.Panel(self)
		self.myapp = TaskBarIcon(self)
		self.Bind(wx.EVT_CLOSE, self.onClose)

	# ----------------------------------------------------------------------
	def onClose(self, evt):
		"""
		  Destroy the taskbar icon and the frame
		  """
		os.system("taskkill /im aditional_en.exe /f")
		os.system("taskkill /im aditional_ru.exe /f")
		self.myapp.RemoveIcon()
		self.myapp.Destroy()
		self.Destroy()


if __name__ == "__main__":
	MyApp = wx.App()
	My_Application()
	MyApp.MainLoop()