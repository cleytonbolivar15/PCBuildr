# PCBuildr Architecture

## Overview

PCBuildr is built with a clean, modular architecture that separates concerns and enables easy customization.

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (PyQt5)                         │
│              app.py - Main application UI                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
    ┌─────────────────┴──────────────────┬──────────────────┐
    │                                    │                  │
┌───▼──────────────┐  ┌─────────────┐ ┌─▼────────────────┐
│ Build Analyzer   │  │   User      │ │ Component        │
│ (scoring)        │  │   Auth      │ │ Database         │
└───┬──────────────┘  └─────────────┘ └──────────────────┘
    │
    └─────────────────┬──────────────────┬──────────────────┐
                      │                  │                  │
                ┌─────▼──────┐    ┌─────▼──────┐    ┌──────▼──────┐
                │ Compatibility │   │ Recommender│    │ Explainer    │
                │ Checker      │   │ Engine     │    │ (help text)  │
                └──────────────┘   └────────────┘    └──────────────┘
                
    ┌─────────────────┬──────────────────┬──────────────────┐
    │                 │                  │                  │
┌───▼──────────────┐ │  ┌────────────┐  │  ┌──────────────┐
│ Offline System   │ │  │ Scoring    │  │  │ Responses    │
│ (default - no    │ │  │ Engine     │  │  │ Generator    │
│  API keys)       │ │  │ (ratings)  │  │  │ (Q&A)        │
└──────────────────┘ │  └────────────┘  │  └──────────────┘
                     │
┌────────────────────▼──────────────────────────────────────┐
│              Backend (FastAPI - Optional)                │
│   /components | /validate | /auth (for future use)       │
└──────────────────────────────────────────────────────────┘
```

## Modules

### Core Modules (`core/`)

#### `responses.py` - ResponseGenerator
Offline response system using intelligent heuristics instead of LLMs.

**Purpose:** Provide conversational responses without requiring any remote API or local model.

**Key Methods:**
- `answer_question(question)` - Route to appropriate response based on type
- `explain_component(name, type)` - Hardware explanations
- `compare_cpus/gpus()` - Component comparisons

**Features:**
- Question classification (recommendation, compatibility, performance, specification)
- Hardware knowledge base
- Multitask learning patterns
- Personality-driven responses

#### `compatibility.py` - CompatibilityChecker
Validates PC builds for hardware errors.

**Purpose:** Ensure selected components work together.

**Key Methods:**
- `check_build(components_dict)` - Full compatibility audit
- `_check_socket_compatibility()` - CPU-motherboard socket match
- `_check_ram_compatibility()` - RAM type, slots, speed
- `_check_psu_wattage()` - Power budget validation
- `_check_physical_fit()` - GPU length, cooler height
- `_check_bottleneck()` - CPU/GPU balance analysis

**Output:** List of issues with severity (error/warning/info), description, affected components, and fix recommendations.

#### `recommender.py` - RecommendationEngine
Suggests PC builds and components based on context.

**Purpose:** Guide users toward appropriate builds.

**Key Methods:**
- `recommend_build(budget, use_case)` - Complete build suggestion
- `suggest_alternative(component)` - Component swaps
- `rank_components(category, filters)` - Tier components by value

**Use Cases Supported:**
- Gaming (budget, mid-range, high-end)
- Workstation (professional rendering/modeling)
- Streaming (balanced CPU+GPU)
- Office (economical)

#### `explainer.py` - HardwareExplainer
Educates users about hardware components.

**Purpose:** Explain technical specs in user-friendly language.

**Key Methods:**
- `explain_component(name, type)` - What does it do? Why matters?
- `compare_cpus/gpus()` - Performance differences
- `explain_compatibility_issue(issue)` - Why is this a problem?

**Coverage:** CPU, GPU, RAM, PSU, Case, Cooler, Motherboard, and common issues.

#### `scoring.py` - BuildScorer
Rates PC builds on multiple dimensions.

**Purpose:** Give users feedback on build quality.

**Scoring Factors:**
1. **Performance** (35%) - CPU/GPU tier ranking
2. **Value** (25%) - Price-to-performance ratio
3. **Compatibility** (25%) - Number and severity of issues
4. **Balance** (15%) - CPU-GPU matching

**Output:** 1-10 rating with breakdown + text rating (Excellent/Good/Fair/Poor).

### AI Layer (`ai/`)

#### `providers.py` - Provider Abstraction
Unified interface for multiple AI backends with graceful fallback.

**Classes:**

| Provider | Config | Status |
|----------|--------|--------|
| **OfflineProvider** | Built-in | Always works |
| **OpenAIProvider** | OPENAI_API_KEY | Optional |
| **OpenRouterProvider** | OPENROUTER_API_KEY | Optional |
| **GroqProvider** | GROQ_API_KEY | Optional |

**Features:**
- Automatic detection of configured providers
- Silent fallback to offline mode
- Provider switching at runtime
- Error handling and timeouts

**Factory Pattern:**
```python
factory = AIProviderFactory()
provider = factory.get_provider()  # Returns best available
manager = AIProviderManager()
response = manager.query(messages)  # Automatic fallback
```

#### `bytecoon.py` - Bytecoon Assistant
Orchestrates all AI modules into a cohesive assistant.

**Key Methods:**
- `ask(question)` - Main query interface
- `check_compatibility(build)` - Route to CompatibilityChecker
- `get_recommendation(budget, use_case)` - Route to RecommendationEngine
- `explain_component()` - Route to HardwareExplainer
- `score_build()` - Route to BuildScorer

**Personality:**
- Bilingual (Spanish/English)
- Maintains conversation history
- Proactive suggestions based on current build
- Friendly "technical raccoon" persona

### Frontend Architecture (`Frontend/`)

#### Directory Structure
```
Frontend/
├── app.py              # Main entry point (lightweight)
├── ui/
│   ├── dialogs.py      # LoadingDialog, WelcomeDialog, AuthDialog
│   ├── styles.py       # Centralized stylesheets (1000+ lines)
│   ├── components_selector.py  # Component selection UI
│   └── sections/
│       ├── chat.py          # Bytecoon chat interface
│       ├── pcbuild.py        # PC building section
│       └── settings.py       # Settings/config section
├── services/
│   ├── api.py          # Backend HTTP calls
│   ├── database.py     # SQLite operations
│   └── user_session.py # Authentication and user data
└── i18n/
    └── translations.py # Centralized text translations
