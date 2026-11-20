import anthropic
from dotenv import load_dotenv

load_dotenv()
from llm import client, MODEL, text_of  # provider chosen by LLM_PROVIDER

def agent_turn(system_prompt: str, conversation_history: list) -> str:
    res = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=system_prompt,
        messages=conversation_history
    )
    return text_of(res)

def run_peer_to_peer(topic: str, max_rounds: int = 3):
    print(f"[P2P Collaboration Started] Topic: {topic}\n")
    
    draft_history = [{"role": "user", "content": f"Write an initial short architecture draft for: {topic}"}]
    critique_history = []
    
    current_draft = agent_turn("You are a Solutions Architect. Write concise architectural drafts.", draft_history)
    print(f"--- Round 1 Draft ---\n{current_draft}\n")
    
    for round_num in range(2, max_rounds + 1):
        # Peer 2 (Critic) reviews Draft
        critique_history = [{"role": "user", "content": f"Critique this architectural draft and suggest 2 improvements:\n{current_draft}"}]
        critique = agent_turn("You are a Critical Reviewer. Be strict and constructive.", critique_history)
        print(f"--- Round {round_num} Critique ---\n{critique}\n")
        
        # Peer 1 (Author) refines based on Critique
        draft_history.append({"role": "assistant", "content": current_draft})
        draft_history.append({"role": "user", "content": f"Incorporate this critique and provide the refined draft:\n{critique}"})
        current_draft = agent_turn("You are a Solutions Architect. Refine your design based on feedback.", draft_history)
        print(f"--- Round {round_num} Refined Draft ---\n{current_draft}\n")

if __name__ == "__main__":
    run_peer_to_peer("A real-time notification microservice using Redis pub/sub.")
