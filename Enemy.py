from Entity import Entity

class Enemy(Entity):
	def __init__(self, name, maxHp):
		super().__init__(name)
		self.maxHp = maxHp
		self.hp = self.maxHp

	def getHp():
		return self.hp

	def reset():
		self.hp = self.maxHp 