from utils import *

class Session(object):
    def __init__(self, name, role="You are a helpful assistant.", model="gpt-3.5-turbo", history=[]):
        self.name = name
        self.role = role
        self.model = model
        self.history = history
        if len(history) == 0:
            self.history = [{"role": "system", "content": role}]
        elif len(history) > 0 and role != history[0]["content"]:
            raise ValueError("Cannot apply system message to chat history. This is because a chat history already\
            exists and it contains a role that is different from the role specified.")

    def put(self, prompt):
        self.history.append({"role": "user", "content": prompt})
        return None
    
    def ask(self, prompt):
        try:
            response = getCompletion(prompt, self.history, self.model)
        except:
            raise Exception
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": response})
        return response
    
    def silentAsk(self, prompt):
        try:
            response = getCompletion(prompt, self.history, self.model)
        except:
            raise Exception
        return response
    
    def freeFlow(self):
        while True:
            print("Entering free flow mode...")
            prompt = input("[User]:\t")
            response = self.tell(prompt)
            print("[Bot]:\t" + response)
