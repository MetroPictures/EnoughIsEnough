import os, json, logging
from sys import argv, exit
from time import sleep

from core.api import MPServerAPI

# arbitrary at this point...
ONE = 3
TWO = 15
THREE = 16
MUTE = 13
DOLLAR = 14
POUND = 10
EURO = 11
FOUR = 6
TEN = 12
COMMAND = 9
CONTROL = 8
INFINITY = 7
COMMA = 5
PAUSE = 4

LOOP_SIGNAL = -1

TYPE_A = [ONE, MUTE, DOLLAR, POUND, FOUR, TEN]
TYPE_B = [ONE, MUTE, DOLLAR, POUND, FOUR, EURO, TEN]
TYPE_C = [ONE, MUTE, DOLLAR, POUND]
TYPE_D = [INFINITY, TEN]

KEY_MAP = {
	'2_MainMenu': {
		'tree' : [
			'3_ThingsInGeneralMenu', 
			'32_ComplaintAboutYourselfEnd',
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
			'6_CausePainEnd',
			'7_UselessEnd',
			'8_SphinxEnd',
			'4_BodiesMenu'
		],
		'map' : TYPE_B
	},
	'5_WeAreSorryEnd': {
		'tree' : ['4_BodiesMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
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
		'map' : TYPE_C
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
		'tree' : [
			'22_A_RetroactivePrecognitionEnd',
			'23_DrivingLicenseMenu',
			'27_QuantumSuicideEnd',
			'28_A_CloggedToiletorDrainMenu'
		],
		'map' : TYPE_C
	},
	'22_A_RetroactivePrecognitionEnd':'22_RetroactivePrecognitionEnd',
	'22_RetroactivePrecognitionEnd': '28_A_CloggedToiletorDrainMenu',
	'23_DrivingLicenseMenu':{
		'tree' : [
			'24_UnderTheInfluenceEnd', 
			'25_DiscriminationEnd', 
			'26_RoadRageEnd'
		],
		'map' : [ONE, MUTE, DOLLAR]
	},
	'24_UnderTheInfluenceEnd':{
		'tree' : ['21_PhysicsMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'25_DiscriminationEnd':'37_ComplaintAboutAnotherPersonMenu',
	'26_RoadRageEnd':'2_MainMenu',
	'27_QuantumSuicideEnd':'21_PhysicsMenu',
	'28_A_CloggedToiletorDrainMenu':{
		'tree' : ['29_FavoriteTVEnd', '30_LegalizeCrimeEnd', '31_OverthrowEnd'],
		'map' : [ONE, MUTE, DOLLAR]
	},
	'29_FavoriteTVEnd':{
		'tree' : ['28_A_CloggedToiletorDrainMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'30_LegalizeCrimeEnd':{
		'tree' : ['28_A_CloggedToiletorDrainMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'31_OverthrowEnd':{
		'tree' : ['28_A_CloggedToiletorDrainMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'32_ComplaintAboutYourselfEnd': '33_UltimaThuleMainMenuOptionOne',
	'33_UltimaThuleMainMenuOptionOne':{
		'tree' : [
			'34_UtlitmaThuleEnd', 
			'34_UtlitmaThuleEnd', 
			'34_UtlitmaThuleEnd', 
			'34_UtlitmaThuleEnd'
		],
		'map' : [ONE, TWO, THREE, FOUR]
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
		'tree' : ['40_AnimalBrokenVaseEnd'],
		'map' : [COMMAND]
	},
	'40_AnimalBrokenVaseEnd':None,
	'41_StrayDogMenu':{
		'tree' : [
			'42_NightlifeEnd', 
			'43_FaithfulnessEnd', 
			'44_ProtectionEnd', 
			'45_EuthanasiaAndMourningEnd'
		],
		'map' : [ONE, MUTE, DOLLAR, POUND]
	},
	'42_NightlifeEnd':{
		'tree' : ['38_AnimalComplaintMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'43_FaithfulnessEnd':'63_FriendComplaintsMenu',
	'44_ProtectionEnd':'33_UltimaThuleMainMenuOptionOne',
	'45_EuthanasiaAndMourningEnd':'33_UltimaThuleMainMenuOptionOne',
	'46_MermaidsEnd':{
		'tree' : ['38_AnimalComplaintMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'47_AnimalBelongingToEmperorEnd':'55_musiconly',
	'48_FabulousAnimalMenu':{
		'tree' : [
			'37_ComplaintAboutAnotherPersonMenu', #what
			'49_DodoBirdEnd', 
			'50_MangroveAndCoelacanthEnd',
			'50_MangroveAndCoelacanthEnd',
			'51_GorgonMenu'
		], 
		'map' : [ONE, MUTE, DOLLAR, POUND, FOUR]
	},
	'49_DodoBirdEnd':'3_ThingsInGeneralMenu',
	'50_MangroveAndCoelacanthEnd':'68_FamilyMemberMenu',
	'51_GorgonMenu':{
		'tree' : ['52_YouHaveBeenTurnedToStoneEnd', '53_TurnedGorgonToStoneMenu'],
		'map' : [ONE, MUTE]
	},
	'52_YouHaveBeenTurnedToStoneEnd':None,
	'53_TurnedGorgonToStoneMenu':{
		'tree' : ['54_AddInsultToInjuryEnd', '55_musiconly'],
		'map' : [ONE, MUTE]
	},
	'54_AddInsultToInjuryEnd':{
		'tree' : ['38_AnimalComplaintMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'55_musiconly':LOOP_SIGNAL,
	'56_AnimalResemblesFlyEnd':'21_PhysicsMenu',
	'57_AnimalYouHaveEatenEnd':'32_ComplaintAboutYourselfEnd',
	'58_MateMenu':{
		'tree' : [
			'59_AccidentallyCalledYouMomEnd', 
			'60_DoesntListenEnd',
			'61_IllegalAlienEnd',
			'62_UsesMindControlEnd'
		],
		'map' : TYPE_C
	},
	'59_AccidentallyCalledYouMomEnd':'2_MainMenu',
	'60_DoesntListenEnd':'58_MateMenu',
	'61_IllegalAlienEnd':'55_musiconly',
	'62_UsesMindControlEnd':'33_UltimaThuleMainMenuOptionOne',
	'63_FriendComplaintsMenu':{
		'tree' : [
			'64_CocaineEnd',
			'65_BeckyEnd',
			'66_DogEnd',
			'67_ImaginaryFriendEnd'
		],
		'map' : TYPE_C
	},
	'64_CocaineEnd':'55_musiconly',
	'65_BeckyEnd':{
		'tree' : ['63_FriendComplaintsMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'66_DogEnd':'38_AnimalComplaintMenu',
	'67_ImaginaryFriendEnd':{
		'tree' : ['63_FriendComplaintsMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'68_FamilyMemberMenu':{
		'tree' : [
			'69_BabyEnd',
			'70_AristocracyEnd',
			'71_SiblingEnd',
			'72_ParanormalStepMotherMenuA',
			'75_ParentEnd',
			'68_FamilyMemberMenu'
		],
		'map' : [ONE, MUTE, DOLLAR, POUND, FOUR, TEN]
	},
	'69_BabyEnd':'4_BodiesMenu',
	'70_AristocracyEnd':{
		'tree' : ['68_FamilyMemberMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'71_SiblingEnd':'38_AnimalComplaintMenu',
	'72_ParanormalStepMotherMenuA':{
		'tree' : ['73_NoneApplyEnd', '74_AnyDoApplyEnd'],
		'map' : [ONE, MUTE]
	},
	'73_NoneApplyEnd':None,
	'74_AnyDoApplyEnd':None,
	'75_ParentEnd':'76_AcquaintanceMenu',
	'76_AcquaintanceMenu':{
		'tree' : [
			'77_WaiterEnd',
			'78_YourNeighborMenu',
			'80_DaveEnd',
			'81_SallyEnd',
			'82_IDontKnowThemEnd'
		],
		'map' : [ONE, MUTE, DOLLAR, POUND, FOUR]
	},
	'77_WaiterEnd':None,
	'78_YourNeighborMenu':{
		'tree' : ['79_YourNeighborEnd'],
		'map' : [COMMAND]
	},
	'79_YourNeighborEnd':None,
	'80_DaveEnd':{
		'tree' : ['76_AcquaintanceMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'81_SallyEnd':{
		'tree' : ['76_AcquaintanceMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'82_IDontKnowThemEnd':{
		'tree' : ['76_AcquaintanceMenu', '2_MainMenu'],
		'map' : TYPE_D
	},
	'83_StrangerMenuOption1':{
		'tree' : [
			'85_PopularLookingEndAndSartoriallyImpairedEnd',
			'86_HappyEnd',
			'88_BovineEnd',
			'89_HomelessEnd',
			'91_DrunkAndCreepyEnd',
			'85_PopularLookingEndAndSartoriallyImpairedEnd',
			'83_StrangerMenuOption1'
		],
		'map' : [ONE, MUTE, DOLLAR, POUND, FOUR, EURO, CONTROL, COMMA, PAUSE, TEN]
	},
	'84_StrangerPromptOption1':{
		'tree' : ['83_StrangerMenuOption1'],
		'map' : [COMMAND]
	},
	'85_PopularLookingEndAndSartoriallyImpairedEnd':{
		'tree' : ['83_StrangerMenuOption1', '2_MainMenu'],
		'map' : TYPE_D
	},
	'86_HappyEnd':{
		'tree' : ['83_StrangerMenuOption1', '2_MainMenu'],
		'map' : TYPE_D
	},
	'87_TallEnd':{
		'tree' : ['83_StrangerMenuOption1', '2_MainMenu'],
		'map' : TYPE_D
	},
	'88_BovineEnd':{
		'tree' : ['83_StrangerMenuOption1', '2_MainMenu'],
		'map' : TYPE_D
	},
	'89_HomelessEnd':{
		'tree' : ['83_StrangerMenuOption1', '2_MainMenu'],
		'map' : TYPE_D
	},
	'90_LoudEnd':{
		'tree' : ['83_StrangerMenuOption1', '2_MainMenu'],
		'map' : TYPE_D
	},
	'91_DrunkAndCreepyEnd':{
		'tree' : ['83_StrangerMenuOption1', '2_MainMenu'],
		'map' : TYPE_D
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
			return self.say(os.path.join("prompts", "%s.wav" % route), interruptable=False)

		# bounce to next route
		if type(KEY_MAP[route]) in [str, unicode]:
			return self.say(os.path.join("prompts", "%s.wav" % route), interruptable=False) \
				and self.route_next(route=KEY_MAP[route])

		if type(KEY_MAP[route]) is int:
			if KEY_MAP[route] == LOOP_SIGNAL:
				return self.say(os.path.join("prompts", "%s.wav" % route), interruptable=False) \
					and self.route_next(route=route)

		choice = self.prompt(os.path.join("prompts", "%s.wav" % route), release_keys=KEY_MAP[route]['map'])
		next_route = KEY_MAP[route]['tree'][KEY_MAP[route]['map'].index(choice)]

		return self.route_next(route=next_route)

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