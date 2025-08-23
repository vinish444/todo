# PathProbe — Intelligent Network Path Validation

**PathProbe** is a topology-aware validation framework that discovers paths between devices and then **verifies them live**.  
It cross-checks expected connectivity (from topology data) against actual device state using commands like `show lldp neighbors`.  
When a path is broken, PathProbe investigates why — helping you identify mismatches, down links, or misconfigurations faster.

---

## ✨ Features

- **Path discovery**: Automatically trace logical connections between devices.  
- **Live validation**: Log into devices and run `show lldp neighbors` to confirm expected adjacencies.  
- **Root cause insight**: Understand *why* a path doesn’t work (e.g., interface down, missing neighbor, mismatch).  
- **Topology-driven**: Uses rack / region topology files to build expected paths.  
- **Automation-ready**: Extend with YAML runbooks for repeatable checks.  
- **Cross-vendor**: Works with Cisco, Juniper, Arista, and more.  

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-org/PathProbe.git
cd PathProbe
```

### 2. Create a virtual environment

#### Linux / macOS

```bash
python -m venv venv
. venv/bin/activate
```

#### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install the tool

#### Development mode (recommended during coding)

```bash
pip install -e .
```

#### Normal install (for end users)

```bash
pip install .
```

Now you can run:

```bash
pathprobe
```

---

## 🧭 Usage

After installation, simply run:

```bash
pathprobe
```

You’ll see:

```
==== PathProbe — Network Path Validator ====
1. Discover path between devices
2. Validate live via LLDP
3. Generate mismatch report
Q. Quit
```

- **Discover**: Finds paths based on topology input.  
- **Validate**: Logs into devices and runs neighbor checks.  
- **Report**: Highlights mismatches and reasons for failures.  

---

## ⚙️ CLI Options

```bash
pathprobe --help
```

Key flags:

- `--discover <deviceA> <deviceB>` : show logical path between two devices  
- `--validate <deviceA> <deviceB>` : run live LLDP validation  
- `--region <name>` : specify region / rack topology to use  
- `--report` : generate validation report in JSON/HTML  

---

## 🛠 Example Workflow

### Step 1. Discover Path

```bash
pathprobe --discover R1 R2 --region us-west
```

Output:

```
Expected path found:
R1 (xe-0/0/1) → Leaf1 (et1/1) → Spine2 (et3/4) → R2 (xe-0/0/0)
```

### Step 2. Validate Live

```bash
pathprobe --validate R1 R2
```

Output:

```
[OK] R1 sees Leaf1 on xe-0/0/1
[FAIL] Spine2 does not list R2 on et3/4
Reason: Interface down
```

### Step 3. Report

```bash
pathprobe --report
```

Generates `output/report.html` with PASS/FAIL status per hop.

---

## 📚 Architecture

```
pathprobe/
  ├─ configs/          # YAML runbooks and settings
  ├─ inventory/        # Rack / topology input
  ├─ modules/          # SSH + LLDP parsing modules
  ├─ output/           # Reports and logs
  └─ main.py           # CLI entrypoint
```

---

## 🤝 Contributing

1. Fork the repo  
2. Create a feature branch  
3. Add features or improve validations  
4. Submit a PR 🚀  

---

## 📜 License

MIT License © Your Name / Your Org
