# Contributing to HelixCore

Thank you for your interest in contributing to **HelixCore**! We welcome contributions of all kinds: bug fixes, new blueprint templates, autonomous agent persona features, documentation enhancements, and Antigravity harness tools.

---

## 🚀 Getting Started

1. **Fork the Repository**:
   Click the **Fork** button on GitHub to create your own copy.

2. **Clone your Fork**:
   ```bash
   git clone https://github.com/your-username/HelixCore.git
   cd HelixCore
   ```

3. **Set Up a Virtual Environment**:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```

4. **Install Dependencies in Editable Mode**:
   ```bash
   pip install -e ".[dev]"
   ```

5. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   # Add your test bot token and test Discord guild ID
   ```

---

## 🛠️ Development Standards

- **Code Formatting & Linting**:
  We use `ruff` to ensure clean, modern Python style:
  ```bash
  ruff check src/ templates/
  ruff format src/
  ```

- **Running Tests**:
  Ensure all automated unit and integration tests pass:
  ```bash
  pytest tests/ -v
  ```

- **Branch Naming Conventions**:
  - `feat/feature-name` (e.g., `feat/ollama-support`)
  - `fix/bug-description` (e.g., `fix/burst-typing-dedup`)
  - `docs/doc-update` (e.g., `docs/blueprint-spec`)

---

## 📜 Pull Request Process

1. Open your PR against the `main` branch.
2. Fill out the PR template completely.
3. Link relevant issues (`Closes #12`).
4. Ensure CI tests pass on all supported Python versions (3.10–3.12).
5. A maintainer will review your PR within 48 hours!

