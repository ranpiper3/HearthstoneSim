from CardTypes import *
from Triggers_Auras import *

import copy

from numpy.random import choice as npchoice
from numpy.random import randint as nprandint
from numpy.random import shuffle as npshuffle

import numpy as np

def extractfrom(target, listObj):
	try: return listObj.pop(listObj.index(target))
	except: return None
	
def fixedList(listObject):
	return listObject[0:len(listObject)]

def PRINT(game, string, *args):
	if game.GUI:
		if not game.mode: game.GUI.printInfo(string)
	elif not game.mode: print("game's guide mode is 0\n", string)

SVClasses = ["Forestcraft","Swordcraft","Runecraft","Drangoncraft","Shadowcraft","Bloodcraft","Havencraft","Portalcraft"]
Classes = ["Demon Hunter", "Druid", "Hunter", "Mage", "Monk", "Paladin", "Priest", "Rogue", "Shaman","Warlock", "Warrior",
		   "Forestcraft","Swordcraft","Runecraft","Drangoncraft","Shadowcraft","Bloodcraft","Havencraft","Portalcraft"]
ClassesandNeutral = ["Demon Hunter", "Druid", "Hunter", "Mage", "Monk", "Paladin", "Priest", "Rogue", "Shaman",
					"Warlock", "Warrior", "Neutral","Forestcraft","Swordcraft","Runecraft","Drangoncraft","Shadowcraft","Bloodcraft","Havencraft","Portalcraft"]


#SV_Basic cards and heroes

class Evolve(HeroPower):
	mana, name, requireTarget = 0, "Evolve", True
	index = "Shadowverse~Hero Power~0~Evolve"
	description = "Evolve an unevolved friendly minion."

	def available(self):
		if self.selectableFriendlyMinionExists() and self.heroPowerTimes < self.heroPowerChances_base + \
				self.heroPowerChances_extra and \
				self.Game.Counters.turns[self.ID] >= \
				self.Game.Counters.numEvolutionTurn[self.ID]:
			if self.Game.Counters.numEvolutionPoint[self.ID] > 0:
				return True
			else:
				hasFree = False
				for minion in self.Game.minionsonBoard(self.ID):
					if isinstance(minion, ShadowverseMinion) and minion.keyWords["Free Evolve"] > 0:
						hasFree = True
						break
				return hasFree
		return False

	def targetCorrect(self, target, choice=0):
		if target.cardType == "Minion" and target.ID == self.ID and target.onBoard \
				and isinstance(target, ShadowverseMinion) and target.status["Evolved"] < 1 \
				and target.marks["Can't Evolve"] == 0:
			if self.Game.Counters.numEvolutionPoint[self.ID] == 0:
				return target.marks["Free Evolve"] > 0
			else:
				return True
		return False

	def effect(self, target, choice=0):
		if target.marks["Free Evolve"] == 0:
			self.Game.Counters.numEvolutionPoint[self.ID] -= 1
		target.evolve()
		target.inHandEvolving()
		return 0

class Arisa(Hero):
	Class, name, heroPower = "Forestcraft", "Erika", Evolve

	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.health, self.health_upper, self.armor = 20, 20, 0

class Erika(Hero):
	Class, name, heroPower = "Swordcraft", "Erika", Evolve

	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.health, self.health_upper, self.armor = 20, 20, 0

class Isabelle(Hero):
	Class, name, heroPower = "Runecraft", "Erika", Evolve

	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.health, self.health_upper, self.armor = 20, 20, 0

class Rowen(Hero):
	Class, name, heroPower = "Dragoncraft", "Erika", Evolve

	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.health, self.health_upper, self.armor = 20, 20, 0

class Luna(Hero):
	Class, name, heroPower = "Shadowcraft", "Erika", Evolve

	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.health, self.health_upper, self.armor = 20, 20, 0

class Urias(Hero):
	Class, name, heroPower = "Bloodcraft", "Erika", Evolve

	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.health, self.health_upper, self.armor = 20, 20, 0

class Eris(Hero):
	Class, name, heroPower = "Havencraft", "Erika", Evolve

	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.health, self.health_upper, self.armor = 20, 20, 0

class Yuwan(Hero):
	Class, name, heroPower = "Portalcraft", "Erika", Evolve

	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.health, self.health_upper, self.armor = 20, 20, 0


