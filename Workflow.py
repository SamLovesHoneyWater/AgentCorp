from utils import *
from Session import Session
from Roundtable import Roundtable

class Workflow(object):
	def __init__(self, participants):
		# Type Check
		if type(participants) != type([0]):
			raise TypeError("Workflow class init expects type list, got type", type(participants))
		if type(participants[0]) != type(Session("dummy")):
			raise TypeError("Workflow class init expects a list of Session() objects, got a list starting with type", type(participants))
		self.participants = participants
		self.roster = [agent.name for agent in self.participants]

	def individualWork(self):
		results = []
		for agent in self.participants:
			task = agent.ask("What is the task that you have to do according to the meeting? If you do not have anything to do, say [NONE].")
			if "[NONE]" in task:
				results.append(None)
				continue
			response = agent.ask("Now, implement your solution to the task:\n")
			results.append(response)
		for listener in self.participants:
			for i, response in enumerate(results):
				if response is None:
					continue
				contributor = self.participants[i].name
				listener.tell(f"{name} gave the following implementation for his task:\n {response}")

	def workLoop(self):
		raise Exception
