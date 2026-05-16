# Contributing to PCBuildr

Thank you for your interest in contributing to PCBuildr! 🦝

## Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/yourusername/pcbuildr.git
cd pcbuildr
```

### 2. Set Up Development Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install pytest pytest-cov black flake8  # Dev tools
```

### 3. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

## Development Guidelines

### Code Style
- Follow PEP 8
- Use `black` for formatting: `black Frontend/ Backend/ core/ ai/`
- Lint with `flake8`: `flake8 Frontend/ Backend/ core/ ai/`
- Type hints for all functions

### File Organization
```
- Core logic → core/
- AI providers → ai/
- Frontend components → Frontend/ui/
- Backend endpoints → Backend/
- Utilities → appropriate module
```

### Commits
- Write clear, imperative commit messages
- Reference issues when applicable: `Fix #123: description`
- Keep commits focused on single features/fixes
- Example:
  ```
  Add bottleneck detection to compatibility checker

  Implements CPU/GPU tier analysis to detect performance mismatches.
  Fixes #45.
  ```

### Documentation
- Add docstrings to all functions/classes
- Update README.md for user-facing changes
- Update ARCHITECTURE.md for structural changes
- Include code examples where helpful

## Contributing Areas

### 🚀 High Priority

- [ ] Improve component database accuracy
- [ ] Add more store integrations
- [ ] Better GPU/CPU performance tiers
- [ ] Advanced thermal analysis
- [ ] Component price history graphs

### 📊 Medium Priority

- [ ] Unit test coverage
- [ ] API rate limiting
- [ ] Caching layer for component queries
- [ ] Mobile app prototype
- [ ] Dark mode improvements

### 📚 Lower Priority

- [ ] Community build sharing
- [ ] Benchmark integrations
- [ ] PCPartPicker API integration
- [ ] YouTube tutorial links
- [ ] Regional component databases

## Pull Request Process

1. **Update your branch**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Test your changes**
   ```bash
   pytest tests/
   python -m py_compile Frontend/app.py Backend/main.py core/*.py ai/*.py
   ```

3. **Format code**
   ```bash
   black .
   flake8 .
   ```

4. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **PR Description Template**
   ```markdown
   ## Description
   Brief explanation of changes

   ## Related Issues
   Fixes #123

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Enhancement
   - [ ] Documentation

   ## Testing
   How did you test this?

   ## Verification Checklist
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] Tests added/updated
   - [ ] No breaking changes
   ```

## Testing

### Running Tests
```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=core --cov=ai --cov-report=html

# Specific test file
pytest tests/test_compatibility.py
```

### What to Test
- **Core Modules:**
  - Recommendation logic with various budgets
  - Compatibility checks for common issues
  - Scoring algorithm accuracy
  - Response generation for different question types

- **Frontend:**
  - UI responsiveness
  - Language switching
  - Theme switching
  - Chat history persistence

- **Backend:**
  - API endpoints with valid/invalid inputs
  - Authentication flows
  - Component database queries

### Example Test
```python
def test_socket_compatibility():
    from core.compatibility import CompatibilityChecker
    checker = CompatibilityChecker()

    # Socket mismatch should return error
    build = {
        "cpu": {"socket": "Socket 1700"},
        "motherboard": {"socket": "Socket AM5"}
    }

    issues = checker.check_build(build)
    assert len(issues) > 0
    assert any("socket" in str(i).lower() for i in issues)
```

## Feature Ideas

### Component Recommendations
- [ ] ML-based preference learning
- [ ] Sustainability/eco-friendly ratings
- [ ] Noise level predictions
- [ ] Warranty tracking

### UI/UX
- [ ] Dark mode polish
- [ ] Mobile responsive design
- [ ] Component preview images
- [ ] Build aesthetic ratings

### Backend
- [ ] Component availability alerts
- [ ] Price drop notifications
- [ ] Seasonal build recommendations
- [ ] Regional currency conversion

## Reporting Issues

### Bug Reports
```markdown
## Description
Brief description

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected vs Actual
Expected: X
Actual: Y

## Environment
- OS: Windows 10
- Python: 3.9
- PyQt5: 5.15
```

### Feature Requests
```markdown
## Description
Clear description of feature

## Motivation
Why is this useful?

## Proposed Implementation
How might this work?

## Alternatives Considered
Other approaches?
```

## Code Review Process

### What We Look For
✅ **Good:**
- Clear, purposeful changes
- Good test coverage
- Helpful error messages
- Follows existing patterns
- Updates documentation

❌ **Problematic:**
- Over-engineering
- Hardcoded values
- Breaking changes without discussion
- Incomplete documentation
- Large PRs without context

### Review Turnaround
- Simple fixes: 1-2 days
- Features: 3-5 days
- Documentation: 1 day

## Style Guide

### Python
```python
# Good
def calculate_psu_requirement(cpu_tdp: int, gpu_tdp: int) -> int:
    """Calculate PSU wattage needed with headroom."""
    total = cpu_tdp + gpu_tdp + 150  # Overhead
    psu = int((total * 1.3) / 50) * 50
    return max(psu, 450)

# Bad (no types, unclear)
def calc_psu(a, b):
    return (a + b + 150) * 1.3
```

### Naming
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private methods: `_leading_underscore`

### Comments
```python
# Good - explain WHY
psu = int((total * 1.3) / 50) * 50  # Round to nearest 50W for compatibility

# Bad - explain WHAT (obvious from code)
psu = int(total * 1.3)  # Multiply by 1.3
```

## Licensing

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- 💬 Open an Issue for discussion
- 📧 Contact maintainers
- 🦝 Check existing discussions

---

**Thank you for helping make PCBuildr better!** 🎉

Your contributions help make PC building accessible to everyone.