class ShadowverseMinion(Minion):
	attackAdd, healthAdd = 2, 2
	
	def blank_init(self, Game, ID):
		super().blank_init(Game, ID)
		self.targets = []
		
	def evolve(self):
		if self.status["Evolved"] < 1:
			self.attack_0 += self.attackAdd
			self.health_0 += self.healthAdd
			self.statReset(self.attack + self.attackAdd, self.health + self.healthAdd)
			self.status["Evolved"] += 1
			PRINT(self, self.name + " evolves.")
			self.Game.Counters.evolvedThisGame[self.ID] += 1
			for card in self.Game.Hand_Deck.hands[self.ID]:
				if isinstance(card, ShadowverseMinion) and "UB" in card.marks:
					card.marks["UB"] -= 1
			self.inEvolving()
			
	def inEvolving(self):
		return
		
	def inHandEvolving(self, target=None):
		return
		
	def findTargets(self, comment="", choice=0):
		game, targets, indices, wheres = self.Game, [], [], []
		for ID in range(1, 3):
			if self.targetCorrect(game.heroes[ID], choice) and (comment == "" or self.canSelect(game.heroes[ID])):
				targets.append(game.heroes[ID])
				indices.append(ID)
				wheres.append("hero")
			where = "minion%d"%ID
			for obj in game.minionsandAmuletsonBoard(ID):
				if self.targetCorrect(obj, choice) and (comment == "" or self.canSelect(obj)):
					targets.append(obj)
					indices.append(obj.position)
					wheres.append(where)
			where = "hand%d"%ID
			for i, card in enumerate(game.Hand_Deck.hands[ID]):
				if self.targetCorrect(card, choice):
					targets.append(obj)
					indices.append(i)
					wheres.append(where)
					
		if targets: return targets, indices, wheres
		else: return [None], [0], ['']
		
	def actionable(self):
		return self.ID == self.Game.turn and \
				(not self.newonthisSide or (self.status["Borrowed"] > 0 or self.keyWords["Charge"] > 0 or self.keyWords["Rush"] > 0 or self.status["Evolved"] > 0))
				
	def canAttack(self):
		return self.actionable() and self.status["Frozen"] < 1 \
				and self.attChances_base + self.attChances_extra > self.attTimes \
				and self.marks["Can't Attack"] < 1
				
	def createCopy(self, game):
		if self in game.copiedObjs:
			return game.copiedObjs[self]
		else:
			Copy = type(self)(game, self.ID)
			game.copiedObjs[self] = Copy
			Copy.mana = self.mana
			Copy.manaMods = [mod.selfCopy(Copy) for mod in self.manaMods]
			Copy.attack, Copy.attack_0, Copy.attack_Enchant = self.attack, self.attack_0, self.attack_Enchant
			Copy.health_0, Copy.health, Copy.health_max = self.health_0, self.health, self.health_max
			Copy.tempAttChanges = copy.deepcopy(self.tempAttChanges)
			Copy.statbyAura = [self.statbyAura[0], self.statbyAura[1], [aura_Receiver.selfCopy(Copy) for aura_Receiver in self.statbyAura[2]]]
			for key, value in self.keyWordbyAura.items():
				if key != "Auras": Copy.keyWordbyAura[key] = value
				else: Copy.keyWordbyAura[key] = [aura_Receiver.selfCopy(Copy) for aura_Receiver in self.keyWordbyAura["Auras"]]
			Copy.keyWords = copy.deepcopy(self.keyWords)
			Copy.marks = copy.deepcopy(self.marks)
			Copy.status = copy.deepcopy(self.status)
			Copy.identity = copy.deepcopy(self.identity)
			Copy.onBoard, Copy.inHand, Copy.inDeck, Copy.dead = self.onBoard, self.inHand, self.inDeck, self.dead
			if hasattr(self, "progress"): Copy.progress = self.progress
			Copy.effectViable, Copy.evanescent, Copy.activated, Copy.silenced = self.effectViable, self.evanescent, self.activated, self.silenced
			Copy.newonthisSide, Copy.firstTimeonBoard = self.newonthisSide, self.firstTimeonBoard
			Copy.sequence, Copy.position = self.sequence, self.position
			Copy.attTimes, Copy.attChances_base, Copy.attChances_extra = self.attTimes, self.attChances_base, self.attChances_extra
			Copy.options = [option.selfCopy(Copy) for option in self.options]
			for key, value in self.triggers.items():
				Copy.triggers[key] = [getattr(Copy, func.__qualname__.split(".")[1]) for func in value]
			Copy.appearResponse = [getattr(Copy, func.__qualname__.split(".")[1]) for func in self.appearResponse]
			Copy.disappearResponse = [getattr(Copy, func.__qualname__.split(".")[1]) for func in self.disappearResponse]
			Copy.silenceResponse = [getattr(Copy, func.__qualname__.split(".")[1]) for func in self.silenceResponse]
			for key, value in self.auras.items():
				Copy.auras[key] = value.createCopy(game)
			Copy.deathrattles = [trig.createCopy(game) for trig in self.deathrattles]
			Copy.trigsBoard = [trig.createCopy(game) for trig in self.trigsBoard]
			Copy.trigsHand = [trig.createCopy(game) for trig in self.trigsHand]
			Copy.trigsDeck = [trig.createCopy(game) for trig in self.trigsDeck]
			Copy.history = copy.deepcopy(self.history)
			Copy.attackAdd = self.attackAdd
			Copy.healthAdd = self.healthAdd
			self.assistCreateCopy(Copy)
			return Copy
			
			
