from Quest import QuestAssociation
from Player import Player
import Config

# A "connection" between two Locations. The reason I made is to 
# make it possible to lock the door between locations, for quest
# purposes, maybe.
class Edge(object):
	def __init__(self, isOpen, locationA, locationB):
		locationA.addEdge(self)
		locationB.addEdge(self)
		self.isOpen = isOpen
		self.A = locationA
		self.B = locationB

	def setIsOpen(isOpen):
		self.isOpen = isOpen

# The regions of the map, which store their neighbors using self.edges.
# They also can be associated with a Quest.
class Location(object):
	def __init__(self, name="", description=""):
		self.name = name
		self.desc = description
		self.contents = dict()
		self.edges = []
		self.questAssociations = []

	# We can print locations out using print(location) when __str__ is defined.
	def __str__(self):
		return self.name + " | " + self.desc + "\n" + self.getContentsAsString() + "\n" + self.getEdgesAsString() + "\n"

	def addEdge(self, edge):
		self.edges.append(edge)

	def addQuestAssociation(self, questAssociation):
		self.questAssociations.append(questAssociation)

	# The following is based on the player's current quest list.
	# The function spawns Entities into the Location by checking all of the
	# tasks this Location is associated with, as well as what subject/entity is involved
	# in those tasks. For example, if a task involved FIGHT-ing a Blob, then the Blob
	# entity would be spawned into this location.
	def loadQuestContent(self, player):
		quests = player.getQuests()
		associationsToLoad = []
		for i in range(len(self.questAssociations)):
			if self.questAssociations[i].quest in quests:
				associationsToLoad.append(self.questAssociations[i])

		for association in associationsToLoad:
			questName, contentId, taskType, taskSubject = association.getTaskHash().split(" ")
			entity = None

			# Check the database for the subject's name and get the actual Entity object.
			if taskSubject in Config.db.items:
				entity = Config.db.items[taskSubject]
			elif taskSubject in Config.db.enemies:
				entity = Config.db.items[taskSubject]
			elif taskSubject in Config.db.npcs:
				entity = Config.db.items[taskSubject]
			if not entity is None:
				# Put the entity into this location's contents.
				self.contents[entity.name] = entity

	def getEntityFromLocationContents(self, entityName):
		if not entityName in self.contents:
			return None
		return self.contents[entityName]

	def getContentsAsString(self):
		contentsStr = ""
		for entity in self.contents:
			contentsStr += entity + ", "
		return "Contents: " + contentsStr.strip(", ")

	def printContents(self):
		print(self.getContentsAsString())

	def getEdgesAsString(self):
		edgesStr = ""
		for edge in self.edges:
			edgesStr += edge.A.name + " <-> " + edge.B.name + ", "
		return "Edges: " + edgesStr.strip(", ")