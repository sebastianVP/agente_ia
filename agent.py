import os
import json

class Agent:
    def __init__(self):
        self.setup_tools()
        
        self.messages = [
            {"role":"system","content":"Eres un asistente util que habla español y eres muy conciso con tus respuestas"}
        ]
    def setup_tools(self):
        self.tools = [
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
    # DEFINICION DE HERRAMIENTAS
    def list_files_in_dir(self,directory="."):
        print("  ⚙️ Herramienta llamada: list_files_in_dir")
        try:
            files =os.listdir(directory)
            return {"files": files}
        except Exception as e:
            return {"error":str(e)}
        
    def process_response(self,message):
        # True= si llama a una funcion. False =No hubo llamado
        # message = response.choices[0].message
        print(message)

            # ✅ IMPORTANTE: guardar mensaje del asistente
        self.messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": message.tool_calls
        })
        # TOOL CALL
        if message.tool_calls and len(message.tool_calls) > 0:
            for tool_call in message.tool_calls:
                fn_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"⚙️ El modelo quiere usar: {fn_name}")
                
                if fn_name == "list_files_in_dir":
                    result = self.list_files_in_dir(**args)

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
                
            return True
        # RESPUESTA NORMAL
        elif message.content:
            print(f"Asistente: {message.content}")
            
            self.messages.append({
                "role": "assistant",
                "content": message.content
            })
           
        return False