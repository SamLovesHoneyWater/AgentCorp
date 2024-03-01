import openai, os

sk_key = os.environ.get("OPEN_AI_KEY")
openai.api_key = sk_key

def getCompletionChatGPT(prompt):
    completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "user", "content": prompt}
              ])
    return completion.choices[0].message.content

def getCompletion(prompt, history, model):
    completion = openai.ChatCompletion.create(
          model=model,
          messages=history+[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content