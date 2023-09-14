# These are just global variables.
# EventType represents the three options as numbers.
# db is for convenience.
from GameDatabase import GameDatabase
from enum import Enum
class EventType(Enum):
	FIGHT = 1
	TALK = 2
	GET = 3

db = GameDatabase()