class AccelerateMinion(ShadowverseMinion):
	accelerate, accelerateSpell = 0, None
	def getMana(self):
		return min(self.accelerate, self.mana) if self.Game.Manas.manas[self.ID] < self.mana else self.mana
		
	def getTypewhenPlayed(self):
		return "Spell" if self.willAccelerate() else "Minion"
		
	def willAccelerate(self):
		curMana = self.Game.Manas.manas[self.ID]
		return curMana < self.mana and curMana >= type(self).accelerate
		
	def becomeswhenPlayed(self):
		return type(self).accelerateSpell(self.Game, self.ID) if self.willAccelerate() else self, self.getMana()
		
		
class ShadowverseSpell(Spell):
	def __init__(self, Game, ID):
		super().__init__(Game, ID)
		self.targets = []
		
	def played(self, target=None, choice=0, mana=0, posinHand=-2, comment=""):
		repeatTimes = 2 if self.Game.status[self.ID]["Spells x2"] > 0 else 1
		if self.Game.GUI:
			self.Game.GUI.showOffBoardTrig(self)
			self.Game.GUI.wait(500)
		self.Game.sendSignal("SpellPlayed", self.ID, self, None, mana, "", choice)
		#假设SV的法术在选取上不触发重导向扳机	
		self.Game.gathertheDead()
		self.Game.Counters.spellsonFriendliesThisGame[self.ID] += [self.index for obj in target if obj.ID == self.ID]
		#假设SV的法术不受到"对相邻的法术也释放该法术"的影响
		for i in range(repeatTimes):
			for obj in target: #每个目标都会检测是否记录该法术的作用历史
				if (obj.type == "Minion" or obj.type == "Amulet") and obj.onBoard:
					obj.history["Spells Cast on This"].append(self.index)
			target = self.whenEffective(target, comment, choice, posinHand)
			
		#仅触发风潮，星界密使等的光环移除扳机。“使用一张xx牌之后”的扳机不在这里触发，而是在Game的playSpell函数中结算。
		self.Game.sendSignal("SpellBeenCast", self.Game.turn, self, None, 0, "", choice)
		self.Game.gathertheDead() #At this point, the minion might be removed/controlled by Illidan/Juggler combo.		
		if self.Game.GUI: self.Game.GUI.eraseOffBoardTrig(self.ID)
		
		
class VesperWitchhunter_Accelerate(ShadowverseSpell):
	Class, name = "Runecraft", "Vesper, Witchhunter"
	requireTarget, mana = True, 2
	index = "SV_Basic~Runecraft~Spell~2~Vesper, Witchhunter~Uncollectible"
	description = "Deal 1 damage to an enemy"
	def targetCorrect(self, target, choice=0):
		if isinstance(target, list): target = target[0]
		return (target.type == "Minion" or target.type == "Hero") and target.ID != self.ID and target.onBoard
		
	def whenEffective(self, target=None, comment="", choice=0, posinHand=-2):
		if target:
			damage = (1 + self.countSpellDamage()) * (2 ** self.countDamageDouble())
			PRINT(self.Game, "Vesper, Witchhunter, as spell, deals %d damage to enemy %s."%(damage, target[0].name))
			self.dealsDamage(target[0], damage)
		return target
		
class VesperWitchhunter(AccelerateMinion):
	Class, race, name = "Runecraft", "", "Vesper, Witchhunter"
	mana, attack, health = 4, 3, 3
	index = "SV_Basic~Runecraft~4~3~3~Minion~None~Vesper, Witchhunter~Accelerate~Fanfare"
	requireTarget, keyWord, description = True, "", "Accelerate 2: Deal 1 damage to an enemy. Fanfare: xxx. Deal 3 damage to an enemy minion, and deal 1 damage to the enemy hero"
	accelerate, accelerateSpell = 2, VesperWitchhunter_Accelerate
	
	def effectCanTrigger(self):
		self.effectViable = self.willAccelerate()
		
	def returnTrue(self, choice=0):
		return not self.targets
		
	def available(self):
		return self.selectableEnemyExists()
		
	def targetExists(self, choice=0):
		return self.selectableEnemyMinionExists()
		
	def targetCorrect(self, target, choice=0):
		if isinstance(target, list): target = target[0]
		return (target.type == "Minion" or (self.willAccelerate() and target.type == "Hero")) \
				and target.ID != self.ID and target.onBoard
				
	def whenEffective(self, target=None, comment="", choice=0, posinHand=-2):
		if target:
			PRINT(self.Game, "Vesper, Witchhunter's Fanfare deals 3 damage to enemy minion %s and 1 damage to the enemy hero."%target[0].name)
			self.dealsDamage(target[0], 3)
			self.dealsDamage(self.Game.heroes[3-self.ID], 1)
		return target
		
		
