from Entity import Entity

class Item(Entity):
	def __init__(self, name="", description=""):
		super().__init__(name)
		self.desc = description		

	def getDescription():
		return self.description
