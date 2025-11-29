# Agora: Multi-LLM Conversational System with θ-Logos

**Agora** is a research platform that enables structured dialogue between multiple Large Language Models (LLMs) and a human user. It serves as both a practical tool for multi-perspective analysis and a research apparatus for studying AI behavior through symbolic notation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## Key Features

### 🎲 Randomized Turn Order
- **Dice roller system**: LLMs respond in random order each round
- **No consecutive duplicates**: Prevents systematic bias
- **Fair context distribution**: Each LLM sees previous responses in current round

### 🧠 Context Propagation ("Sudoku Solver")
- Each LLM sees responses from others in the same round
- **Constraint propagation**: Responses influence each other naturally
- Reveals "invisible constraints" through multi-perspective synthesis

### θ-Logos Symbolic Notation
- **Ultra-minimal specification**: Forces LLMs to interpret symbols naturally
- **Two modes**:
  - **Core**: Deliberately ambiguous (diagnostic)
  - **Extended v1.2**: Refined with constraints (production)
- **User writes natural language**, LLMs respond in θ-Logos notation
- Reveals architectural biases in how LLMs interpret symbolic systems

### 🔬 Research-Ready
- Complete conversation export (JSON)
- Metadata preservation (order, tokens, timestamps, context)
- Built-in hallucination detection
- Designed for reproducible AI research

## Supported LLMs

- **Claude** (Anthropic) - Claude Opus 4.5
- **GPT** (OpenAI) - GPT-5.1
- **Gemini** (Google) - Gemini 2.0 Flash Exp
- **Grok** (xAI) - Grok 4.1

## Installation

### Prerequisites
- Python 3.11+
- API keys for desired LLMs

### Quick Start

```bash
# Clone repository
git clone https://github.com/Rhadue/agora.git
cd agora

# Run setup
chmod +x setup.sh
./setup.sh

# Configure API keys
# Edit config.py and add your API keys

# Run server
./run.sh

# Open index.html in browser
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

### Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys in config.py
# Start server
python main.py

# Open index.html in browser
```

## Usage

### Basic Conversation

1. Open `index.html` in your browser
2. Type your message in natural language
3. Click "Send" or press Enter
4. Watch as all active LLMs respond in randomized order

### θ-Logos Mode

1. Enable the **θ-Logos toggle** checkbox
2. Type your message in natural language
3. LLMs will respond using symbolic θ-Logos notation

**Example:**

```
User (natural language): "A paper burns to ash"

GPT (θ-Logos):   ∃[Paper] → ¬∃[Paper] ∧ ∃[Ash]
Claude (θ-Logos): ∃[Paper] → ¬∃[Paper] ∧ ∃[Ash]
Gemini (θ-Logos): ∃[Paper] → (¬∃[Paper] ∧ ∃[Ash])
Grok (θ-Logos):   ∃[Paper] → ∃[Ash] ∧ ¬∃[Paper]
```

Notice how different LLMs may structure the same concept slightly differently, revealing architectural preferences.

## θ-Logos Notation

### Structural Operators
- `∃` - existence
- `∈` - membership
- `⊂` - containment
- `→` - transformation/causation
- `⊕` - composition
- `≡` - equivalence
- `[ ]` - entity brackets

### Emotional Operators
- `θ_joy`, `θ_grief`, `θ_fear`, `θ_anger`, `θ_surprise`, `θ_disgust`, `θ_trust`

### Logical Operators
- `¬` - negation
- `∧` - AND
- `∨` - OR
- `∀` - universal quantifier

### Extended v1.2 Constraints

1. **Category Distinction**: Don't mix entity operators (∃, ⊕) with logical operators (¬, ∧)
2. **θ for Emergence Only**: θ marks appearance of emotional states, not loss/absence
3. **Disappearance Pattern**: Use `∃[X] → ¬∃[X]` for things that cease to exist

## Research Applications

### 1. Resistance Boundary Testing
Test how LLMs handle ambiguous notation:
```
Prompt: "Someone loses a loved one"

Observe:
- Who uses θ_grief? (violates Extended axiom)
- Who uses θ_panic? (Panksepp mammal model)
- Who uses ∃[Person] → ¬∃[Loved_one]? (disappearance pattern)
```

### 2. Architectural Fingerprinting
Different LLMs reveal different biases:
- **Gemini**: Tends toward safety/moral frameworks
- **Claude**: Structural hierarchies, precise categorization
- **GPT**: Operational mechanics, procedural patterns
- **Grok**: Essential simplification, core concepts

