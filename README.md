# PCBuildr 🦝

**The Intelligent PC Building Assistant** - Build, compare, and maintain desktop computers with AI-powered guidance.

PCBuildr is your expert assistant for PC building, offering:
- 🤖 **Offline-First AI** - Works immediately without any setup (powered by intelligent logic, not local LLMs)
- 🔧 **Component Compatibility** - Automatically checks if your components work together
- 💡 **Smart Recommendations** - Get PC build suggestions based on budget and use case
- 📊 **Performance Analysis** - Detect bottlenecks and optimize your build
- 🛒 **Price Comparison** - Find components across multiple stores
- 🌐 **Bilingual** - English & Spanish support

## Features

### ✨ Bytecoon AI Assistant
- Intelligent recommendations without API keys or local models
- Ask questions about hardware, compatibility, performance
- Get explanations of technical specs
- Compare components intelligently
- Optional: Enhance with OpenAI, OpenRouter, or Groq API keys

### 🔍 Compatibility Checker
- CPU socket matching
- RAM type compatibility
- PSU wattage validation
- Physical fit checks (GPU length, cooler height)
- Bottleneck detection

### 💰 Component Database
- Real-time price scraping from:
  - Extreme Tech (extremetechcr.com)
  - Intelec (intelec.co.cr)
  - Facebook Marketplace
- Component categorization and filtering

### 📱 User Management
- Multi-user login system
- Per-user build history
- Save and manage multiple PC configurations
- Export builds as JSON

## Installation

### Quick Start

#### Windows (Automatic):
```bash
# Clone the repository
git clone https://github.com/yourusername/pcbuildr.git
cd pcbuildr

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run everything (backend + frontend) with one command
run_pcbuildr.bat
```

#### Windows (Manual - 2 Terminal Windows):
**Terminal 1 - Backend:**
```bash
cd pcbuildr
.venv\Scripts\activate
cd Backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd pcbuildr
.venv\Scripts\activate
cd Frontend
python app.py
```

#### macOS/Linux:
**Terminal 1 - Backend:**
```bash
git clone https://github.com/yourusername/pcbuildr.git
cd pcbuildr
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
cd Backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd pcbuildr
source .venv/bin/activate
cd Frontend
python app.py
```

### Demo Credentials
- **Username:** DemoUsr
- **Password:** 2025

### ⚠️ Important
The backend **must** be running before you start the frontend. If you see login errors, check:
1. Backend is running on `http://127.0.0.1:8000`
2. No other process is using port 8000
3. Both are using the same Python environment

Start building immediately - no LLM installation needed!

## Configuration

### Environment Variables
Copy `.env.template` to `.env` and customize (optional):

```bash
cp .env.template .env
```

Edit `.env` to:
- Change UI language and theme
- Enable optional AI providers

### Optional: Enhanced AI with API Keys

To unlock advanced AI responses, set any of these environment variables:

**OpenAI:**
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

**OpenRouter (unlimited models):**
```bash
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-...
```

**Groq (fast inference):**
```bash
AI_PROVIDER=groq
GROQ_API_KEY=gsk-...
```

**Note:** Without API keys, PCBuildr uses intelligent offline mode - fully functional!

## Architecture

PCBuildr is built with a clean, modular architecture:

- **Frontend/** - PyQt5 GUI application
- **Backend/** - FastAPI REST API for compatibility checking and user management
- **core/** - Intelligent AI modules (recommender, compatibility checker, explainer, scorer)
- **ai/** - Provider abstraction (offline, OpenAI, OpenRouter, Groq)
- **data/** - Reference databases (JSON)

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed explanation.

## Usage

### Building a PC
1. **Chat with Bytecoon** - Ask for recommendations based on your budget and use case
2. **Select Components** - Choose CPU, GPU, RAM, PSU, case, and cooling
3. **Check Compatibility** - App automatically validates your build
4. **Save Build** - Store multiple builds in your profile
5. **Export** - Save as JSON for sharing

### Building from Scratch
1. Describe your use case: Gaming, Workstation, Office, Streaming
2. Set your budget in USD
3. Bytecoon suggests starter builds
4. Fine-tune components using the selector
5. App validates and suggests alternatives

## FAQ

**Q: Do I need to install a local AI model like Ollama or LM Studio?**
A: No! PCBuildr works fully offline with intelligent built-in logic. Optional: Add an API key for cloud AI.

**Q: Can I use it without the backend?**
A: The frontend works offline for component selection and chat. Backend (optional) adds cloud price scraping.

**Q: How accurate are the compatibility checks?**
A: Very! We check socket compatibility, RAM types, power budgets, and physical fit.

**Q: Can I export my builds?**
A: Yes! Builds export to JSON format for sharing or backup.

## Development

### Project Structure
```
pcbuildr/
├── Frontend/          # PyQt5 GUI
├── Backend/          # FastAPI server
├── core/             # AI logic modules
├── ai/               # Provider abstraction
├── data/             # Reference data (JSON)
├── config.py         # Configuration management
├── requirements.txt  # Dependencies
└── .env.template     # Environment template
```

### Contributing
See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Running Tests
```bash
pytest tests/
```

## Performance

- **Startup:** < 2 seconds (no LLM loading)
- **Compatibility Check:** < 100ms
- **Offline Mode:** Works in airplane mode
- **Memory Usage:** ~150MB (UI + logic)
- **RAM Usage:** Minimal (no model inference)

## Known Limitations

- Facebook Marketplace scraping requires manual data entry (anti-scraping protections)
- Some component specs are estimated from naming patterns
- Bottleneck detection uses simplified heuristics (good for quick checks)

## Roadmap

- [ ] Component price history and trends
- [ ] Integration with PC part picker databases
- [ ] Advanced thermal simulations
- [ ] Power consumption estimates
- [ ] Build quality scoring with ML models
- [ ] Component availability alerts
- [ ] Build sharing community

## License

MIT License - See [LICENSE](./LICENSE) for details.

## Support

Having issues? Check [GitHub Issues](https://github.com/yourusername/pcbuildr/issues) or create a new one!

---

**Built with ❤️ by the PCBuildr team**

*PCBuildr makes PC building accessible, intelligent, and fun.* 🦝
