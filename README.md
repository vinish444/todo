
# Orchestron

**Orchestron** is an interactive and user friendly automation and validation framework designed to execute network device validations, parse command outputs, and generate structured reports.

It uses YAML-driven runbooks to define workflows for both **validation** and **configuration** tasks.
- **Validation runbooks** handle checks like firmware, link, and scorecard validations.
- **Configuration runbooks** automate configuration-related operations, such as setting up device clocks, DDOS devices etc.

The framework supports multi-vendor models and enables reusable parser/validator logic.

---

## 📂 Project Structure

```
Orchestron/
├── data/                     # Mapping and reference data for parsers/validators
│   ├── bgp_state.yaml
│   ├── device_role_patterns.yaml
│   ├── firmware_mapping.yaml
│   ├── interface_description_exceptions.yaml
│   ├── interface_map.yaml
│   ├── interface_status_map.yaml
│   ├── lldp_exceptions.yaml
│   └── type_lookup.yaml
│
├── env/                      # Environment-specific configs
│
│
├── inventory/                # Region-wise inventory data
│   ├── abc/
│   ├── qrs/
│   └── xyz/
│
├── modules/                  # Core Python modules
│   ├── custom/               # Custom logic (inventory mgmt, credential handling, region loader, etc.)
│   ├── executor/             # Runbook executor engine
│   ├── report/               # HTML/JSON report generation
│   ├── ssh_modules/          # SSH utilities (ssh_run, config)
│   └── validation_assets/    # Vendor/Model-specific parser, test_case, validate modules
│       ├── parser/
│       ├── test_case/
│       └── validate/
│
│
├── output/                   # Generated reports, parsed data, and results
│
├── runbook/                  # YAML-based validation workflows
│   ├── configuration/
│   └── validation/
│       ├── firmware_validation.yaml
│       ├── link_validation.yaml
│       ├── scorecard_validation.yaml
│       ├── ssh_access_validation_selected.yaml
│       └── test.yaml
│
├── test/                     # Test scripts
│
├── tools/                    # Utility scripts (scaffolding, etc.)
│
├── vendor/                   # Vendor & model mapping data
│   ├── test.yaml
│   └── vendor_data.yaml
│
├── venv/                     # Python virtual environment
│
├── main.py                    # CLI entry point for runbook execution
├── requirements.txt           # Python dependencies
└── readme.md                  # Project documentation
```

---

## 🚀 Features

- **Multi-vendor Support** – Supports Cisco, Juniper, Arista, and more via YAML-based mappings.
- **Runbook Driven** – Modular YAML workflows (`runbook/validation/*.yaml`) to define steps like SSH, parsing, and validation.
- **Dynamic Parsing & Validation** – Auto-loads vendor/model-specific parser and validator modules.
- **Inventory Filtering** – Select devices by Region → Building → Rack, with role-based filtering.
- **Credential Management** – Supports keychain/JIT/manual entry per device.
- **Report Generation** – HTML reports with PASS/FAIL status and diffs for mismatched results.

---

## ⚙️ Installation

1. **Clone the repository**
```bash
git clone <repo_url>
cd Orchestron
```

2. **Create a Python virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment configs**
- Place your environment-specific files in `env/`.
- Configure vendor and model mappings in `vendor/vendor_data.yaml`.

---

## 📜 Usage

### **Run the CLI**
```bash
python main.py
```

### **Workflow Steps**
1. **Select Category**  
   Choose from available categories (e.g., `validation`, `configuration`).

2. **Select Runbook(s)**  
   Pick one or more YAML runbooks from the selected category.

3. **Select Region**  
   Choose the region from available inventory.

4. **Select Building**  
   If multiple buildings exist, choose one; otherwise it is auto-selected.

5. **Select Racks & Devices**  
   Filter devices by rack and role as per runbook.

6. **Provide Credentials**  
   Automatically fetched from keychain/JIT/manual prompt.

