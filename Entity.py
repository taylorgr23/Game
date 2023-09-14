from Config import EventType

# This is the base class (we're using inheritance here) for:
# 	- enemies
#	- items
#	- NPCs
#
# We want to use inerhitance because each of the above may cause a
# quest to progress when interacted with by the player (associated with
# a quest). Another thing they have in common is a name (self.name)
class Entity(object):
	def __init__(self, name=""):
		self.name = name
		self.questAssociations = []

	# Associate this entity with a quest
	def addQuestAssociation(self, questAssociation):
		self.questAssociations.append(questAssociation)

	# Update the quests associated with this entity based on an eventType:
	# FIGHT/TALK/GET
	def updateQuestProgress(self, eventType):
		associationsToRemove = []
		for association in self.questAssociations:
			# Index 2 == task.type (EventType enum), e.g. FIGHT, TALK, GET
			# For each task that this entity is associated with, check if
			# either FIGHT, TALK, or GET are valid options to progress a
			# quest. If so, set the task to done and propagate a progress
			# check from Quest to QuestContent to Task to update indexes.
			if association.getTaskHash().split(" ")[2] == eventType:
				association.task.setDoneness(True)
				association.quest.progressContentWithCheck()
				if association.quest.done:
					associationsToRemove.append(association)
		
		# If a quest has been marked as done, we don't want to be able to
		# update it anymore, so remove it from the list of quests this
		# entity is associated with
		for association in associationsToRemove:
			self.questAssociations.remove(association)

	# Function that returns the name of this entity, e.g. "Bucket"
	def getName(self):
		return self.name