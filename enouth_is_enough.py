import os, json, logging
from sys import argv, exit
from time import sleep

from core.api import MPServerAPI
from core.vars import DEFAULT_TELEPHONE_GPIO, UNPLAYABLE_FILES

class EnoughIsEnough(MPServerAPI):
	def __init__(self):
		MPServerAPI.__init__(self)

		self.gpio_mappings = DEFAULT_TELEPHONE_GPIO
		logging.basicConfig(filename=self.conf['d_files']['module']['log'], level=logging.DEBUG)

	def run_script(self):
		super(EnoughIsEnough, self).run_script()

if __name__ == "__main__":
	res = False
	eie = EnoughIsEnough()

	if argv[1] in ['--stop', '--restart']:
		res = eie.stop()
		sleep(5)

	if argv[1] in ['--start', '--restart']:
		res = eie.start()

	exit(0 if res else -1)