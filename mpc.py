
#mpc class - controls mpc

#imports ______________________________________________
import os

class MPC():

	def __init__(self, volume=30):
		self.volume = volume
		self.volume_mute = self.volume
		self.playing = True

	def play(self):
		print ("----> play")
		os.system('mpc play')
		self.playing = True

	def stop(self):
		print ("----> stop")
		os.system('mpc stop')
		self.playing = False

	def pause(self):
		print ("----> pause")
		os.system('mpc pause')
		self.playing = False

	def volum_set(self, volum):
		#print('dins mpc__________', type(volum) )
		print (f"----> volume {volum} ")
		os.system(f'mpc volume {volum}')

	def prev(self):
		print ("----> prev")
		os.system('mpc prev')

	def next(self):
		print ("----> next")
		os.system('mpc next')

	def random(self):
		print ("----> random")
		os.system('mpc random')

	def current(self):
		print ("----> random")
		os.system('mpc current')





