import os, json, logging
from sys import argv, exit
from time import sleep

from core.api import MPServerAPI

# arbitrary at this point...
ONE = 3
MUTE = 13
DOLLAR = 14
POUND = 10
EURO = 11
FOUR = 6
TEN = 12
COMMAND = 9
CONTROL = 8
INFINITY = 7
COMMA = 6

TYPE_A = [ONE, MUTE, DOLLAR, POUND, FOUR, TEN]
TYPE_B = [ONE, MUTE, DOLLAR, POUND, FOUR, EURO, TEN]
TYPE_C = [ONE, MUTE, DOLLAR, POUND]
TYPE_D = [INFINITY, TEN]

KEY_MAP = {
	'2_MainMenu': {
		'tree' : [
			'3_ThingsInGeneralMenu', 
			{'32_ComplaintAboutYourselfEnd' : '33_UltimaThuleMainMenuOptionOne'},
			'35_ComlaintAboutComputerMenu',
			'36_ComplaintAboutHotlineOperatorsEnd',
			'37_ComplaintAboutAnotherPersonMenu',
			'2_MainMenu'
		],
		'map' : TYPE_A
	},
	'3_ThingsInGeneralMenu': {
		'tree' : [
			'4_BodiesMenu',
			'9_SocietyCulturePoliticsMenu',
			'20_EnvironmentEnd',
			'10_CreuxdeLaVagueEnd', #what
			'21_PhysicsMenu',
			'3_ThingsInGeneralMenu'
		],
		'map' : TYPE_A
	},
	'4_BodiesMenu': {
		'tree' : [
			'5_WeAreSorryEnd',
			'5_WeAreSorryEnd',
			'5_WeAreSorryEnd',
			{'6_CausePainEnd' : '21_PhysicsMenu'},
			{'7_UselessEnd' : '2_MainMenu'},
			'8_SphinxEnd',
			'4_BodiesMenu'
		],
		'map' : TYPE_B
	},
	'5_WeAreSorryEnd': None,
	'6_CausePainEnd' : '21_PhysicsMenu',
	'7_UselessEnd': '2_MainMenu',
	'8_SphinxEnd':{
		'tree' : ['8_SphinxEnd', '2_MainMenu'],
		'map' : [None, COMMAND]
	},
	'9_SocietyCulturePoliticsMenu':{
		'tree' : [
			'10_CreuxdeLaVagueEnd',
			'11_PeopleAreAnimalsEnd',
			'12_BirthCertificateMenu',
			'18_PeopleAreMoronsEnd',
			'19_PeopleAreEvilEnd',
			'9_SocietyCulturePoliticsMenu'
		],
		'map' : TYPE_A
	},
	'10_CreuxdeLaVagueEnd': '20_EnvironmentEnd',
	'11_PeopleAreAnimalsEnd': '38_AnimalComplaintMenu',
	'12_BirthCertificateMenu':{
		'tree' : [
			'13_BornUnderBadSignEnd',
			'14_BornFullMoonMenu',
			'17_CantRememberEnd'
		],
		'map' : [ONE, MUTE, DOLLAR]
	},
	'13_BornUnderBadSignEnd': None,
	'14_BornFullMoonMenu':{
		'tree' : [
			'15_AstrologicalAspectMenu',
			'15_AstrologicalAspectMenu',
			'15_AstrologicalAspectMenu',
			'15_AstrologicalAspectMenu'
		],
		'map' : [ONE, MUTE, DOLLAR, POUND]
	},
	'15_AstrologicalAspectMenu':{
		'tree' : [
			'16_AstrologicalAspectEnd',
			'16_AstrologicalAspectEnd',
			'16_AstrologicalAspectEnd',
			'16_AstrologicalAspectEnd',
			'16_AstrologicalAspectEnd',
			'16_AstrologicalAspectEnd'
		],
		'map' : [ONE, MUTE, DOLLAR, POUND, EURO, CONTROL]
	},
	'16_AstrologicalAspectEnd': {
		'tree' : ['15_AstrologicalAspectMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'17_CantRememberEnd': {
		'tree' : ['12_BirthCertificateMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'18_PeopleAreMoronsEnd':{
		'tree' : ['9_SocietyCulturePoliticsMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'19_PeopleAreEvilEnd':{
		'tree' : ['9_SocietyCulturePoliticsMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'20_EnvironmentEnd': '28_A_CloggedToiletorDrainMenu',
	'21_PhysicsMenu':{
		'tree' : [],
		'map' : []
	},
	'22_A_RetroactivePrecognitionEnd':{
		'tree' : [],
		'map' : []
	},
	'22_RetroactivePrecognitionEnd':{
		'tree' : [],
		'map' : []
	},
	'23_DrivingLicenseMenu':{
		'tree' : [],
		'map' : []
	},
	'24_UnderTheInfluenceEnd':{
		'tree' : [],
		'map' : []
	},
	'25_DiscriminationEnd':{
		'tree' : [],
		'map' : []
	},
	'26_RoadRageEnd':{
		'tree' : [],
		'map' : []
	},
	'27_QuantumSuicideEnd':{
		'tree' : [],
		'map' : []
	},
	'28_A_CloggedToiletorDrainMenu':{
		'tree' : [],
		'map' : []
	},
	'29_FavoriteTVEnd':{
		'tree' : [],
		'map' : []
	},
	'30_LegalizeCrimeEnd':{
		'tree' : [],
		'map' : []
	},
	'31_OverthrowEnd':{
		'tree' : [],
		'map' : []
	},
	'32_ComplaintAboutYourselfEnd': '33_UltimaThuleMainMenuOptionOne',
	'33_UltimaThuleMainMenuOptionOne':{
		'tree' : [
			'34_UtlitmaThuleEnd', 
			'34_UtlitmaThuleEnd', 
			'34_UtlitmaThuleEnd', 
			'34_UtlitmaThuleEnd'
		],
		'map' : TYPE_C
	},
	'34_UtlitmaThuleEnd': None,
	'35_ComlaintAboutComputerMenu':{
		'tree' : ['37_ComplaintAboutAnotherPersonMenu', '32_ComplaintAboutYourselfEnd'],
		'map' : [ONE, MUTE]
	},
	'36_ComplaintAboutHotlineOperatorsEnd': None,
	'37_ComplaintAboutAnotherPersonMenu':{
		'tree' : [
			'38_AnimalComplaintMenu',
			'58_MateMenu',
			'63_FriendComplaintsMenu',
			'68_FamilyMemberMenu',
			'76_AcquaintanceMenu',
			'83_StrangerMenuOption1',
			'37_ComplaintAboutAnotherPersonMenu'
		],
		'map' : TYPE_B
	},
	'38_AnimalComplaintMenu':{
		'tree' : [
			'39_AnimalBrokenVaseMenu',
			'41_StrayDogMenu',
			'46_MermaidsEnd',
			'47_AnimalBelongingToEmperorEnd', #what
			'47_AnimalBelongingToEmperorEnd',
			'48_FabulousAnimalMenu',
			'56_AnimalResemblesFlyEnd',
			'57_AnimalYouHaveEatenEnd',
			'38_AnimalComplaintMenu'
		], 
		'map' : [ONE, MUTE, DOLLAR, POUND, FOUR, EURO, CONTROL, COMMA, TEN]
	},
	'39_AnimalBrokenVaseMenu':{
		'tree' : [],
		'map' : []
	},
	'40_AnimalBrokenVaseEnd':[],
	'41_StrayDogMenu':{
		'tree' : [],
		'map' : []
	},
	'42_NightlifeEnd':{
		'tree' : [],
		'map' : []
	},
	'43_FaithfulnessEnd':{
		'tree' : [],
		'map' : []
	},
	'44_ProtectionEnd':{
		'tree' : [],
		'map' : []
	},
	'45_EuthanasiaAndMourningEnd':{
		'tree' : [],
		'map' : []
	},
	'46_MermaidsEnd':[],
	'47_AnimalBelongingToEmperorEnd':{
		'tree' : [],
		'map' : []
	},
	'48_FabulousAnimalMenu':{
		'tree' : [],
		'map' : []
	},
	'49_DodoBirdEnd':{
		'tree' : [],
		'map' : []
	},
	'50_MangroveAndCoelacanthEnd':{
		'tree' : [],
		'map' : []
	},
	'51_GorgonMenu':{
		'tree' : [],
		'map' : []
	},
	'52_YouHaveBeenTurnedToStoneEnd':{
		'tree' : [],
		'map' : []
	},
	'53_TurnedGorgonToStoneMenu':{
		'tree' : [],
		'map' : []
	},
	'54_AddInsultToInjuryEnd':{
		'tree' : [],
		'map' : []
	},
	'55_musiconly':{
		'tree' : [],
		'map' : []
	},
	'56_AnimalResemblesFlyEnd':{
		'tree' : [],
		'map' : []
	},
	'57_AnimalYouHaveEatenEnd':{
		'tree' : [],
		'map' : []
	},
	'58_MateMenu':{
		'tree' : [],
		'map' : []
	},
	'59_AccidentallyCalledYouMomEnd':{
		'tree' : [],
		'map' : []
	},
	'60_DoesntListenEnd':{
		'tree' : [],
		'map' : []
	},
	'61_IllegalAlienEnd':{
		'tree' : [],
		'map' : []
	},
	'62_UsesMindControlEnd':{
		'tree' : [],
		'map' : []
	},
	'63_FriendComplaintsMenu':{
		'tree' : [],
		'map' : []
	},
	'64_CocaineEnd':{
		'tree' : [],
		'map' : []
	},
	'65_BeckyEnd':{
		'tree' : [],
		'map' : []
	},
	'66_DogEnd':{
		'tree' : [],
		'map' : []
	},
	'67_ImaginaryFriendEnd':{
		'tree' : [],
		'map' : []
	},
	'68_FamilyMemberMenu':{
		'tree' : [],
		'map' : []
	},
	'69_BabyEnd':{
		'tree' : [],
		'map' : []
	},
	'70_AristocracyEnd':{
		'tree' : [],
		'map' : []
	},
	'71_SiblingEnd':{
		'tree' : [],
		'map' : []
	},
	'72_ParanormalStepMotherMenuA':{
		'tree' : [],
		'map' : []
	},
	'73_NoneApplyEnd':{
		'tree' : [],
		'map' : []
	},
	'74_AnyDoApplyEnd':{
		'tree' : [],
		'map' : []
	},
	'75_ParentEnd':{
		'tree' : [],
		'map' : []
	},
	'76_AcquaintanceMenu':{
		'tree' : [],
		'map' : []
	},
	'77_WaiterEnd':{
		'tree' : [],
		'map' : []
	},
	'78_YourNeighborMenu':{
		'tree' : [],
		'map' : []
	},
	'79_YourNeighborEnd':{
		'tree' : [],
		'map' : []
	},
	'80_DaveEnd':{
		'tree' : [],
		'map' : []
	},
	'81_SallyEnd':{
		'tree' : [],
		'map' : []
	},
	'82_IDontKnowThemEnd':{
		'tree' : [],
		'map' : []
	},
	'83_StrangerMenuOption1':{
		'tree' : [],
		'map' : []
	},
	'84_StrangerPromptOption1':{
		'tree' : [],
		'map' : []
	},
	'85_PopularLookingEndAndSartoriallyImpairedEnd':{
		'tree' : [],
		'map' : []
	},
	'86_HappyEnd':{
		'tree' : [],
		'map' : []
	},
	'87_TallEnd':{
		'tree' : [],
		'map' : []
	},
	'88_BovineEnd':{
		'tree' : [],
		'map' : []
	},
	'89_HomelessEnd':{
		'tree' : [],
		'map' : []
	},
	'90_LoudEnd':{
		'tree' : [],
		'map' : []
	},
	'91_DrunkAndCreepyEnd':{
		'tree' : [],
		'map' : []
	},
}

class EnoughIsEnough(MPServerAPI):
	def __init__(self):
		MPServerAPI.__init__(self)
		logging.basicConfig(filename=self.conf['d_files']['module']['log'], level=logging.DEBUG)

	def hear_hotline_start(self):

		if self.say(os.path.join("prompts", "1_GossipSection.wav"), interruptable=False):
			return self.route_next()

		return False

	def route_next(self, route=None):
		if route is None:
			route = '2_MainMenu'

		# go to terminus
		if KEY_MAP[route] is None:
			return self.say(os.path.join("prompts", "%s.wav" % route), interruptable=False) \
				and self.on_hang_up()

		# bounce to next route
		if type(KEY_MAP[route]) in [str, unicode]:
			return self.say(os.path.join("prompts", "%s.wav" % route), interruptable=False) \
				and self.route_next(route=KEY_MAP[route])

		choice = self.prompt(os.path.join("prompts", "%s.wav" % route), release_keys=KEY_MAP[route]['map'])
		next_route = KEY_MAP[route]['tree'][KEY_MAP[route]['map'].index(choice)]

		if type(next_route) is dict:
			return self.say(os.path.join("prompts", "%s.wav" % next_route.items()[0][0])) \
				and self.route_next(route=next_route.items()[0][1])
		else:
			return self.route_next(route=next_route)

		return False

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