import os, json, logging
from sys import argv, exit
from time import sleep

from core.api import MPServerAPI
from core.vars import DEFAULT_TELEPHONE_GPIO, UNPLAYABLE_FILES

STAR_KEY = 12
POUND_KEY = 14

PROMPTS = {
	'hear_hotline_start' : "hotline_start.wav",
	'hear_main_menu_start' : "main_menu_start.wav",
	'choose_from_main_menu' : "choose_from_main_menu.wav",
	'choose_things_in_general' : "choose_things_in_general.wav",
	'hear_hold_music' : "hold_music.wav",
	'hear_we_are_sorry' : "we_are_sorry.wav",
	'hear_cause_pain' : "bodies_cause_pain.wav",
	'hear_body_is_sphinx' : "recombination_is_naturally_occurring.wav",
	'choose_body_is_sphinx' : "we_have_yet_to_arrive_at_singularity.wav"
}

KEY_MAP = {
	'choose_from_main_menu' : xrange(3,7) +  [STAR_KEY],
	'choose_things_in_general' : xrange(3,6) +  [STAR_KEY],
	'choose_about_bodies' : xrange(3,7) + [STAR_KEY],
	'choose_body_is_sphinx' : [POUND_KEY]
}

class EnoughIsEnough(MPServerAPI):
	def __init__(self):
		MPServerAPI.__init__(self)

		self.gpio_mappings = DEFAULT_TELEPHONE_GPIO
		logging.basicConfig(filename=self.conf['d_files']['module']['log'], level=logging.DEBUG)

	def hear_hotline_start(self):
		c = 'hear_hotline_start'
		logging.info(c)

		"""
		Hello, complaints line, please hold. (muffled, gossipy) 
		But you know what happened when I was with Ray and his girl the other day?
		etc...
		"""

		if self.say(os.path.join("prompts", PROMPTS[c])):
			return self.hear_main_menu_start()

		return False

	def hear_main_menu_start(self):
		c = 'hear_main_menu_start'
		logging.info(c)

		"""
		Hello, and thank you for calling. Please be aware that your call may be
		monitored for quality assurance.
		"""
		if self.say(os.path.join("prompts", PROMPTS[c])):
			return self.choose_from_main_menu()

		return False

	def choose_from_main_menu(self):
		c = 'choose_from_main_menu'
		logging.info(c)

		"""
		Please select from the following options: 
		For complaints about the way things are in general, press 1. 
		For a complaint about yourself, press 2. 
		For complaints about your computer, press 3. 
		To submit a complaint about our complaint hotline operators, press 4. 
		For complaints about another person, press 5. 
		To hear these options again, press the Star key.
		"""
		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])

		if choice == KEY_MAP[c][0]:
			return self.choose_things_in_general()
		elif choice == KEY_MAP[c][1]:
			return self.about_yourself()
		elif choice == KEY_MAP[c][2]:
			return self.about_your_computer()
		elif choice == KEY_MAP[c][3]:
			return self.about_hotline_operators()
		elif choice == KEY_MAP[c][4]:
			return self.about_another_person()
		elif choice == KEY_MAP[c][5]:
			return self.choose_from_main_menu()

		return False

	def choose_things_in_general(self):
		c = 'choose_things_in_general'
		logging.info(c)

		"""
		For complaints about bodies, press 1. 
		For society, culture, and politics, press 2. 
		To complain about the environment, press 3. 
		To complain about the demiurge, press 4. 
		For complaints related to physics, press 5. 
		Press Star to hear these options again.
		"""
		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])

		if choice == KEY_MAP[c][0]:
			return self.choose_about_bodies()
		elif choice == KEY_MAP[c][1]:
			return self.about_society_culture_politics()
		elif choice == KEY_MAP[c][2]:
			return self.about_environment()
		elif choice == KEY_MAP[c][3]:
			return self.about_demiurge()
		elif choice == KEY_MAP[c][4]:
			return self.choose_physics()
		elif choice == KEY_MAP[c][5]:
			return self.choose_things_in_general()

		return False

	def choose_about_bodies(self):
		c = 'choose_about_bodies'
		logging.info(c)

		"""
		If your complaint is that there are too many bodies, press 1. 
		If there are too few, press 2. 
		If they are disgusting, press 3. 
		Press 4 if you are calling to complain because they cause pain. 
		Press 5 if they are useless. 
		Press 6 if it is because every body is a sphinx. 
		To hear these options again, press Star.
		"""
		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])

		if choice == KEY_MAP[c][0] || choice == KEY_MAP[c][1]:
			return self.hear_we_are_sorry()
		elif choice == KEY_MAP[c][2]:
			return self.hear_cause_pain()
		elif choice == KEY_MAP[c][3]:
			return self.hear_useless_bodies()
		elif choice == KEY_MAP[c][4]:
			return self.hear_body_is_sphinx()
		elif choice == KEY_MAP[c][5]:
			return self.choose_about_bodies()
		
		return False

	def hear_we_are_sorry(self):
		c = 'hear_we_are_sorry'
		logging.info(c)

		"""
		We are sorry, there is nothing we can do about this problem at the moment. 
		Our best technicians are working to find a solution. 
		Your complaint has been logged and will be addressed to the appropriate department. 
		Thank you for calling, and have a great day!
		"""

		# terminus
		return self.say(os.path.join("prompts", PROMPTS[c])) and self.hear_hold_music()

	def hear_cause_pain(self):
		c = 'hear_cause_pain'
		logging.info(c)

		"""
		Please hold while we transfer your call to: Physics.
		"""
		if self.say(os.path.join("prompts", PROMPTS[c])) and self.hear_hold_music():
			return self.choose_physics()

		return False

	def hear_useless_bodies(self):
		c = 'hear_useless_bodies'
		logging.info(c)

		"""
		Please hold while we transfer your call to: Complaints.
		"""
		if self.say(os.path.join("prompts", PROMPTS[c])) and self.hear_hold_music():
			return self.choose_from_main_menu()

		return False

	def hear_body_is_sphinx(self):
		c = 'hear_body_is_sphinx'
		logging.info(c)

		"""
		Recombination is naturally occurring. It is a fact of biological life. 
		Please hold the line for the singularity.
		"""
		if self.say(os.path.join("prompts", PROMPTS[c])) and self.hear_hold_music():
			return self.choose_body_is_sphinx()

		return False

	def choose_body_is_sphinx(self):
		c = 'choose_body_is_sphinx'
		logging.info(c)

		""" 
		We're sorry, we have yet to arrive at the singularity, 
		please continue to hold the line or 
		else press the Pound key to return to the main menu.
		"""
		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.choose_from_main_menu()

		if self.hear_hold_music():
			return self.choose_body_is_sphinx()

		return False

	def hear_hold_music(self):
		c = 'hear_hold_music':
		logging.info(c)

		return self.say(os.path.join("prompts", PROMPTS[c]))

	def run_script(self):
		super(EnoughIsEnough, self).run_script()
		self.hear_hotline_start()

if __name__ == "__main__":
	res = False
	eie = EnoughIsEnough()

	if argv[1] in ['--stop', '--restart']:
		res = eie.stop()
		sleep(5)

	if argv[1] in ['--start', '--restart']:
		res = eie.start()

	exit(0 if res else -1)