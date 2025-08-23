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

### Clone the repo

```bash
git clone https://github.com/your-org/onecli.git
cd onecli
```

### Create a shared virtual environment

#### Linux / macOS

```bash
python -m venv .venv
. .venv/bin/activate
```

#### Windows

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### Install launcher dependencies

```bash
pip install --upgrade pip pyyaml
```

---

## 🧭 Usage

Run the launcher:

```bash
python loader.py
```

You’ll see:

```
==== Modular CLI Launcher (shared venv) ====
1. tools
2. bootstrap
U. Update ALL sections (install all requirements)
S. Update a SINGLE section
H. Help (project READMEs)
R. Refresh
Q. Quit
```

- Choose a section (e.g. `tools`).  
- Pick a project inside the section.  
- The project’s `main.py` runs inside the shared venv with its `default_args`.  

---

## ⚙️ CLI Options

```bash
python loader.py --help
```

Key flags:

- `--list-sections` : list sections from YAML  
- `--list` : list all projects with their section  
- `--list-readmes` : list projects that have `readme_url`  
- `--update` : install all project requirements into shared venv  
- `--update-section <name>` : install only one section’s requirements  
- `--project <id>` : run a specific project (bypass menus)  
- `--open-readme <id>` : open README link for a project in browser  

---

## ⌨️ Passing Arguments to a Project

Everything after `--` is passed directly to the project:

```bash
python loader.py --project auth_demo -- -u alice -p
```

---

## 🛠 Onboarding New Apps

All apps live under `projects/`, each in its own folder:

```
projects/
  ├─ auth_demo/
  │   ├─ requirements.txt
  │   └─ run.py
  ├─ example_a/
  │   ├─ requirements.txt
  │   └─ main.py
  └─ example_b/
      ├─ requirements.txt
      └─ main.py
```

### Step 1: Create the project folder

```bash
mkdir projects/my_tool
```

### Step 2: Add your Python script

Example `main.py`:

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="My Tool")
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    print(f"Hello {args.name}!")

if __name__ == "__main__":
    main()
```

### Step 3: Add requirements

```txt
# projects/my_tool/requirements.txt
requests>=2.31
```

### Step 4: Register in `configs/projects.yaml`

```yaml
- id: "my_tool"
  name: "My Custom Tool"
  section: "tools"
  entrypoint: "main.py"
  default_args: []
  readme_url: "https://github.com/your-org/my_tool#readme"
```

### Step 5: Install requirements

```bash
python loader.py --update-section tools
```

Now `my_tool` appears in the menu.

---

## 📚 Help System

If a project has `readme_url` defined in YAML, it will show up in the **Help menu (H)**:

```
==== Help / READMEs ====
1. [tools] auth demo -> https://github.com/python/cpython/blob/main/Lib/argparse.py
2. [tools] Example B — Log Cleaner -> https://click.palletsprojects.com/en/8.1.x/
B. Back
```

Selecting a project opens its README in your default browser.

---

## 🔧 Examples

Run with defaults (from YAML):

```bash
python loader.py --project auth_demo
```

Override defaults:

```bash
python loader.py --project auth_demo -- -u admin -p
```

Install/update all requirements:

```bash
python loader.py --update
```

Open docs for a tool:

```bash
python loader.py --open-readme auth_demo
```

---

## 🤝 Contributing

1. Fork the repo  
2. Create a feature branch  
3. Add your tool under `projects/` + update `configs/projects.yaml`  
4. Submit a PR 🚀  

---

## 📜 License

MIT License © Your Name / Your Org