class Terrorformer(ShadowverseMinion):
	Class, race, name = "Forestcraft", "", "Terrorformer"
	mana, attack, health = 6, 4, 4
	index = "SV_Basic~Forestcraft~Minion~6~4~4~None~Terrorformer~Fusion~Fanfare"
	requireTarget, keyWord, description = True, "", "Fusion: Forestcraft followers that originally cost 2 play points or more. Whenever 2 or more cards are fused to this card at once, gain +2/+0 and draw a card. Fanfare: If at least 2 cards are fused to this card, gain Storm. Then, if at least 4 cards are fused to this card, destroy an enemy follower."
	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.fusion = 1
		self.fusionMaterials = 0
		
	def returnTrue(self, choice=0): #需要targets里面没有目标，且有3个融合素材
		return not self.targets and self.fusionMaterials > 3
		
	def targetCorrect(self, target, choice=0):
		if isinstance(target, list): target = target[0]
		return target.type == "Minion" and target.ID != self.ID and target.onBoard
		
	def findFusionMaterials(self):
		return [card for card in self.Game.Hand_Deck.hands[self.ID] if card.type == "Minion" and card != self and type(card).mana > 1]
		
	def fusionDecided(self, objs):
		if objs:
			self.fusionMaterials += len(objs)
			self.Game.Hand_Deck.extractfromHand(self, enemyCanSee=True)
			for obj in objs: self.Game.Hand_Deck.extractfromHand(obj, enemyCanSee=True)
			self.Game.Hand_Deck.addCardtoHand(self, self.ID)
			if len(objs) > 1:
				PRINT(self.Game, "Terrorformer's Fusion involves more than 1 minion. It gains +2/+0 and lets player draw a card")
				self.buffDebuff(2, 0)
				self.Game.Hand_Deck.drawCard(self.ID)
			self.fusion = 0 #一张卡每回合只有一次融合机会
			
	def whenEffective(self, target=None, comment="", choice=0, posinHand=-2):
		PRINT(self.Game, "Terrorformer's Fanfare gives minion Storm as it has no less than 2 fusion materials")
		self.getsKeyword("Charge")
		if target and self.fusionMaterials > 3:
			PRINT(self.Game, "Terrorformer's Fanfare destroys enemy follower"%target[0].name)
			target[0].dead = True
		return target
		
#当费用不足以释放随从本体但又高于结晶费用X时，打出会以结晶方式打出，此时随从变形为一张护符打出在战场上，护符名为结晶：{随从名}，效果与随从本体无关。可能会具有本体不具有的额外种族。不会被本体减费影响，但若本体费用低于结晶费用则结晶无法触发。同一个随从可以同时具有结晶和爆能强化。
class CrystallizeMinion(ShadowverseMinion):
	crystallize, crystallizeAmulet = 0, None
	def getMana(self):
		return min(self.crystallize, self.mana) if self.Game.Manas.manas[self.ID] < self.mana else self.mana
		
	def getTypewhenPlayed(self):
		return "Amulet" if self.willCrystallize() else "Minion"
		
	def willCrystallize(self):
		curMana = self.Game.Manas.manas[self.ID]
		return curMana < self.mana and curMana >= type(self).crystallize
		
	def becomeswhenPlayed(self):
		return type(self).crystallizeAmulet(self.Game, self.ID) if self.willCrystallize() else self, self.getMana()
		
		