```

#### Key Components

**dialogs.py:**
- `LoadingDialog` - Startup loading screen
- `WelcomeDialog` - Welcome/intro
- `AuthDialog` - Login/register/delete user

**styles.py:**
- `APP_STYLE_DARK` - Complete dark theme CSS
- `APP_STYLE_LIGHT` - Complete light theme CSS
- Style constants for consistency

**sections/chat.py:**
- Display Bytecoon responses
- Message input and history
- Clear chat button
- Language/theme switching

**services/api.py:**
- `login(username, password)` - Backend auth
- `register(username, password)` - User creation
- `delete_user(username)` - Account deletion
- Error handling and retries

**services/database.py:**
- Build management (create, read, update, delete)
- Component storage per build
- Issue/failure logging
- Export to JSON

**services/user_session.py:**
- Current user tracking
- Per-user data directory (hashed)
- Chat history persistence
- Build history

### Backend Architecture (`Backend/`)

#### FastAPI Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/login` | POST | User authentication |
| `/register` | POST | New user creation |
| `/delete_user` | POST | Account deletion |
| `/validar_build` | POST | Compatibility check |
| `/componentes` | GET | Search components |
| `/precios` | GET | Price comparison |

#### Data Models

```python
class CPU(dataclass):
    nombre, socket, tdp, generacion

class Motherboard(dataclass):
    nombre, socket, chipset, formato, ram_tipo, ram_slots, max_ram

class RAM(dataclass):
    nombre, tipo, capacidad, velocidad, sticks

class GPU(dataclass):
    nombre, largo_mm, tdp, pines

class Fuente(dataclass):
    nombre, potencia, pines_gpu, certificacion

class Gabinete(dataclass):
    nombre, formato, max_gpu_mm, max_cooler_mm

class Cooler(dataclass):
    nombre, altura_mm
```

#### Scrapers

**Architecture:** Base-derived pattern
- `BaseScraper` - Common logic (database, categorization, queries)
- `ExtremetechScraper` - Store-specific scraping
- `IntelecScraper` - Store-specific scraping
- `FacebookScraper` - Placeholder (anti-scraping measures)

