# onecli — Unified CLI Launcher for Modular Python Tools

**onecli** is a shared-venv based launcher that organizes and runs multiple Python CLI tools (apps) from a single interface.  
It lets you group tools into sections (e.g., `tools`, `pre-bootstrap`, `bootstrap`, `post-bootstrap`), manage their dependencies in a **shared virtual environment**, and launch them with a consistent UX.

---

## ✨ Features

- **Unified interface**: one command to access all your tools.
- **Section-based menus**: group apps logically (`tools`, `bootstrap`, etc.).
- **Shared venv**: install all requirements once, no per-project virtualenvs.
- **YAML-driven onboarding**: add new tools by editing `configs/projects.yaml`.
- **Default args**: preconfigure standard arguments for each project.
- **Help system**: link each tool to its GitHub/Docs README for quick reference.
- **Cross-platform**: works on Linux, macOS, and Windows (tested with Python 3.9+).

---

## 📦 Installation

Clone the repo:

```bash
git clone https://github.com/your-org/onecli.git
cd onecli

Create a shared virtual environment:

# Linux / macOS
python -m venv .venv
. .venv/bin/activate

# Windows
python -m venv .venv
.\.venv\Scripts\activate
