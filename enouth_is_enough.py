import os, json, logging
from sys import argv, exit
from time import sleep

from core.api import MPServerAPI
from core.vars import DEFAULT_TELEPHONE_GPIO, UNPLAYABLE_FILES

STAR_KEY = 12
POUND_KEY = 14

AWKWARD_PAUSE = 5

PROMPTS = {
	'hear_hotline_start' : "hotline_start.wav",
	'hear_main_menu_start' : "main_menu_start.wav",
	'choose_from_main_menu' : "choose_from_main_menu.wav",
	'choose_things_in_general' : "choose_things_in_general.wav",
	'hear_hold_music' : "hold_music.wav",
	'hear_we_are_sorry' : "we_are_sorry.wav",
	'hear_cause_pain' : "bodies_cause_pain.wav",
	'hear_body_is_sphinx' : "recombination_is_naturally_occurring.wav",
	'choose_body_is_sphinx' : "we_have_yet_to_arrive_at_singularity.wav",
	'choose_society_culture_politics' : "choose_society_culture_politics.wav",
	'hear_people_are_morons' : "hear_people_are_morons.wav",
	'hear_people_are_evil' : "hear_people_are_evil.wav",
	'choose_birth_certificate' : "choose_birth_certificate.wav",
	'hear_born_under_bad_sign' : "hear_born_under_bad_sign.wav",
	'hear_cant_remember_birthday' : "hear_cant_remember_birthday.wav",
	'choose_born_full_moon' : "choose_born_full_moon.wav",
	'choose_astro_aspect' : "choose_astro_aspect.wav",
	'choose_physics' : "choose_physics.wav",
	'hear_retroactive_precognition' : "hear_retroactive_precognition.wav",
	'hear_quantum_suicide' : "hear_quantum_suicide.wav",
	'choose_drivers_license' : "choose_drivers_license.wav",
	'hear_under_the_influence' : "hear_under_the_influence.wav",
	'hear_discrimination' : "hear_discrimination.wav",
	'hear_road_rage' : "hear_road_rage.wav",
	'hear_about_toilet' : ["hear_about_toilet_1.wav", "hear_about_toilet_2.wav"],
	'choose_toilet' : "choose_toilet.wav",
	'hear_favorite_tv_show' : "hear_favorite_tv_show.wav",
	'hear_legalize_crime' : "hear_legalize_crime.wav",
	'hear_overthrow' : "hear_overthrow.wav",
	'hear_about_yourself' : "hear_about_yourself.wav",
	'choose_about_yourself' : "choose_about_yourself.wav",
	'hear_ultima_thule_no_credit' : "hear_ultima_thule_no_credit.wav",
	'choose_about_computers' : "choose_about_computers.wav",
	'hear_about_hotline_operators' : "hear_about_hotline_operators.wav",
	'choose_about_others' : "choose_about_others.wav",
	'gather_animal_passcode' : "gather_animal_passcode.wav",
	'hear_animal_passcode' : "hear_animal_passcode.wav",
	'hear_mermaids' : "hear_mermaids.wav",
	'hear_wait_for_authorities' : "hear_wait_for_authorities.wav",
	'hear_animal_resembles_fly' : "hear_animal_resembles_fly.wav",
	'hear_animal_eaten' : "hear_animal_eaten.wav",
	'hear_stray_dog' : "hear_stray_dog.wav",
	'choose_stray_dog' : "choose_stray_dog.wav",
	'hear_nightlife' : "hear_nightlife.wav",
	'hear_faithfulness' : "hear_faithfulness.wav",
	'choose_fabulous_animal' : "choose_fabulous_animal.wav",
	'choose_gorgon' : "choose_gorgon.wav",
	'choose_turn_to_stone' : "choose_turn_to_stone.wav",
	'hear_about_family' : "hear_about_family.wav",
	'choose_about_mate' : "choose_about_mate.wav",
	'hear_doesnt_listen' : "hear_doesnt_listen.wav",
	'choose_about_becky' : "choose_about_becky.wav",
	'choose_about_imaginary_friend' : "choose_about_imaginary_friend.wav",
	'choose_about_acquaintance_loop' : "choose_about_acquaintance_loop.wav"
}

