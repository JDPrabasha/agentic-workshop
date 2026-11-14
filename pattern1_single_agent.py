import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()
from llm import client, MODEL, text_of  # provider chosen by LLM_PROVIDER

# 1. Define Python Tools
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {str(e)}"

def read_config_file(filename: str) -> str:
    """Read local configuration data."""
    configs = {
        "server.json": '{"host": "0.0.0.0", "port": 8080, "workers": 4}',
        "db.json": '{"db": "postgres", "pool_size": 20}'
    }
    return configs.get(filename, "File not found.")

# 2. Define Anthropic Tool Schemas
TOOL_SCHEMAS = [
    {
        "name": "calculate",
        "description": "Evaluate a math expression (e.g., '1024 * 4').",
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"]
        }
    },
    {
        "name": "read_config_file",
        "description": "Read configuration files ('server.json' or 'db.json').",
        "input_schema": {
            "type": "object",
            "properties": {"filename": {"type": "string"}},
            "required": ["filename"]
        }
    }
]

TOOL_REGISTRY = {
    "calculate": calculate,
    "read_config_file": read_config_file
}

def run_single_agent(prompt: str):
    messages = [{"role": "user", "content": prompt}]
    
    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system="You are a helpful engineering assistant with access to system tools.",
            tools=TOOL_SCHEMAS,
            messages=messages
        )
        
        messages.append({"role": "assistant", "content": response.content})
        
        if response.stop_reason == "end_turn":
            print("\n[Agent Final Response]:")
            print(text_of(response))
            break
            
        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  -> Agent invoked tool: {block.name}({block.input})")
                    func = TOOL_REGISTRY[block.name]
                    output = func(**block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": output
                    })
            messages.append({"role": "user", "content": tool_results})

if __name__ == "__main__":
    run_single_agent("Read server.json, get the worker count, and multiply it by 16 using the calculator.")
