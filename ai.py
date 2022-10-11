import openai
import sys
from record import record_audio
import whisper
import re
import pyttsx3



def chat_bot():
    openai.api_key = "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"

    
    question = ""

    for line in sys.stdin:
        if 'q' == line.rstrip():
            break
        question=line
        conversation_string+=f"{question}"

        response = openai.Completion.create(engine="curie",
        prompt=conversation_string,
        temperature=0.85,
        max_tokens=128,
        frequency_penalty=0.0,
        presence_penalty=0.0)

        answer = response['choices'][0]['text']
        x = re.search(r"(.*): (.*)", answer)
        if(x is None):
            print("--------------------------")
            print(conversation_string)
            print("----------------------")
            print(answer)
            print("Got no response from OpenAI :( rip")
        else:
            answer = f"{x.group(2)}"
            print(f"{x.group(1)}: {answer}")
            conversation_string+=f"{person2}: {answer}\n{person1}: "


def chat_bot_audio(person1, person2, conversation_string):
    openai.api_key = "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"
    model = whisper.load_model("small.en")

    question = ""
    engine = pyttsx3.init()

    while True:
        question=record_audio(model)
        print(question)
        conversation_string+=f"{question}\n"

        response = openai.Completion.create(engine="curie",
        prompt=conversation_string,
        temperature=0.9,
        max_tokens=128,
        frequency_penalty=0.0,
        presence_penalty=0.0)

        answer = response['choices'][0]['text']
        x = re.search(r".*: (.*)", answer)
        if(x is None):
            print(response['choices'][0]['text'])
            print("Got no response from OpenAI :( rip")
        else:
            answer = x.group(1)
            print(answer)
            engine.say(answer)
            engine.runAndWait()
            conversation_string+=f"{person2}: {answer}\n{person1}: "
        #print("------------------")
        #print(conversation_string)
        #print("------------------------")
        
person1 = "Person"
person2 = "John Cena"
conversation_string = f"{person1}: Hello, who are you?\n{person2}: Hello, this is John Cena. I am an American professional wrestler, actor, and former rapper. I am widely regarded as one of the greatest professional wrestlers of all time!\n{person1}: "

chat_bot_audio(person1, person2, conversation_string)