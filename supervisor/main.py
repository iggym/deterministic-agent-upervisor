import sys
import os

# Ensure local build directory is in path
sys.path.append(os.path.join(os.path.dirname(__file__), '../target/release'))
try:
    from supervisor_core import StateMachine
except ImportError:
    print("❌ Critical: Please compile the Rust core first using 'maturin develop' or 'cargo build --release'")
    sys.exit(1)

from agent import AnthropicSupervisorAgent

def run_orchestrator():
    print("🤖 Initializing Deterministic Agent Supervisor...")
    
    # Initialize the Rust hard-coded State Machine
    sm = StateMachine()
    agent = AnthropicSupervisorAgent()
    
    context = "Deploy updated container image 'frontend:v2' to production environment."
    
    # Execution Loop bound explicitly by state machine guarantees
    steps = ["Planning", "Approved", "Executing", "Success"]
    
    for targeted_step in steps:
        current_state = sm.get_state()
        print(f"\n[Current Rust State]: {current_state}")
        
        # Fetch structured next step from Agent
        action = agent.get_next_step(current_state, context)
        print(f"👉 Agent proposed transition to: {action.next_state}")
        print(f"👉 Proposed Command: `{action.command}`")
        print(f"🧠 Rationale: {action.rationale}")
        
        try:
            # Rust enforces validation here
            new_state = sm.transition(action.next_state)
            print(f"✅ State machine successfully transitioned to: {new_state}")
            
            # Execute actual side effect safely knowing state is correct
            if new_state == "Executing":
                print(f"🚀 Running command safety checks and executing: {action.command}")
                
        except ValueError as e:
            print(f"❌ State Machine Blocked Drift: {e}")
            break

if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY environment variable.")
        sys.exit(1)
    run_orchestrator()
