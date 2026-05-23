# PCBuildr 🦝

> Professional Desktop PC Hardware Analysis and Builder Tool

**Build, analyze, and compare desktop computer configurations with intelligent compatibility checking.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Beta](https://img.shields.io/badge/Status-Beta-blue.svg)]()
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

PCBuildr is your desktop PC building companion, offering:
- 🔧 **Component Compatibility** - Automatically checks if your components work together
- 📊 **Build Analysis** - Analyze performance tiers, bottlenecks, and power requirements
- 💡 **Smart Recommendations** - Get PC build suggestions based on budget and use case
- 🛒 **Component Database** - Browse and select from current hardware inventory
- 🌐 **Bilingual** - English & Spanish support
- 💾 **Offline-First** - Works immediately without any API keys or internet

## Features

### 📊 Build Analysis Engine
- Real-time build analysis and performance scoring
- CPU/GPU bottleneck detection
- Power supply validation and wattage estimation
- Component tier classification (Entry-Level to Enthusiast)
- Compatibility issue detection
- Intelligent upgrade recommendations

### 🔍 Compatibility Checker
- CPU socket matching
- RAM type compatibility
- PSU wattage validation
- Physical fit checks (GPU length, cooler height)
- Bottleneck detection

### � Component Database
- Offline component inventory
- Easy component categorization and filtering
- Price reference in Costa Rican Colones (₡)
- Support for future price tracking

### 📱 User Management
- Multi-user login system
- Per-user build history and profiles
- Save and manage multiple PC configurations

## Technologies

- **Frontend:** PyQt5 (Python GUI framework)
- **Backend:** FastAPI (async Python web framework)
- **Data:** JSON-based component database
- **Language:** Python 3.8+
- **OS:** Windows, macOS, Linux

## Installation

### Quick Start - Windows

```bash
# Clone the repository
git clone https://github.com/yourusername/pcbuildr.git
cd pcbuildr

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python Frontend/app.py
```

Or use the batch file shortcut:
```bash
run_pcbuildr.bat
```

### Quick Start - macOS/Linux

```bash
git clone https://github.com/yourusername/pcbuildr.git
cd pcbuildr

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python Frontend/app.py
```

### Demo Credentials
- **Username:** DemoUsr
- **Password:** 2025

## Screenshots

PCBuildr's intuitive interface makes PC building accessible to everyone:

- **Main Interface** - Clean dashboard with PC builder and analysis tools
- **Component Selection** - Browse and select from comprehensive component database
- **Build Analysis** - Real-time compatibility checking and performance scoring
- **Recommendations** - Smart suggestions based on budget and use case

See the [screenshots/](./screenshots/) directory for examples.

## Usage

### Building a PC
1. **Log in or create an account** - Use demo credentials to test
2. **Go to PC Builder** - Select components from each category
3. **View Build Analysis** - See real-time performance scoring, compatibility issues, and recommendations
4. **Save Build** - Store your configuration for later
5. **Manage Profiles** - Switch between saved builds or create new ones

### Understanding Build Analysis
- **Performance Score (0-100)** - Composite metric of CPU and GPU capabilities
- **Build Tier** - Classification: Entry-Level, Mid-Range, High-End, Enthusiast
- **Compatibility Issues** - List of any detected problems (missing components, incompatibilities)
- **Power Estimation** - Estimated system power draw in watts
- **Bottleneck Analysis** - Identifies if CPU or GPU limits overall performance
- **Recommendations** - Suggestions for component upgrades or changes

## Configuration

PCBuildr works out of the box without configuration. For advanced customization:

### Environment Variables (Optional)
```bash
# Default language
PCBUILDR_LANGUAGE=es

# Default theme
PCBUILDR_THEME=dark

# Debug mode
DEBUG=false
```

The application stores user data in:
- `usuarios.json` - User accounts and authentication
- `componentes.json` - Component inventory
- `userdata/` - Per-user build configurations

## Architecture

PCBuildr is built with a clean, modular architecture:

- **Frontend/** - PyQt5 GUI application (main executable)
  - `app.py` - Main application and UI orchestration
  - `build_analyzer.py` - Build analysis and scoring engine
  - `user_data/` - User profiles and build history
- **core/** - Intelligent analysis modules
  - `compatibility.py` - Component compatibility checking
  - `recommender.py` - Build recommendations engine
  - `scoring.py` - Performance and build tier scoring
  - `explainer.py` - Component specifications and documentation
  - `responses.py` - Offline response generation
- **Backend/** - FastAPI server (optional, for future features)
- **data/** - Reference databases (JSON)
  - `componentes.json` - Component inventory

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed technical explanation.

## FAQ

**Q: How do I start the application?**
A: Run `python Frontend/app.py` or use `run_pcbuildr.bat` on Windows.

**Q: Do I need to install any external dependencies like Ollama?**
A: No! PCBuildr is self-contained and works completely offline. No external services required.

**Q: Can I use it without the backend?**
A: Yes! The frontend is fully functional standalone for all core features.

**Q: How accurate are the compatibility checks?**
A: Very accurate! We validate socket compatibility, RAM types, power budgets, and physical constraints.

**Q: What can I do with saved builds?**
A: Save multiple PC configurations under your user profile. Each build includes component selections and build analysis.

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