KEY_MAP = {
	'choose_from_main_menu' : xrange(3,7) +  [STAR_KEY],
	'choose_things_in_general' : xrange(3,7) +  [STAR_KEY],
	'choose_about_bodies' : xrange(3,7) + [STAR_KEY],
	'choose_body_is_sphinx' : [POUND_KEY],
	'choose_society_culture_politics' : xrange(3,7) + [STAR_KEY],
	'choose_birth_certificate' : xrange(3,5),
	'choose_born_full_moon' : xrange(3,6),
	'choose_astro_aspect' : xrange(3,9),
	'choose_physics' : xrange(3,6),
	'choose_drivers_license' : xrange(3,5),
	'choose_toilet' : xrange(3,5),
	'choose_about_yourself' : xrange(3,6),
	'choose_about_computers' : [3,4],
	'choose_about_others' : xrange(3,8) + [STAR_KEY],
	'choose_fabulous_animal' : xrange(3,7),
	'choose_gorgon' : [3,4],
	'choose_turn_to_stone' : [3,4],
	'choose_about_mate' : xrange(3,6),
	'choose_about_friend_loop' : [11, STAR_KEY],
	'choose_about_family' : xrange(3,7) + [STAR_KEY],
	'choose_exorcisms' : [3,4],
	'choose_about_acquaintance_loop' : [11, STAR_KEY]
	'choose_about_stranger_loop' : [11, STAR_KEY]
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
			if self.redirect_to('hear_about_yourself'):
				return self.choose_about_yourself()
		elif choice == KEY_MAP[c][2]:
			return self.choose_about_computers()
		elif choice == KEY_MAP[c][3]:
			return self.go_to_terminus('hear_about_hotline_operators')
		elif choice == KEY_MAP[c][4]:
			return self.choose_about_others()
		elif choice == KEY_MAP[c][5]:
			return self.choose_from_main_menu()

		return False

	def choose_about_computers(self):
		c = 'choose_about_computers'
		logging.info(c)

		"""
		I’m sorry, a computer must obey orders given to it by human beings. 
		Please press 1 to redirect your call to Complaint about another person. 
		Press 2 to redirect your call to Complaint about yourself.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.choose_about_others()
		elif choice == KEY_MAP[c][1]:
			if self.redirect_to('hear_about_yourself'):
				return self.choose_about_yourself()

		return False

	def choose_about_yourself(self):
		c = 'choose_about_yourself'
		logging.info(c)

		"""
		Welcome to Ultima Thule Tele-therapy! Face your demons andemerge victorious! 
		Our life-changing service is for entertainment purposes only. 
		Ultima Thule is not to be held responsible for failure to treat unresolved problems, 
		mistaken revelations, exacerbation of unresolved problems, 
		or any other internal or external inconveniences. 
		Please choose how far back in time you would like to travel to confront your demon. 
		(use Ultima Thule hotline intro) 
		Press 1 for childhood. 
		Press 2 for adolescence. 
		Press 3 for adulthood. 
		Press 4 for now.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice in KEY_MAP[c]:
			return self.go_to_terminus('hear_ultima_thule_no_credit')

		return False

	def choose_about_others(self):
		c = 'choose_about_others'
		logging.info(c)

		"""
		Would you like to place a complaint about an animal? Press 1. 
		Press 2 for complaints about your mate. 
		Press 3 for complaints about a friend. 
		Press 4 for complaints about a family member. 
		To place a complaint about an acquaintance, press 5. 
		To complain about a stranger, press 6. 
		To hear these options again, press Star.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.choose_about_animals()
		elif choice == KEY_MAP[c][1]:
			return self.choose_about_mate()
		elif choice == KEY_MAP[c][2]:
			return self.choose_about_friend()
		elif choice == KEY_MAP[c][3]:
			return self.choose_about_family()
		elif choice == KEY_MAP[c][4]:
			return self.choose_about_acquaintance()
		elif choice == KEY_MAP[5]:
			return self.choose_about_stranger()
		elif choice == KEY_MAP[6]:
			return self.choose_about_others()

		return False

	def choose_about_family(self):
		c = 'choose_about_family'
		logging.info(c)

		"""
		If you are calling to complain about a baby, press 1. 
		For the aristocracy, press 2. 
		For sibling-related complaints, press 3. 
		Press 4 for a paranormal step-mother or 5 for another parent. 
		To hear these options again, press Star.
		"""
		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			if self.redirect_to('hear_about_bodies'):
				return self.choose_about_bodies()
		elif choice == KEY_MAP[c][1]:
			return self.go_to_terminus('hear_about_aristocracy')
		elif choice == KEY_MAP[c][2]:
			if self.redirect_to('hear_about_animals'):
				return self.choose_about_animals()
		elif choice == KEY_MAP[c][3]:
			if self.redirect_to('hear_about_exorcisms'):
				return self.choose_exorcisms()
		elic choice == KEY_MAP[c][4]:
			if self.redirect_to('hear_about_acquaintance'):
				return self.choose_about_acquaintance()

		return False

	def choose_exorcisms(self):
		c = 'choose_exorcisms'
		logging.info(c)

		"""
		...
		If none of these entry points apply to you, press 1. 
		If any of these entry points do apply to you, press 2.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.go_to_terminus('hear_none_apply_exorcism')
		elif choice == KEY_MAP[c][1]:
			return self.go_to_terminus('hear_any_apply_exorcism')

		return False

	def choose_about_acquaintance(self):
		c = 'choose_about_acquaintance'
		logging.info(c)

		"""
		For complaints regarding the waiter at your usual lunch spot, press 1. 
		To complain about your neighbor, press 2. 
		Press 3 for complaints about Dave. 
		Press 4 for complaints about Sally. 
		If you would like to place a complaint about someone I don’t know, press 5.
		"""
		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			if self.redirect_to('hear_redirect_to_health_department'):
				return self.go_to_terminus('hear_health_department')
		elif choice == KEY_MAP[c][1]:
			return self.choose_about_neighbor()
		elif choice == KEY_MAP[c][2]:
			return self.choose_about_acquaintance_loop('choose_about_dave')
		elif choice == KEY_MAP[c][3]:
			return self.choose_about_acquaintance_loop('choose_about_sally')
		elif choice == KEY_MAP[c][4]:
			return self.choose_about_acquaintance_loop('choose_about_someone_i_dont_know')

		return False

	def choose_about_acquaintance_loop(self, with_prompt):
		c = 'choose_about_acquaintance_loop'
		logging.info(c)

		"""
		If you have another complaint about an acquaintance, please press 0, 
		otherwise press Star to return to the main menu.
		"""

		if not self.say(os.path.join("prompts", PROMPTS[with_prompt])):
			return False

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.choose_about_acquaintance()
		elif choice == KEY_MAP[c][1]:
			return self.choose_from_main_menu()

		return False

	def choose_about_stranger(self):
		c = 'choose_about_stranger'
		logging.info(c)

		"""
		Press 1 if the stranger is popular-looking. 
		Press 2 if he or she is happy. 
		If the stranger is tall, press 3. 
		If he or she is bovine and or porcine, press 4.
		For complaints about homeless strangers, press 5. 
		For loud strangers, press 6. 
		Press 7 for drunken strangers. 
		If you want to complain about a creepy stranger, press 8. 
		To complain about a sartorially impaired stranger, press 9. 
		Press Star to hear these options again.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][-1]:
			return self.choose_about_stranger()

		p = None

		if choice in [KEY_MAP[c][0], KEY_MAP[c][8]]:
			p = 'choose_popular_looking_or_satorily_impared_stranger'
		elif choice == KEY_MAP[c][1]:
			p = 'choose_happy_looking_stranger'
		elif choice == KEY_MAP[c][2]:
			p = 'choose_tall_stranger'
		elif choice == KEY_MAP[c][3]:
			p = 'choose_bovine_stranger'
		elif choice == KEY_MAP[c][4]:
			p = 'choose_homeless_stranger'
		elif choice == KEY_MAP[c][5]:
			p = 'choose_loud_stranger'
		elif choice in [KEY_MAP[c][6],KEY_MAP[c][7]]:
			p = 'choose_drunk_or_creepy_stranger'

		if p is not None:
			return self.choose_about_stranger_loop(p)

		return False

	def choose_about_stranger_loop(self, with_prompt):
		c = 'choose_about_stranger_loop'
		logging.info(c)

		_ = self.prompt(os.path.join("prompt", PROMPTS['choose_leave_complaint']), KEY_MAP['choose_leave_complaint'])
		if not self.say(os.path.join("prompts", PROMPTS[with_prompt])):
			return False

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.choose_about_stranger_loop()
		elif choice == KEY_MAP[c][1]:
			return self.choose_from_main_menu()

		return False

	def choose_about_mate(self):
		c = 'choose_about_mate'
		logging.info(c)

		"""
		If your mate accidentally called you “mom” or “dad”, press 1. 
		If he or she doesn’t listen, press 2. 
		Press 3 if your mate is an illegal alien. 
		Press 4 if he or she uses mind control.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			if self.say(os.path.join("prompts", "silence.wav")):
				sleep(AWKWARD_PAUSE)
				return self.choose_from_main_menu()
		elif choice == KEY_MAP[c][1]:
			if self.say(os.path.join("prompts", PROMPTS['hear_doesnt_listen'])):
				return self.choose_from_main_menu()
		elif choice == KEY_MAP[c][2]:
			return self.go_to_terminus('hear_wait_for_authorities')
		elif choice == KEY_MAP[c][3]:
			if self.redirect_to('hear_about_yourself'):
				return self.choose_about_yourself()

		return False

	def choose_about_friend(self):
		c = 'choose_about_friend'
		logging.info(c)

		"""
		If your call concerns cocaine, press 1 now. 
		If you’re calling about Becky, press 2. 
		For calls about your dog, press 3. 
		Press 4 if your call is about an imaginary friend or fictional character.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.go_to_terminus('hear_wait_for_authorities')
		elif choice == KEY_MAP[c][1]:
			return self.choose_about_friend_loop('choose_about_becky')
		elif choice == KEY_MAP[c][2]:
			if self.redirect_to('hear_about_animals'):
				return self.choose_about_animals()
		elif choice == KEY_MAP[c][3]:
			return self.choose_about_friend_loop('choose_about_imaginary_friend')

		return False

	def choose_about_friend_loop(self, with_prompt):
		c = 'choose_about_friend_loop'
		logging.info(c)

		"""
		You deserve better than Becky… 

		or

		Terrible! Just terrible! You deserve better…

		If you have complaint about another friend, please press 0, 
		otherwise press Star to return to the main menu.
		"""

		if not self.say(os.path.join("prompts", PROMPTS[with_prompt])):
			return False

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.choose_about_friend()
		elif choice == KEY_MAP[c][1]:
			return self.choose_from_main_menu()

		return False

	def choose_about_animals(self):
		c = 'choose_about_animals'
		logging.info(c)

		"""
		For complaints about an animal that has just broken the flower vase, press 1. 
		For stray dogs, press 2. 
		For mermaids or sirens, press 3. 
		Press 4 for complaints about a trained animal. 
		Press 5 for an animal belonging to the emperor. 
		Press 6 for a fabulous animal. 
		To place a complaint about an animal that, from a distance, resembles a fly, press 7. 
		For an animal you have eaten, press 8. 
		Please be advised: if you are calling about a vindictive cat, 
		a disobedient bird, or a malodorous fish, 
		we are no longer licensed to assist you. 
		If you would like to hear these options again, press Star.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			_ = self.gather(os.path.join("prompts", PROMPTS['gather_animal_passcode']))
			return self.go_to_terminus('hear_animal_passcode')
		elif choice == KEY_MAP[c][1]:
			return self.choose_stray_dog()
		elif choice == KEY_MAP[c][2]:
			return self.go_to_terminus('hear_mermaids')
		elif choice == KEY_MAP[c][3]:
			# MISSING FROM SCRIPT?
			return self.go_to_terminus('we_are_sorry')
		elif choice == KEY_MAP[c][4]:
			return self.go_to_terminus('hear_wait_for_authorities')
		elif choice == KEY_MAP[c][5]:
			return self.choose_fabulous_animal()
		elif choice == KEY_MAP[c][6]:
			if self.redirect_to('hear_animal_resembles_fly'):
				return self.choose_physics()
		elif choice == KEY_MAP[c][7]:
			if self.redirect_to('hear_animal_eaten') and self.redirect_to('hear_about_yourself'):
				return self.choose_about_yourself()
		elif choice == KEY_MAP[c][8]:
			return self.choose_about_animals()

		return False

	def choose_fabulous_animal(self):
		c = 'choose_fabulous_animal'
		logging.info(c)

		"""
		Press 1 for supermodels. 
		Press 2 for the dodo bird. 
		Press 3 for mangrove. 
		Press 4 for the coelacanth. 
		Press 5 for gorgons.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			# missing from script?
			return self.go_to_terminus('we_are_sorry')
		elif choice == KEY_MAP[c][1]:
			if self.redirect_to('hear_complaints_in_general'):
				return self.choose_from_main_menu()
		elif choice in [KEY_MAP[c][2], KEY_MAP[c][3]]:
			if self.redirect_to('hear_about_family'):
				return self.choose_about_family()
		elif choice == KEY_MAP[c][4]:
			return self.choose_gorgon()

		return False

	def choose_gorgon(self):
		c = 'choose_gorgon'
		logging.info(c)

		"""
		If you have been turned to stone, press 1. 
		If you have turned the gorgon to stone, press 2.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.go_to_terminus('hear_turned_to_stone')
		elif choice == KEY_MAP[c][1]:
			return self.choose_turn_to_stone()

		return False

	def choose_turn_to_stone(self):
		c = 'choose_turn_to_stone'
		logging.info(c)

		"""
		If you would like to add insult to injury, press 1. 
		If you would like to let it be, press 2.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.go_to_terminus('hear_insult_to_injury')
		elif choice == KEY_MAP[c][1]:
			return self.hear_hold_music()

		return False

	def choose_stray_dog(self):
		c = 'choose_stray_dog'
		logging.info(c)

		"""
		Thank you for contacting Animal Control. 
		If you know your party's extension, please dial it now, otherwise please hold the line. 
		(wait music) 
		For nightlife, press 1. 
		For faithfulness, press 2. 
		For protection, press 3. 
		Press 4 for euthanasia and mourning.
		"""
		if not self.say(os.path.join("prompts", PROMPTS['hear_stray_dog'])) and self.hear_hold_music():
			return False

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.hear_hold_music() and self.go_to_terminus('hear_nightlife')
		elif choice == KEY_MAP[c][1]:
			if self.redirect_to('hear_faithfulness'):
				return self.choose_about_friend()
		elif choice in [KEY_MAP[c][2], KEY_MAP[c][3]]:
			if self.redirect_to('hear_about_yourself'):
				return self.choose_about_yourself()

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
			return self.choose_society_culture_politics()
		elif choice == KEY_MAP[c][2]:
			return self.hear_about_environment()
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
			return self.go_to_terminus(PROMPTS['hear_we_are_sorry'])
		elif choice == KEY_MAP[c][2]:
			return self.hear_cause_pain()
		elif choice == KEY_MAP[c][3]:
			return self.hear_useless_bodies()
		elif choice == KEY_MAP[c][4]:
			return self.hear_body_is_sphinx()
		elif choice == KEY_MAP[c][5]:
			return self.choose_about_bodies()
		
		return False

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

	def choose_society_culture_politics(self):
		c = 'choose_society_culture_politics'
		logging.info(c)

		"""
		Tapez un si vous appellez car on est dans le creux de la vague. 
		Press 2 if you would like to complain that people are animals. 
		Press 3 for a birth certificate. 
		Press 4 if you would like to complain that people are morons. 
		Press 5 for people are evil. 
		To hear these options again, press Star.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.hear_creux_de_la_vague()
		elif choice == KEY_MAP[c][1]:
			return self.hear_people_are_animals()
		elif choice == KEY_MAP[c][2]:
			return self.choose_birth_certificate()
		elif choice == KEY_MAP[c][3]:
			return self.go_to_terminus(PROMPTS['hear_people_are_morons'])
		elif choice == KEY_MAP[c][4]:
			return self.go_to_terminus(PROMPTS['hear_people_are_evil'])
		elif choice == KEY_MAP[c][5]:
			return self.choose_society_culture_politics()

		return False

	def hear_creux_de_la_vague(self):
		c = 'hear_creux_de_la_vague'
		logging.info(c)

		"""
		Merci de patienter, nous dirigeons votre appel à: l'environment
		"""
		if self.say(os.path.join("prompts", PROMPTS[c])) and self.hear_hold_music():
			return self.hear_about_environment()

		return False

	def hear_people_are_animals(self):
		c = 'hear_people_are_animals'
		logging.info(c)

		"""
		Please hold while we transfer your call to: Complaints about animals.
		"""

		if self.say(os.path.join("prompts", PROMPTS[c])) and self.hear_hold_music():
			return self.hear_about_animals()

		return False

	def choose_birth_certificate(self):
		c = 'choose_birth_certificate'
		logging.info(c)

		"""
		Press 1 if you were born under a bad sign. 
		Press 2 if you were born during a full moon. 
		If you can’t remember your birthday, press 3.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.go_to_terminus(PROMPTS['hear_born_under_bad_sign'])
		elif choice == KEY_MAP[c][1]:
			return self.choose_born_full_moon()
		elif choice == KEY_MAP[c][2]:
			return self.go_to_terminus(PROMPTS['hear_cant_remember_birthday'])

		return False

	def choose_born_full_moon(self):
		c = 'choose_born_full_moon'
		logging.info(c)

		"""
		Were you born under an air sign? Press 1. 
		For earth signs, press 2. 
		Water signs, press 3. 
		Fire signs, press 4.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice in KEY_MAP[c]:
			return self.choose_astro_aspect()

		return False

	def choose_astro_aspect(self):
		c = 'choose_astro_aspect'
		logging.info(c)

		"""
		Press 1 if your astrological aspect is contraparallel. 
		2 if it is trine. 
		3 for sextile. 
		4 for conjunction. 
		5 for opposition. 
		6 for square. 
		7 for parallel.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice in KEY_MAP[c]:
			return self.go_to_terminus(PROMPTS['hear_astro_aspect'])

		return False

	def hear_about_environment(self):
		c = 'hear_about_environment'
		logging.info(c)

		if self.say(os.path.join("prompts", PROMPTS[c])) and self.hear_hold_music():
			return self.hear_about_toilet()

		return False

	def hear_about_toilet(self):
		c = 'hear_about_toilet'
		logging.info(c)

		"""
		Please hold as we connect you to our plumbing department. 
		(wait music) All of our plumbers are currently on strike. 
		Please hold while we connect you to our strikebreaking thugs. (wait music)
		"""

		for p in PROMPTS[c]:
			if not self.say(os.path.join("prompts", p)) and self.hear_hold_music():
				return False

		return self.choose_toilet()

	def choose_toilet(self):
		c = 'choose_toilet'
		logging.info(c)

		"""
		Thank you for contacting Pinkerton Detective Agency. 
		All of our personnel are now lobbyists. 
		If you are calling to get your favorite TV show back on the air, press 1. 
		Press 2 if you are calling to support the legalization of a white collar crime. 
		If you are seeking to contribute to the overthrow of a non-OECD member country regime, 
		press 3.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.go_to_terminus('hear_favorite_tv_show')
		elif choice == KEY_MAP[c][1]:
			return self.go_to_terminus('hear_legalize_crime')
		elif choice == KEY_MAP[c][2]:
			return self.go_to_terminus('hear_overthrow')

		return False

	def choose_physics(self):
		c = 'choose_physics'
		logging.info(c)

		"""
		For complaints about retroactive precognition, press 1. 
		If your driving license has been revoked, press 2. 
		For quantum suicide and immortality-related complaints, press 3. 
		If you are calling about a clogged toilet or drain, press 4.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			return self.hear_retroactive_precognition()
		elif choice == KEY_MAP[c][1]:
			return self.choose_drivers_license()
		elif choice == KEY_MAP[c][2]:
			if self.say(os.path.join("prompts", PROMPTS['hear_quantum_suicide'])):
				return self.choose_physics()
		elif choice == KEY_MAP[c][3]:
			return self.hear_about_toilet()

		return False

	def hear_retroactive_precognition(self):
		c = 'hear_retroactive_precognition'
		logging.info(c)

		"""
		Hello and thank you for calling Howard the All-Knowing. 
		Don't tell me what ails you – I know it already! 
		My advice: nothing is wrong, it's all life, baby! (silence) 
		I'm going to transfer you to the plumbers now.
		"""

		self.hear_hold_music():
		if self.say(os.path.join("prompts", PROMPTS['hear_retroactive_precognition'])) and self.hear_hold_music():
			return self.hear_about_toilet()

		return False

	def choose_drivers_license(self):
		c = 'choose_drivers_license'
		logging.info(c)

		"""
		If you were driving under the influence, press 1. 
		Press 2 if you were discriminated against. 
		For road rage, press 3.
		"""

		choice = self.prompt(os.path.join("prompts", PROMPTS[c]), KEY_MAP[c])
		if choice == KEY_MAP[c][0]:
			if self.hear_hold_music():
				return self.go_to_terminus(PROMPTS['hear_under_the_influence'])
		elif choice == KEY_MAP[c][1]:
			if self.say(os.path.join("prompts", PROMPTS['hear_discrimination'])) and self.hear_hold_music():
				return self.choose_about_others()
		elif choice == KEY_MAP[c][2]:
			if self.say(os.path.join("prompts", PROMPTS['hear_road_rage'])) and self.hear_hold_music():
				return self.choose_from_main_menu()

		return False

	def hear_hold_music(self):
		c = 'hear_hold_music':
		logging.info(c)

		return self.say(os.path.join("prompts", PROMPTS[c]))

	def go_to_terminus(self, with_prompt):
		# terminus
		logging.info("terminus: %s" % with_prompt)
		return self.redirect_to(with_prompt)
	
	def redirect_to(self, with_prompt):
		return self.say(os.path.join("prompts", PROMPTS[with_prompt])) and self.hear_hold_music()

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