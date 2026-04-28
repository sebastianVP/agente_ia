from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

print("Mi primer agente de IA")

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

messages = [
    {"role":"system","content":"Eres un asistente util que habla español y eres muy conciso con tus respuestas"}
]



# DEFINICION DE HERRAMIENTAS
def list_files_in_dir(directory="."):
    print("  ⚙️ Herramienta llamada: list_files_in_dir")
    try:
        files =os.listdir(directory)
        return {"files": files}
    except Exception as e:
        return {"error":str(e)}

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files_in_dir",
            "description": "Lista los archivos que existen en un directorio dado(por defector es el directorio actual)",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directorio para listar(opcional). Por defecto es el directorio actual"
                    }
                }
            }
        }
    }
]
"""
tools = [
    {
        "type":"function",
        "name":"list_files_in_dir",
        "description":"Lista los archivos que existen en un directorio dado(por defector es el directorio actual)",
        "parameters":{
            "type":"object",
            "properties":{
                "directory":{
                    "type":"string",
                    "desription":"Directorio para listar(opcional). Por defecto es el directorio actual"
                }
            },
            "required":[]
        }
    },

]
"""
while True:
    user_input = input("Magic: ").strip()

    #validaciones
    if not user_input:
        continue

    if user_input.lower() in ("salir","exit","bye","adios"):
        print("Cuidate Magic nos vemos pronto :)!")
        break
    
    # Agregar nuestro mensaje al historial
    messages.append({"role":"user","content":user_input})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages= messages,
        tools = tools
          #[
          #  {"role":"user","content":user_input}
          #  {"role":"user","content":"Dime el nombre de 5 personajes del señor de los anillos(Solo el nombre nada mas)"}
          #]
    )
    #assistant_replay = response.choices[0].message.content

    #messages.append({"role":"assistant","content":assistant_replay})

    #print(f"Asistente:{assistant_replay}")

    message = response.choices[0].message
    print(message)
    # TOOL CALL
    if message.tool_calls:
        for tool_call in message.tool_calls:
            fn_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            print(f"⚙️ El modelo quiere usar: {fn_name}")

            if fn_name == "list_files_in_dir":
                result = list_files_in_dir(**args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    # RESPUESTA NORMAL
    elif message.content:
        print(f"Asistente: {message.content}")

        messages.append({
            "role": "assistant",
            "content": message.content
        })