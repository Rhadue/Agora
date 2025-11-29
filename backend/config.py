# config.py - API Keys și Settings Centralizate
#claude=
#openai=
# === API KEYS ===
CLAUDE_API_KEY = "put your Claude API key here"
OPENAI_API_KEY = "put your OpenAI API key here"
GEMINI_API_KEY = "put your Gemini API key here"
GROK_API_KEY = "put your Grok API key here"

#don't forget to save it. 

# === MODEL CONFIGURATIONS ===
MODELS = {
    "claude": {
        "api_model_name": "claude-opus-4-5-20251101",
        "temperature": 0.8,
        #"top_p": 0.90,
        "timeout": 30
    },
    "gpt": {
        "api_model_name": "gpt-5.1",
        "temperature": 0.8,
        #"top_p": 0.90,
        "timeout": 30
    },
    "gemini": {
        "api_model_name": "gemini-2.0-flash-exp",
        "temperature": 0.8,
        #"top_p": 0.90,
        "timeout": 30
    },
    "grok": {
        "api_model_name": "grok-4-1-fast-reasoning",
        "temperature": 0.8,
        #"top_p": 0.90,
        "timeout": 30
    }
}

# === TOKEN LIMITS ===
TOKEN_LIMIT_DEFAULT = 300
TOKEN_LIMIT_MIN = 50
TOKEN_LIMIT_MAX = 500

# === THETA-LOGOS SETTINGS ===
THETA_ENABLED = False  # Toggle θ-Logos mode on/off (controlled from UI)
THETA_MODE = "extended"  # "core" or "extended"
THETA_TOKEN_LIMIT = 500  # Token limit when in θ-Logos mode
