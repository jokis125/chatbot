import openai
import sys
from record import record_audio
import whisper
import re
import pyttsx3
import os
from datetime import datetime


def chat_bot(person1, person2, conversation_string):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    question = ""

    for line in sys.stdin:
        if 'q' == line.rstrip():
            break
        question=line
        conversation_string+=f"{question}{person2}:"

        response = openai.Completion.create(engine="curie",
        prompt=conversation_string,
        temperature=0.85,
        max_tokens=128,
        frequency_penalty=0.1,
        presence_penalty=0.3)

        answer = response['choices'][0]['text']
        x = re.search(r"(.*)\n.*:.*", answer)
        #print("--------DEBUG--------")
        #print(answer)
        if(x is None):
            print(response['choices'][0]['text'])
            print("Got no response from OpenAI :( rip")
        else:
            answer = f"{x.group(1)}"
            answer_string = f"{person2}:{answer}"
            print(answer_string)
            conversation_string+=f"{answer}\n{person1}: "

    now = datetime.now()
    text_file = open(f"conv{now.strftime('%H %M')}.txt", "w")
    n = text_file.write(conversation_string)
    text_file.close()


def chat_bot_audio(person1, person2, conversation_string):
    os.system('cls')
    openai.api_key = os.getenv('OPENAI_API_KEY')
    model = whisper.load_model("small.en")

    question = ""
    engine = pyttsx3.init()

    while True:
        question=record_audio(model)
        print(f"{person1}: {question}")
        conversation_string+=f"{question}\n"

        response = openai.Completion.create(engine="curie",
        prompt=conversation_string,
        temperature=0.8,
        max_tokens=128,
        frequency_penalty=0.4,
        presence_penalty=0.4)

        answer = response['choices'][0]['text']
        x = re.search(r" (.*)\n.*:.*", answer)
        #print("--------DEBUG--------")
        #print(answer)
        if(x is None):
            print(response['choices'][0]['text'])
            print("Got no response from OpenAI :( rip")
        else:
            answer = f"{x.group(1)}"
            answer_string = f"{person2}: {answer}"
            print(answer_string)
            engine.say(answer)
            engine.runAndWait()
            conversation_string+=f"{answer_string}\n{person1}: "
        
person1 = "Person"
person2 = "Angry Bot"
rudebot_string = f"""{person1}: Hello, who are you?
{person2}: I am a very angry chatbot created with LLM
{person1}: Oh...
{person2}: Shut up, I hate everyone!
{person1}: """


chat_bot(person1, person2, rudebot_string)
