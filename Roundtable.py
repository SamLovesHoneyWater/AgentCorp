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
    
    def discuss(self, order="sequential"):
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
                reply = speaker.ask("Do you think this meeting has come to a conclusion and you can continue with your work? Answer [YES] or [NO].")
                if "[YES]" not in reply:
                    doEnd = False
        return doEnd
    
    def discussTillEnd(self, timeout=3):
        doEnd = False
        i = 0
        while not doEnd and i < timeout:
            doEnd = self.discuss()
            i += 1
        print(f"Meeting ended after {i} exchange(s).")
        return i

    def individualWork(self):
        results = []
        for agent in self.participants:
            task = agent.ask("What is the task that you have to do according to the meeting? If you do not have anything to do, say [NONE].")
            if "[NONE]" in task:
                results.append(None)
                continue

            response = agent.ask("Implement your solution to the task. If you need to run a python program to observe its output, put <RUN_PYTHON> at the start of the code and <END_PYTHON> at the end of the code, and the system will run it for you and return the results. Now, complete your task:\n")
            tries = 0
            while ("<RUN_PYTHON>" in response and not "<END_PYTHON>" in response) or \
                  (not "<RUN_PYTHON>" in response and "<END_PYTHON>" in response):
                tries += 1
                if tries > 2:
                    response += "\n[SYSTEM]: The proposed code is not run because it is not formatted correctly.\n"
                    break
                response = agent.ask("To run a python program, you have to include both the <RUN_PYTHON> and the <END_PYTHON> markers, but you only included one. Try again by typing the correct implementation below:")
            if "<RUN_PYTHON>" in response and "<END_PYTHON>" in response:
                code = (response.split("<RUN_PYTHON>"))[1].split("<END_PYTHON>")[0]
                if "```" in code:
                    code = code.split("```")[1]
                code_output = self.runCode(code)
                response += "\nThe code above is run, and it gave the following output:\n" + code_output
            results.append(response)

        for listener in self.participants:
            for i, response in enumerate(results):
                contributor = self.participants[i].name
                if response is None:
                    listener.put(f"{contributor} did not think he has to make an implementation.")
                else:
                    listener.put(f"{contributor} gave the following implementation for his task:\n {response}")
    
    def broadcast(self, msg):
        for agent in self.participants:
            agent.put(msg)

    def runCode(self, code):
        permission = input(("Running code:\n\n" + code + "\n\n", "Enter '1' to grant access:\t"))
        if permission != "1":
            return None
        try:
            output = exec(code)
            return str(output)
        except Exception as e:
            return str(e)