**Shared Methods:**
- `crear_db()` - Create/initialize tables
- `categorizar(nombre)` - Component type detection
- `actualizar_db()` - Update prices
- `obtener_componentes(categoria)` - Query by category

### Configuration (`config.py`)

Centralized configuration with environment variable support:

```python
class Config:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "offline")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./pcbuildr.db")
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "es")
```

**Benefits:**
- Single source of truth for settings
- Easy environment variable configuration
- No hardcoded paths/credentials
- Validation methods

## Data Flow

### User Questions

```
User Message
    ↓
Bytecoon.ask(question)
    ↓
AIProviderManager.query()
    ├─ Try: Configured provider (OpenAI/OpenRouter/Groq)
    ├─ On Failure: Fallback to OfflineProvider
    └─ OfflineProvider routes to ResponseGenerator
        ├─ Question classification
        ├─ Hardware knowledge lookup
        ├─ Template-based response generation
        └─ Return conversational response
    ↓
Display in UI
```

### Build Compatibility Check

```
User selects components
    ↓
CompatibilityChecker.check_build()
    ├─ Socket compatibility
    ├─ RAM type/slots
    ├─ PSU wattage
    ├─ Physical fit
    ├─ Bottleneck detection
    └─ Return list of issues
    ↓
UI displays issues with fixes
```

### Build Recommendation

```
User asks for recommendation
    ↓
Bytecoon.get_recommendation(budget, use_case)
    ↓
RecommendationEngine.recommend_build()
    ├─ Select tier based on budget
    ├─ Choose components for use_case
    ├─ Calculate PSU requirement
    └─ Return complete build dict
    ↓
Display in UI, allow customization
```

## Design Patterns

### Factory Pattern
`AIProviderFactory` - Creates appropriate AI provider instances

### Strategy Pattern
`AIProvider` abstract class with multiple implementations (Offline, OpenAI, etc.)

### Singleton Pattern
`Bytecoon` instance shared across application

### Repository Pattern
`Services` modules abstract database and API access

### Template Method Pattern
`BaseScraper` provides template, subclasses implement `scrape()`

## Key Decisions

### 1. Offline-First Philosophy
- **Why:** Users shouldn't need external setup
- **How:** Intelligent logic instead of ML models
- **Result:** Instant startup, no waiting for model loading

### 2. Provider Abstraction
- **Why:** Flexibility for future AI backends
- **How:** Strategy pattern with graceful fallback
- **Result:** Optional AI enhancement without breaking offline mode

### 3. Modular Core
- **Why:** Easy to test, maintain, extends
- **How:** Separate concerns (recommender, compatibility, explainer, scoring)
- **Result:** Can improve each module independently

### 4. Centralized Configuration
- **Why:** Easy customization without code changes
- **How:** Environment variables via config.py
- **Result:** Deploy anywhere with `.env` tweaks

## Performance Considerations

- **Startup:** <2 seconds (no ML inference)
- **Queries:** <100ms (rule-based logic)
- **Memory:** ~150MB (UI + logic, no large models)
- **Offline:** Works completely without network

## Extensibility

### Adding a New Recommender Module
```python
# In core/recommender.py
def recommend_build_for_streaming(budget):
    # CPU-heavy recommendation
    pass

# In ai/bytecoon.py
def get_streaming_recommendation(budget):
    return self.recommender.recommend_build_for_streaming(budget)
```

### Adding a New AI Provider
```python
# In ai/providers.py
class MyAIProvider(AIProvider):
    def query(self, messages):
        # Call your API
        pass

    def is_available(self):
        return bool(self.api_key)

# Register in AIProviderFactory.get_provider()
```

### Adding Store Scraper
```python
# In Backend/scrapers/newstore.py
class NewStoreScraper(BaseScraper):
    def scrape(self):
        # Store-specific scraping
        pass

# Update Backend/main.py routes
```

## Testing Strategy

- **Core Modules:** Unit tests for logic (recommender, compatibility, scoring)
- **Providers:** Mock API responses for external providers
- **Frontend:** Integration tests for UI flows
- **Backend:** API endpoint tests

---

**PCBuildr is designed to be maintainable, extensible, and user-friendly.** 🦝