class Amulet(Dormant):
	Class, race, name = "Neutral", "", "Vanilla"
	mana = 2
	index = "Vanilla~Neutral~2~Amulet~None~Vanilla~Uncollectible"
	requireTarget, description = False, ""
	
	def blank_init(self, Game, ID):
		self.Game, self.ID = Game, ID
		self.Class, self.name = type(self).Class, type(self).name
		self.type, self.race = "Amulet", type(self).race
		# 卡牌的费用和对于费用修改的效果列表在此处定义
		self.mana, self.manaMods = type(self).mana, []
		self.tempAttChanges = []  # list of tempAttChange, expiration timepoint
		self.description = type(self).description
		# 当一个实例被创建的时候，其needTarget被强行更改为returnTrue或者是returnFalse，不论定义中如何修改needTarget(self, choice=0)这个函数，都会被绕过。需要直接对returnTrue()函数进行修改。
		self.needTarget = self.returnTrue if type(self).requireTarget else self.returnFalse
		# Some state of the minion represented by the marks
		# 复制出一个游戏内的Copy时要重新设为初始值的attr
		# First two are for card authenticity verification. The last is to check if the minion has ever left board.
		# Princess Talanji needs to confirm if a card started in original deck.
		self.identity = [np.random.rand(), np.random.rand(), np.random.rand()]
		self.dead = False
		self.effectViable, self.evanescent = False, False
		self.newonthisSide, self.firstTimeonBoard = True, True  # firstTimeonBoard用于防止随从在休眠状态苏醒时再次休眠，一般用不上
		self.onBoard, self.inHand, self.inDeck = False, False, False
		self.activated = False  # This mark is for minion state change, such as enrage.
		# self.sequence records the number of the minion's appearance. The first minion on board has a sequence of 0
		self.sequence, self.position = -1, -2
		self.keyWords = {}
		self.marks = {"Evasive": 0, "Enemy Effect Evasive": 0, "Can't Break": 0}
		self.status = {}
		self.auras = {}
		self.options = []  # For Choose One minions.
		self.overload, self.chooseOne, self.magnetic = 0, 0, 0
		self.silenced = False
		
		self.triggers = {"Discarded": [], "StatChanges": [], "Drawn": []}
		self.appearResponse, self.disappearResponse, self.silenceResponse = [], [], []
		self.deathrattles = []  # 随从的亡语的触发方式与场上扳机一致，诸扳机之间与
		self.trigsBoard, self.trigsHand, self.trigsDeck = [], [], []
		self.history = {"Spells Cast on This": [],
						"Magnetic Upgrades": {"Deathrattles": [], "Triggers": []
											  }
						}
		self.targets = []
		
	def applicable(self, target):
		return target != self
		
	"""Handle the trigsBoard/inHand/inDeck of minions based on its move"""
	def appears(self):
		PRINT(self.Game, "%s appears on board." % self.name)
		self.newonthisSide = True
		self.onBoard, self.inHand, self.inDeck = True, False, False
		self.dead = False
		self.mana = type(self).mana  # Restore the minion's mana to original value.
		for value in self.auras.values():
			PRINT(self.Game, "Now starting amulet {}'s Aura {}".format(self.name, value))
			value.auraAppears()
		# 随从入场时将注册其场上扳机和亡语扳机
		for trig in self.trigsBoard + self.deathrattles:
			trig.connect()  # 把(obj, signal)放入Game.triggersonBoard中
		# Mainly mana aura minions, e.g. Sorcerer's Apprentice.
		for func in self.appearResponse: func()
		# The buffAuras/hasAuras will react to this signal.
		self.Game.sendSignal("AmuletAppears", self.ID, self, None, 0, "")
		for func in self.triggers["StatChanges"]: func()
		
	def disappears(self, deathrattlesStayArmed=True):  # The minion is about to leave board.
		self.onBoard, self.inHand, self.inDeck = False, False, False
		# Only the auras and disappearResponse will be invoked when the minion switches side.
		for value in self.auras.values():
			value.auraDisappears()
		# 随从离场时清除其携带的普通场上扳机，但是此时不考虑亡语扳机
		for trig in self.trigsBoard:
			trig.disconnect()
		if deathrattlesStayArmed == False:
			for trig in self.deathrattles:
				trig.disconnect()
		# 如果随从有离场时需要触发的函数，在此处理
		for func in self.disappearResponse: func()
		self.activated = False
		self.Game.sendSignal("AmuletDisappears", self.ID, None, self, 0, "")
		
	def STATUSPRINT(self):
		PRINT(self.Game, "Game is {}.".format(self.Game))
		PRINT(self.Game,
			  "Amulet: %s. ID: %d Race: %s\nDescription: %s" % (self.name, self.ID, self.race, self.description))
		if self.manaMods != []:
			PRINT(self.Game, "\tCarries mana modification:")
			for manaMod in self.manaMods:
				if manaMod.changeby != 0:
					PRINT(self.Game, "\t\tChanged by %d" % manaMod.changeby)
				else:
					PRINT(self.Game, "\t\tChanged to %d" % manaMod.changeto)
		if self.trigsBoard != []:
			PRINT(self.Game, "\tAmulet's trigsBoard")
			for trigger in self.trigsBoard:
				PRINT(self.Game, "\t{}".format(type(trigger)))
		if self.trigsHand != []:
			PRINT(self.Game, "\tAmulet's trigsHand")
			for trigger in self.trigsHand:
				PRINT(self.Game, "\t{}".format(type(trigger)))
		if self.trigsDeck != []:
			PRINT(self.Game, "\tAmulet's trigsDeck")
			for trigger in self.trigsDeck:
				PRINT(self.Game, "\t{}".format(type(trigger)))
		if self.auras != {}:
			PRINT(self.Game, "Amulet's aura")
			for key, value in self.auras.items():
				PRINT(self.Game, "{}".format(value))
		if self.deathrattles != []:
			PRINT(self.Game, "\tMinion's Deathrattles:")
			for trigger in self.deathrattles:
				PRINT(self.Game, "\t{}".format(type(trigger)))

	def afterSwitchSide(self, activity):
		self.newonthisSide = True
		
	# Whether the minion can select the attack target or not.
	def canAttack(self):
		return False
		
	def canAttackTarget(self, target):
		return False
		
	def deathResolution(self, attackbeforeDeath, triggersAllowed_WhenDies, triggersAllowed_AfterDied):
		self.Game.sendSignal("AmuletDestroys", self.Game.turn, None, self, attackbeforeDeath, "", 0,
							 triggersAllowed_WhenDies)
		for trig in self.deathrattles:
			trig.disconnect()
		self.Game.sendSignal("AmuletDestroyed", self.Game.turn, None, self, 0, "", 0, triggersAllowed_AfterDied)
		
	# Minions that initiates discover or transforms self will be different.
	# For minion that transform before arriving on board, there's no need in setting its onBoard to be True.
	# By the time this triggers, death resolution caused by Illidan/Juggler has been finished.
	# If Brann Bronzebeard/ Mayor Noggenfogger has been killed at this point, they won't further affect the battlecry.
	# posinHand在played中主要用于记录一张牌是否是从手牌中最左边或者最右边打出（恶魔猎手职业关键字）
	def played(self, target=None, choice=0, mana=0, posinHand=-2, comment=""):
		self.appears()
		self.Game.sendSignal("AmuletPlayed", self.ID, self, target, mana, "", choice)
		self.Game.sendSignal("AmuletSummoned", self.ID, self, target, mana, "")
		self.Game.gathertheDead()  # At this point, the minion might be removed/controlled by Illidan/Juggler combo.
		#假设不触发重导向扳机
		num = 1
		if "~Fanfare" in self.index and self.Game.status[self.ID]["Battlecry x2"] + self.Game.status[self.ID]["Shark Battlecry x2"] > 0:
			num = 2
		for i in range(num):
			target = self.whenEffective(target, "", choice, posinHand)
			
		# 结算阶段结束，处理死亡情况，不处理胜负问题。
		self.Game.gathertheDead()
		return target
		
	"""buffAura effect, Buff/Debuff, stat reset, copy"""
	# 在原来的Game中创造一个Copy
	def selfCopy(self, ID, mana=False):
		Copy = self.hardCopy(ID)
		# 随从的光环和亡语复制完全由各自的selfCopy函数负责。
		Copy.activated, Copy.onBoard, Copy.inHand, Copy.inDeck = False, False, False, False
		size = len(Copy.manaMods)  # 去掉牌上的因光环产生的费用改变
		for i in range(size):
			if Copy.manaMods[size - 1 - i].source:
				Copy.manaMods.pop(size - 1 - i)
		# 在一个游戏中复制出新实体的时候需要把这些值重置
		Copy.identity = [np.random.rand(), np.random.rand(), np.random.rand()]
		Copy.dead = False
		Copy.effectViable, Copy.evanescent = False, False
		Copy.newonthisSide, Copy.firstTimeonBoard = True, True  # firstTimeonBoard用于防止随从在休眠状态苏醒时再次休眠，一般用不上
		Copy.onBoard, Copy.inHand, Copy.inDeck = False, False, False
		Copy.activated = False
		Copy.sequence, Copy.position = -1, -2
		Copy.attTimes, Copy.attChances_base, Copy.attChances_extra = 0, 0, 0
		return Copy
		
	def createCopy(self, game):
		if self in game.copiedObjs:
			return game.copiedObjs[self]
		else:
			Copy = type(self)(game, self.ID)
			game.copiedObjs[self] = Copy
			Copy.mana = self.mana
			Copy.manaMods = [mod.selfCopy(Copy) for mod in self.manaMods]
			Copy.marks = copy.deepcopy(self.marks)
			Copy.identity = copy.deepcopy(self.identity)
			Copy.onBoard, Copy.inHand, Copy.inDeck, Copy.dead = self.onBoard, self.inHand, self.inDeck, self.dead
			if hasattr(self, "progress"): Copy.progress = self.progress
			Copy.effectViable, Copy.evanescent, Copy.activated, Copy.silenced = self.effectViable, self.evanescent, self.activated, self.silenced
			Copy.newonthisSide, Copy.firstTimeonBoard = self.newonthisSide, self.firstTimeonBoard
			Copy.sequence, Copy.position = self.sequence, self.position
			Copy.options = [option.selfCopy(Copy) for option in self.options]
			for key, value in self.triggers.items():
				Copy.triggers[key] = [getattr(Copy, func.__qualname__.split(".")[1]) for func in value]
			Copy.appearResponse = [getattr(Copy, func.__qualname__.split(".")[1]) for func in self.appearResponse]
			Copy.disappearResponse = [getattr(Copy, func.__qualname__.split(".")[1]) for func in self.disappearResponse]
			Copy.silenceResponse = [getattr(Copy, func.__qualname__.split(".")[1]) for func in self.silenceResponse]
			for key, value in self.auras.items():
				Copy.auras[key] = value.createCopy(game)
			Copy.deathrattles = [trig.createCopy(game) for trig in self.deathrattles]
			Copy.trigsBoard = [trig.createCopy(game) for trig in self.trigsBoard]
			Copy.trigsHand = [trig.createCopy(game) for trig in self.trigsHand]
			Copy.trigsDeck = [trig.createCopy(game) for trig in self.trigsDeck]
			Copy.history = copy.deepcopy(self.history)
			self.assistCreateCopy(Copy)
			return Copy
			
			
