from GameDatabase import *
from Entity import Entity
from Player import Player
from Enemy import Enemy
from NPC import NPC
from Item import Item
from Location import *
from Quest import *
from Config import *
import os

# Display this at the top of every iteration
DASH_BANNER = "--------------------------------------------"

# Player
player = Player(maxHp=100)

# Enemies
enemies = [ Enemy(name="Sample Enemy", maxHp=50) ]

# Locations
locations = [ Location(name="Sandy Shores", description="A nice quiet beach."), \
	Location(name="Seashore Town", description="Just a little hamlet."), \
	Location(name="Exeter Plaza", description="A shopping center.") ]

#Items
item_bottle = Item(name="Bottle", description="A worn out glass bottle.")

"""Quests have a similar structure to:

- Quest 				(top level object)
	- Quest Content 	(groups tasks)
		- Task 			(jobs, which using involve FIGHT-ing/TALK-ing/GET-ting)
		- Task
	- Quest Content
		- Task
		- Task
- Quest
	...
"""

# Quests
quest1 = Quest(name="My First Quest", description="Get to know a friend.")

# QuestContent
quest1.addQuestContent(QuestContent(tasks= \
		[Task(EventType.TALK, item_bottle, locations[2], "Talk to the bottle in Exeter Plaza")]
	)
)

# Add entities to the database for easy access. GameDatabase isn't really used.
def dbSetup():
	db.player = player

	for enemy in enemies:
		db.addEnemy(enemy)

	for loc in locations:
		db.addLocation(loc)

	db.items["Bottle"] = item_bottle
	Edge(True, db.locations["Sandy Shores"], db.locations["Seashore Town"]), 
	Edge(True, db.locations["Seashore Town"], db.locations["Exeter Plaza"])

	db.startLoc = db.locations["Sandy Shores"]
	player.setLocation(db.startLoc)
	player.addQuest(quest1)

if __name__ ==  "__main__":
	# This is an hack to clear the terminal and keep it neat
	os.system('cls||clear')
	dbSetup()

	"""MAIN LOOP"""
	userInput = ""
	while userInput != "quit":
		print(DASH_BANNER + "\n" + str(player.location))

		# Remove completed quests from the player's log
		# Display completed message
		player.checkQuestStatus()

		# Prompt for input, split the input, and put it into a list
		userInput = input("Please enter an action:" + \
			"\n - move <destination>\n - talk <target>\n - quests\n - quit\n> ").lower()
		userInputTokens = userInput.split(" ") 
		numTokens = len(userInputTokens)

		print("") # add a newline

		# Do nothing if the user inputted nothing
		if numTokens > 0:
			# userInputTokens[0] indicates the first word entered
			if userInputTokens[0] == "quests":
				player.printQuests()
				input("Press enter when you're finished looking.")

			# At least two words must be entered to use these commands
			if numTokens > 1:
				# Enter a different area of the map
				if userInputTokens[0] == "move":
					player.move(userInputTokens[1])

				# Speak to an entity -- dialogue not yet implemented
				if userInputTokens[0] == "talk":
					entityName = userInputTokens[1].title()
					entity = player.location.getEntityFromLocationContents(entityName)
					entity.updateQuestProgress(str(EventType.TALK))

		# Clear the console
		os.system('cls||clear')