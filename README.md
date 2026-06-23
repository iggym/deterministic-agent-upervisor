# Deterministic Agent Supervisor

A robust multi-agent orchestration framework utilizing a **Rust-compiled state machine engine** combined with **Anthropic structured outputs** to eliminate non-deterministic execution drift during complex infrastructure updates.

## Architecture Highlights
1. **Immutable States (Rust):** core transitions are validated inside compiled Rust code, completely out of reach of LLM hallucinations.
2. **Structured Typings (Python):** Pydantic schemas mapped directly into Anthropic's Tool Use API force Claude to speak strictly in actionable JSON payloads matching valid execution states.

## Getting Started

### Prerequisites
* Rust toolchain (`cargo`, `rustc`)
* Python 3.10+
* Anthropic API Key

### Installation

1. Clone and navigate to the project directory:
   ```bash
   git clone [https://github.com/yourusername/deterministic-agent-supervisor.git](https://github.com/yourusername/deterministic-agent-supervisor.git)
   cd deterministic-agent-supervisor