class SacredPlea(Amulet):
	Class, race, name = "Havencraft", "", "Sacred Plea"
	mana = 1
	index = "SV_Basic~Havencraft~1~Amulet~None~Sacred Plea~Last Words"
	requireTarget, description = False, "Countdown 3. Last Words: Draw 2 cards"
	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.trigsBoard = [Trig_SacredPlea(self)]
		self.deathrattles = [Draw2Cards(self)]
		
class Trig_SacredPlea(TrigBoard):
	def __init__(self, entity):
		self.blank_init(entity, ["TurnStarts"])
		self.counter = 3
		
	def canTrigger(self, signal, ID, subject, target, number, comment, choice=0):
		return self.entity.onBoard and ID == self.entity.ID
		
	def effect(self, signal, ID, subject, target, number, comment, choice=0):
		PRINT(self.entity.Game, "At the start of turn, Sacred Plea's countdown -1")
		self.counter -= 1
		if self.counter < 1:
			PRINT(self.entity.Game, "Sacred Plea's countdown is 0 and destroys itself")
			self.entity.dead = True
			
class Draw2Cards(Deathrattle_Minion):
	def effect(self, signal, ID, subject, target, number, comment, choice=0):
		PRINT(self.entity.Game, "Deathrattle: Draw 2 cards triggers.")
		self.entity.Game.Hand_Deck.drawCard(self.entity.ID)
		self.entity.Game.Hand_Deck.drawCard(self.entity.ID)
		
		
