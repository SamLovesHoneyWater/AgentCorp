from utils import *
from Session import Session

class Roundtable(object):
    def __init__(self, participants):
        # Type Check
        if type(participants) != type([0]):
            raise TypeError("Roundtable class init expects type list, got type", type(participants))
        if type(participants[0]) != type(Session("dummy")):
            raise TypeError("Roundtable class init expects a list of Session() objects, got a list starting with type", type(participants))
        self.participants = participants
        self.roster = [agent.name for agent in self.participants]
    
    def initConvo(self, topic, starting_index):
        header = "You are in a meeting with"
        for name in self.roster:
            header += f" {name},"
        header += f" and you are talking about the following topic: {topic}"
        header += " Be concise."
        #header += "\nWhen you think the conversation is finished and everybody can start working, output [END]. Do not output [END] unless everyone has explicitly reached a consensus."
        self.broadcast(header)
    
    def roundRobin(self, order="sequential"):
        doEnd = True
        if order == "sequential":
            gsl = self.participants
        elif order == "random":
            gsl = self.participants[:]
            random.shuffle(temp)
        else:
            raise ValueError("Unexpected order keyword " + sequential)
        for speaker in gsl:  # iterate General Speaker's List
            response = speaker.ask(f"[You ({speaker.name})]: ")
            header_response = f"[{speaker.name}]:\t{response}"
            for listener in self.participants:
                if speaker == listener:
                    continue
                listener.put(header_response)
            if doEnd:
                reply = speaker.silentAsk("Do you think this meeting has come to a conclusion and everybody can go on with their own work? Answer [YES] or [NO].")
                if "[YES]" not in reply:
                    doEnd = False
        return doEnd
    
    def roundRobinTillEnd(self, timeout=5):
        doEnd = False
        i = 0
        while not doEnd and i < timeout:
            doEnd = self.roundRobin()
            i += 1
        print(f"Meeting ended after {i} exchanges.")
        return i

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
                listener.put(f"{contributor} gave the following implementation for his task:\n {response}")
    
    def broadcast(self, msg):
        for agent in self.participants:
            agent.put(msg)