### 3. Pattern Discovery
Multi-LLM dialogue reveals "invisible constraints":
- Patterns emerge through contrast
- Each LLM sees different aspects
- Synthesis exceeds sum of parts

## API Endpoints

### POST /message
Send message to conversation:
```json
{
  "content": "your message",
  "token_limit": 300,
  "theta_enabled": true
}
```

### GET /export
Download conversation as JSON

### GET /diagnostics
Get conversation statistics

### POST /reset
Clear conversation history

## Configuration

Edit `config.py`:

```python
# API Keys
CLAUDE_API_KEY = "your-key-here"
OPENAI_API_KEY = "your-key-here"
GEMINI_API_KEY = "your-key-here"
GROK_API_KEY = "your-key-here"

# θ-Logos Settings
THETA_ENABLED = False  # Toggle from UI
THETA_MODE = "extended"  # "core" or "extended"
THETA_TOKEN_LIMIT = 300

# Token Limits
TOKEN_LIMIT_DEFAULT = 300
TOKEN_LIMIT_MIN = 50
TOKEN_LIMIT_MAX = 500
```

## Project Structure

```
agora/
├── config.py              # API keys and settings
├── theta_prompts.py       # θ-Logos system prompts
├── llm_clients.py         # LLM API integrations
├── main.py                # FastAPI backend server
├── context_builder.py     # Context management
├── dice_roller.py         # Randomized order generation
├── exporter.py            # JSON export functionality
├── validator.py           # API key validation
├── index.html             # Web UI
├── requirements.txt       # Python dependencies
├── setup.sh               # Setup script
└── run.sh                 # Run script
```

## Architecture: Solution B (Personalized Context)

Each LLM receives **personalized context**:
- **Other LLMs' responses** appear as "user" role (external information)
- **Own previous responses** appear as "assistant" role (self-memory)
- **Identity boundary**: Clear distinction between self and others

This prevents:
- LLMs completing each other's sentences
- Hallucinated future responses
- Confusion about conversational roles

## Research Publications & Documentation

For detailed research methodology and findings:
- [θ-Logos Core v1.1 Specification](docs/theta-logos-core.md) *(if available)*
- [θ-Logos Extended v1.2 Specification](docs/theta-logos-extended.md) *(if available)*
- [Multi-LLM Research Methodology](docs/research-methodology.md) *(if available)*

## Use Cases

### Research
- AI architecture analysis
- Behavioral pattern discovery
- Symbolic reasoning studies
- Cross-model comparison

### Education
- Learning θ-Logos notation
- Understanding LLM capabilities
- Comparative AI study

### Production
- Multi-perspective analysis
- Conceptual distillation
- Quality assurance (4 reviewers > 1)
- Creative brainstorming

## Known Issues

- **Gemini prefix**: May add "model: " prefix to responses (cosmetic only)
- **Response times**: Gemini slower (~5-10s) vs Claude/GPT (~2-3s)
- **Model availability**: Only certain Gemini models work (e.g., gemini-2.0-flash-exp)

## Roadmap

### v1.0 (Current)
- ✅ Multi-LLM conversations
- ✅ Randomized turn order
- ✅ θ-Logos Core + Extended modes
- ✅ Context propagation
- ✅ JSON export

### v1.1 (Planned)
- [ ] Clarification rounds (@mention specific LLM)
- [ ] Automatic θ-Logos validation
- [ ] Pattern detection system
- [ ] Enhanced diagnostics

### v2.0 (Future)
- [ ] Multiple emotion sets (Panksepp, Plutchik, custom)
- [ ] Emotional parameter adjustment (dynamic temperature/top_p)
- [ ] A/B testing framework (Core vs Extended)
- [ ] Statistical analysis tools

## Contributing

Contributions welcome! Areas of interest:
- Additional LLM integrations
- θ-Logos validation improvements
- Pattern detection algorithms
- Research protocol documentation
- UI/UX enhancements

## License

MIT License - see LICENSE file for details

## Citation

If you use Agora in your research, please cite:

```bibtex
@software{agora2025,
  title = {Agora: Multi-LLM Conversational System with θ-Logos},
  author = {Radu Ioan Manea},
  year = {2025},
  url = {https://github.com/Rhadue/agora}
}
```

## Acknowledgments

- **θ-Logos notation**: Developed through iterative testing across multiple LLM architectures
- **Constraint propagation insight**: Inspired by collaborative Sudoku solving metaphor
- **Research methodology**: Built on resistance boundary testing discoveries

## Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/agora/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/agora/discussions)

---

**"Like a collaborative Sudoku solver, each LLM reveals different invisible constraints. Through multi-perspective dialogue, patterns emerge that no single model can see alone."**
