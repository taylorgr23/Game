from Config import EventType

# The "jobs" that the player must perform to progress a Quest.
# Consists of a "type" (FIGHT/TALK/GET), has an Entity which
# acts as the subject that must be interacted with, has a 
# location where the task must be completed in, and has a 
# description.

# Also, each task is owned by a QuestContent object, which 
# helps categorize these tasks within a Quest.
class Task(object):
	def __init__(self, type, subject, location, description):
		self.questContent = None
		self.type = type
		self.subject = subject
		self.location = location
		self.desc = description
		self.done = False

	# Set what QuestContent object this task belongs to
	def setOwner(self, owner):
		self.questContent = owner

	# Associate the "subject" Entity with this task's Quest.
	# Also associate the location with the Quest, as well. 
	def initializeAssociations(self):
		self.subject.addQuestAssociation(QuestAssociation(self))
		self.location.addQuestAssociation(QuestAssociation(self))

	def setDoneness(self, isDone):
		self.done = isDone

	def isDone(self):
		return self.done

# Quest Content:
# The units with which we categorize Tasks within Quests.
# The reason we have these is that there may be multiple
# tasks within a Quest that have similar completion conditions
# and there may be a situation where we need to ensure that
# they do not conflict. We do this by combining QuestContent's
# ID with the type of its tasks and the names of their subject 
# entities to create unique strings. We may use these strings
# later to fetch dialogue that's unique to given tasks.
class QuestContent(object):
	def __init__(self, tasks=None):
		self.quest = None
		self.id = -1
		# Conditions are just tasks; aka, the conditions needed
		# to progress this batch of QuestContent
		self.conditions = [] 
		self.conditionsIndex = -1
		self.done = False

		# Can initialize QuestContent directly with a list of tasks
		# or using setTasks.
		if tasks is not None:
			self.setTasks(tasks)

	def progressTasksWithCheck(self):
		# If the current task in this QuestContent batch is not complete,
		# do not progress to the next task. Also, do not progress if the
		# entire batch of tasks is complete.
		if not self.conditions[self.conditionsIndex].isDone() or self.done:
			return False
		
		# Otherwise, progress to the next task. If all tasks are done, set
		# this QuestContent's state to done.
		self.conditionsIndex += 1
		if self.conditionsIndex == len(self.conditions):
			self.setDoneness(True)
		
		return True

	def getCurrentTask(self):
		return self.conditions[self.conditionsIndex]

	# We let the tasks know what QuestContent object they belong to
	# and associate each of their subjects and locations with the 
	# Quest.
	def initializeTaskAssociations(self):
		for task in self.conditions:
			task.setOwner(self)
			task.initializeAssociations()

	def setTasks(self, tasks):
		self.conditionsIndex = 0
		self.conditions = tasks
		for task in self.conditions:
			task.setOwner(self)

	def setOwner(self, owner):
		self.quest = owner

	def setId(self, newId):
		self.id = newId

	def setDoneness(self, isDone):
		self.done = isDone

	def isDone(self):
		for task in self.conditions:
			if task.done == False:
				return False
		return True

# What you'd generally think of as a quest. It has a name, description,
# and stores QuestContent objects in self.content to progress through.
class Quest(object):
	def __init__(self, name="", description=""):
		self.name = name
		self.desc = description
		self.content = []
		self.contentIndex = len(self.content) - 1
		self.done = False

	# Add a batch of tasks via a QuestContent object and initialize them.
	def addQuestContent(self, questContent):
		if self.contentIndex == -1:
			self.contentIndex = 0
		questContent.setOwner(self)
		questContent.setId(len(self.content))
		questContent.initializeTaskAssociations()
		self.content.append(questContent)

	def getCurrentContent(self):
		if self.contentIndex == -1:
			return None
		return self.content[self.contentIndex]

	# We use this to enable printing Quests in the UI
	def getCurrentContentAndTaskAsString(self):
		if self.contentIndex == -1:
			return ""
		return self.getCurrentContent().getCurrentTask().desc + "\n"

	def getThisQuestAsString(self):
		return " - \"" + self.name + "\" | " + self.desc + "\n\t- " + self.getCurrentContentAndTaskAsString()

	# This function looks at the current QuestContent object and checks
	# whether all tasks within it are complete. If they are, then this quest
	# is done. Otherwise, progress to the next batch of tasks. 
	def progressContentWithCheck(self):
		if self.done:
			return False
		
		self.content[self.contentIndex].progressTasksWithCheck()
		if not self.content[self.contentIndex].isDone():
			return False
		
		self.contentIndex += 1
		if self.contentIndex == len(self.content):
			self.done = True
		return True

# We use these to associate Locations and Entities with Quests.
class QuestAssociation(object):
	def __init__(self, task=None):
		self.hash = self.createTaskHash(task)
		self.task = task
		self.quest = task.questContent.quest

	# The unique identifier string, which gets split into its 4 pieces when needed.
	def createTaskHash(self, task):
		questContent = task.questContent
		quest = questContent.quest
		return "".join(quest.name.split(" ")) + " " + str(questContent.id) + " " + str(task.type) + " " + task.subject.name

	def getTaskHash(self):
		return self.hash