class AirboundBarrage(ShadowverseSpell):
	Class, name = "Forestcraft", "Airbound Barrage"
	requireTarget, mana = True, 1
	index = "SV_Basic~Forestcraft~Spell~1~Airbound Barrage"
	description = "Return an allied follower or amulet to your hand. Then deal 3 damage to an enemy follower.(Can be played only when both a targetable allied card and enemy card are in play.)"
	def returnTrue(self, choice=0):
		return len(self.targets) < 2
		
	def available(self):
		return (self.selectableFriendlyMinionExists() or self.selectableFriendlyAmuletExists()) and self.selectableEnemyMinionExists()
		
	def targetCorrect(self, target, choice=0):
		if isinstance(target, list):
			allied, enemy = target[0], target[1]
			return (allied.type == "Minion" or allied.type == "Amulet") and allied.onBoard and allied.ID == self.ID and enemy.type == "Minion" and enemy.ID != self.ID and enemy.onBoard
		else:
			if self.targets: #When checking the 2nd target
				return target.type == "Minion" and target.ID != self.ID and target.onBoard
			else: #When checking the 1st target
				return (target.type == "Minion" or target.type == "Amulet") and target.ID == self.ID and target.onBoard
				
	def whenEffective(self, target=None, comment="", choice=0, posinHand=-2):
		if target:
			allied, enemy = target[0], target[1]
			self.Game.returnMiniontoHand(allied, deathrattlesStayArmed=False)
			damage = (3 + self.countSpellDamage()) * (2 ** self.countDamageDouble())
			PRINT(self.Game, "Airbound Barrage deals %d damage to enemy %s."%(damage, enemy.name))
			self.dealsDamage(enemy, damage)
		return target
		
		
class RuinwebSpider_Amulet(Amulet):
	Class, race, name = "Bloodcraft", "", "Ruinweb Spider"
	mana = 2
	index = "SV_Basic~Bloodcraft~2~Amulet~None~Ruinweb Spider~Last Words"
	requireTarget, description = False, "Countdown 3. Last Words: Draw 2 cards"
	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.trigsBoard = [Trig_RuinwebSpider_Amulet(self)]
		self.deathrattles = [SummonaRuinwebSpider(self)]
		
class Trig_RuinwebSpider_Amulet(TrigBoard):
	def __init__(self, entity):
		self.blank_init(entity, ["TurnStarts", "AmuletAppears"])
		self.counter = 10
		
	def canTrigger(self, signal, ID, subject, target, number, comment, choice=0):
		if signal == "TurnStarts": return self.entity.onBoard and ID == self.entity.ID
		else: return self.entity.onBoard and subject != self.entity and subject.ID == self.entity.ID == self.entity.Game.turn #TurnStarts and AmuletAppears both send the correct ID
		
	def effect(self, signal, ID, subject, target, number, comment, choice=0):
		if signal == "TurnStarts": PRINT(self.entity.Game, "At the start of turn, Ruinweb Spider's countdown -1")
		else: PRINT(self.entity.Game, "When another Amulet enters player's board during player's turn, Ruinweb Spider's countdown -1")
		self.counter -= 1
		if self.counter < 1:
			PRINT(self.entity.Game, "Sacred Plea's countdown is 0 and destroys itself")
			self.entity.dead = True
			