7. **Execution & Reports**  
   Runs all steps in the runbook and generates HTML/JSON results in `output/`.

---

## 🛠 Runbook YAML Format

A runbook YAML (`runbook/validation/example.yaml`) contains:

```yaml
title: "Firmware Validation"
validation_folder: "firmware_validation"
device_role: ["vpn", "core"]
steps:
  - action: create_artifact_folder
    base_path: output
    folder_name: firmware_validation
    folder_module: modules.generic.create_artifact_folder

  - action: ssh_run
    commands:
      - show_version
      - show_inventory

  - action: parse_output
    parsers:
      show_version: version_parser
      show_inventory: inventory_parser

  - action: validate_output
    validators:
      show_version: version_validator
      show_inventory: inventory_validator
```

---

## 📊 Reports

- **HTML Report** – Located in `output/<validation_folder>/report.html`
- **JSON Results** – Includes:
  - `<device>_<command>.txt` (Raw output)
  - `<device>_<command>_parsed.json`
  - `<device>_<command>_expected.json`
  - `<device>_<command>.result.json`
  - `<device>_<command>_diff.json`

---

## 🧩 Extending Orchestron

1. **Add a new vendor/model**
   - Update `vendor/vendor_data.yaml` with models and default commands.

2. **Add a parser**
   - Place a new `.py` file under `modules/validation_assets/parser/<validation_folder>/<vendor>/<model>/`.

3. **Add a validator**
   - Place a new `.py` file under `modules/validation_assets/validate/<validation_folder>/<vendor>/<model>/`.

4. **Add a test case**
   - Place `.json` under `modules/validation_assets/test_case/<validation_folder>/<vendor>/<model>/`.

5. **Create a new runbook**
   - Add a `.yaml` file in `runbook/validation/`.

---

## 🖥 Example Commands

Run all link validations for region `abc`:
```bash
python main.py
# Select category: validation
# Select runbook: link_validation.yaml
# Select region: abc
```

Run firmware validation on all devices in building 1:
```bash
python main.py
# Select category: validation
# Select runbook: firmware_validation.yaml
# Select region & building
```

---

## 📌 Notes

- Ensure inventory JSON is up to date before running validations.
- Use `tools/scaffold_interactive.py` to scaffold parser/test_case/validator for new models.
- Output folder is auto-cleared per run before execution.

---

## 📄 License

This project is proprietary and intended for internal use.


---

## 🛠 Tools: Scaffold Interactive

The **scaffold_interactive.py** script under `tools/` allows you to quickly create the folder and file structure for parsers, test cases, and validators for new models.

### **Usage**
```bash
python tools/scaffold_interactive.py
```
**Features:**
- Select vendor from menu
- Enter multiple models (end with `#` to finish)
- Auto-copies default parser, test case, and validator files to new model folders
- Aborts if default files are missing

**Example:**
```
Select vendor:
1) Arista
2) Cisco
3) Juniper
vendor> 2
Enter model> CIS3000
Enter model> CIS9000
Enter model> #
Overwrite existing files if present? [y/N] y
Scaffolding assets...
```

---

## 🤝 How to Contribute

We welcome contributions to enhance **Orchestron**!

### Steps to Contribute
1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone <your_fork_url>
   cd Orchestron
   ```
3. **Create a new branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** – follow the project’s structure and coding conventions.
5. **Test your changes** locally before committing.
6. **Commit and push** your changes:
   ```bash
   git commit -m "Add feature: your feature description"
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** from your fork to the main repository.

### Contribution Guidelines
- Keep code modular and readable.
- Follow the **YAML runbook format** for new validations.
- Provide **test cases** for new parsers and validators.
- Update documentation if you add new functionality.

---

## 👤 Author

**Vinish Vijayan**  
📧 [vinish.vijayan@oracle.com](mailto:vinish.vijayan@oracle.com)
