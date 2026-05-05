from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from agent import Agent

load_dotenv()

print("Mi primer agente de IA")

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)
agent= Agent()

messages = [
    {"role":"system","content":"Eres un asistente util que habla español y eres muy conciso con tus respuestas"}
]




while True:
    user_input = input("Magic: ").strip()

    #validaciones
    if not user_input:
        continue

    if user_input.lower() in ("salir","exit","bye","adios"):
        print("Cuidate Magic nos vemos pronto :)!")
        break
    
    # Agregar nuestro mensaje al historial
    agent.messages.append({"role":"user","content":user_input})
    while True:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages= agent.messages,
            tools = agent.tools
            #[
            #  {"role":"user","content":user_input}
            #  {"role":"user","content":"Dime el nombre de 5 personajes del señor de los anillos(Solo el nombre nada mas)"}
            #]
        )
    #assistant_replay = response.choices[0].message.content

    #messages.append({"role":"assistant","content":assistant_replay})

    #print(f"Asistente:{assistant_replay}")
        
        message = response.choices[0].message
        called_tool =agent.process_response(message)
        if not called_tool:
            break
        