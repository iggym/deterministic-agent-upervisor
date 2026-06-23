import os
from anthropic import Anthropic
from pydantic import BaseModel, Field

# Pydantic schema for structured output enforcement
class AgentAction(BaseModel):
    next_state: str = Field(description="The next state to transition into. Must be Planning, Approved, Executing, Success, or Failed.")
    command: str = Field(description="The specific infrastructure bash command or action to execute.")
    rationale: str = Field(description="Justification for why this step matches the current state constraints.")

class AnthropicSupervisorAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        # Using Claude 3.5 Sonnet for deterministic task planning
        self.model = "claude-3-5-sonnet-20240620" 

    def get_next_step(self, current_state: str, context: str) -> AgentAction:
        prompt = f"""
        You are acting as an internal brain module for a deterministic state machine.
        Current System State: {current_state}
        Context/Objective: {context}

        Analyze the current state and emit the required action schema. You must follow state transition hygiene flawlessly.
        """

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system="You only speak JSON matching the tool specification provided. Do not deviate.",
            messages=[{"role": "user", "content": prompt}],
            tools=[
                {
                    "name": "emit_action",
                    "description": "Emit structured output for the deterministic state machine engine.",
                    "input_schema": AgentAction.model_json_schema()
                }
            ],
            tool_choice={"type": "tool", "name": "emit_action"}
        )
        
        # Parse the structured output
        tool_use = response.content[0] if response.content else None
        if tool_use and tool_use.type == "tool_use":
            return AgentAction(**tool_use.input)
        raise RuntimeError("Agent failed to output correct structural schema tool call.")
