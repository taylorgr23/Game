from Entity import Entity

class NPC(Entity):
	def __init__(self, name=""):
		super().__init__(name)
		self.inventory = []

	def updateInventory(entity):
		self.inventory.append(entity)

	def getInventory():
		return self.inventory
