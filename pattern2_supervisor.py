import anthropic
from dotenv import load_dotenv

load_dotenv()
from llm import client, MODEL, text_of  # provider chosen by LLM_PROVIDER

def call_worker(system_prompt: str, task: str) -> str:
    """Stateless helper for specialized worker agents."""
    res = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=system_prompt,
        messages=[{"role": "user", "content": task}]
    )
    return text_of(res)

def coder_worker(requirements: str) -> str:
    return call_worker("You are a Python Expert. Write clean code snippets.", f"Write code for: {requirements}")

def security_worker(code_snippet: str) -> str:
    return call_worker("You are a Security Auditor. Find vulnerabilities concisely.", f"Audit this code:\n{code_snippet}")

SUPERVISOR_TOOLS = [
    {
        "name": "coder_worker",
        "description": "Delegate coding tasks to the Python Expert worker.",
        "input_schema": {"type": "object", "properties": {"requirements": {"type": "string"}}, "required": ["requirements"]}
    },
    {
        "name": "security_worker",
        "description": "Delegate security auditing to the Security Auditor worker.",
        "input_schema": {"type": "object", "properties": {"code_snippet": {"type": "string"}}, "required": ["code_snippet"]}
    }
]

def run_supervisor(goal: str):
    messages = [{"role": "user", "content": goal}]
    print(f"[Supervisor Goal]: {goal}\n")
    
    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system="You are a Tech Lead Supervisor. Delegate tasks to your specialist workers and synthesize results.",
            tools=SUPERVISOR_TOOLS,
            messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})
        
        if response.stop_reason == "end_turn":
            print("\n[Supervisor Final Synthesis]:")
            print(text_of(response))
            break
            
        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  [Supervisor] Delegating to -> {block.name}({block.input})")
                    if block.name == "coder_worker":
                        out = coder_worker(**block.input)
                    else:
                        out = security_worker(**block.input)
                    print(f"    Worker Output: {out[:80]}...")
                    tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": out})
            messages.append({"role": "user", "content": tool_results})

if __name__ == "__main__":
    run_supervisor("Create a Python function that reads user input and runs SQL queries, then audit it for security.")