class SummonaRuinwebSpider(Deathrattle_Minion):
	def effect(self, signal, ID, subject, target, number, comment, choice=0):
		PRINT(self.entity.Game, "Deathrattle: Summon a Ruinweb Spider triggers.")
		self.entity.Game.summon(RuinwebSpider(self.entity.Game, self.entity.ID), self.entity.position+1, self.entity.ID)
		
		
class RuinwebSpider(CrystallizeMinion):
	Class, race, name = "Bloodcraft", "", "Ruinweb Spider"
	mana, attack, health = 10, 5, 10
	index = "SV_Basic~Bloodcraft~Minion~10~5~10~None~Ruinweb Spider~Crystallize"
	requireTarget, keyWord, description = False, "", "Crystallize 2; Countdown 10 During you turn, whenever an Amulet enters your board, reduce this Amulets countdown by 1. Last Words: Summon a Ruinweb Spider"
	crystallize, crystallizeAmulet = 2, RuinwebSpider_Amulet
	attackAdd, healthAdd = 2, 2
	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.trigsBoard = [Trig_RuinwebSpider(self)]
		self.appearResponse = [self.enemyMinionsCantAttackThisTurn]
		
	def effectCanTrigger(self):
		self.effectViable = self.willCrystallize()
		
	def enemyMinionsCantAttackThisTurn(self):
		PRINT(self.Game, "Ruinweb Spider appears and enemy minions can't attack until the end of opponent's turn")
		for minion in self.Game.minionsonBoard(3-self.ID):
			minion.marks["Can't Attack"] += 1
			trig = Trig_CantAttack4aTurn(minion)
			trig.connect()
			minion.trigsBoard.append(trig)
			
class Trig_RuinwebSpider(TrigBoard):
	def __init__(self, entity):
		self.blank_init(entity, ["MinionBeenPlayed"])
		
	def canTrigger(self, signal, ID, subject, target, number, comment, choice=0):
		return self.entity.onBoard and subject.ID != self.entity.ID
		
	def effect(self, signal, ID, subject, target, number, comment, choice=0):
		PRINT(self.entity.Game, "After opponent plays minion %s, Ruinweb Spider prevents it from attacking until the end of opponent's turn"%subject.name)
		trig = Trig_CantAttack4aTurn(subject)
		trig.connect()
		subject.trigsBoard.append(trig)
		
class Trig_CantAttack4aTurn(TrigBoard):
	def __init__(self, entity):
		self.blank_init(entity, ["TurnEnds"])
		self.temp = True
		
	def canTrigger(self, signal, ID, subject, target, number, comment, choice=0):
		return self.entity.onBoard and ID == self.entity.ID
		
	def effect(self, signal, ID, subject, target, number, comment, choice=0):
		PRINT(self.entity.Game, "At the end of turn, minion %s can attack again."%self.entity.name)
		self.entity.marks["Can't Attack"] -= 1
		self.disconnect()
		try: self.entity.trigsBoard.remove(self)
		except: pass
		
		
class XIErntzJustice(ShadowverseMinion):
	Class, race, name = "Bloodcraft", "Dragon", "XI. Erntz, Justice"
	mana, attack, health = 10, 11, 8
	index = "SV_Basic~Bloodcraft~Minion~10~11~8~Dragon~XI. Erntz, Justice~Ward"
	requireTarget, keyWord, description = False, "Taunt", ""
	attackAdd, healthAdd = 2, 2
	def __init__(self, Game, ID):
		self.blank_init(Game, ID)
		self.appearResponse = [self.draw3Cards]
		self.disappearResponse = [self.restore8HealthtoPlayer]
		
	def draw3Cards(self):
		PRINT(self.Game, "XI. Erntz, Justice appears and lets player draw 3 cards")
		for num in range(3):
			self.Game.Hand_Deck.drawCard(self.ID)
			
	def restore8HealthtoPlayer(self):
		heal = 8 * (2 ** self.countHealDouble())
		PRINT(self.Game, "XI. Erntz, Justice leaves board and restores %d health to player"%heal)
		self.restoresHealth(self.Game.heroes[self.ID], heal)
		
		
		
SV_Basic_Indices = {"SV_Basic~Runecraft~4~3~3~Minion~None~Vesper, Witchhunter~Accelerate~Fanfare": VesperWitchhunter,
					"SV_Basic~Runecraft~Spell~2~Vesper, Witchhunter~Uncollectible": VesperWitchhunter_Accelerate,
					"SV_Basic~Havencraft~1~Amulet~None~Sacred Plea~Last Words": SacredPlea,
					"SV_Basic~Bloodcraft~Minion~10~5~10~None~Ruinweb Spider~Crystallize": RuinwebSpider,
					"SV_Basic~Bloodcraft~2~Amulet~None~Ruinweb Spider~Last Words": RuinwebSpider_Amulet,
					"SV_Basic~Bloodcraft~Minion~10~11~8~Dragon~XI. Erntz, Justice~Ward": XIErntzJustice,
					"SV_Basic~Forestcraft~Spell~1~Airbound Barrage": AirboundBarrage,
					}