# ConfigRelay — Parallel, No-Paste Network Configuration Orchestrator

**ConfigRelay** eliminates manual copy-paste by pushing configurations to **many devices in parallel**.  
It supports **direct SSH**, **console/bastion → device** hop, and **mixed paths**—all driven by **YAML runbooks** and **inventory metadata**.

---

## ✨ Features

- **Zero copy-paste:** YAML-driven steps apply configs reliably.
- **Parallel fan-out:** Push to dozens/hundreds of devices concurrently.
- **Multi-hop aware:** Direct SSH or Console/Bastion → Device (nested SSH).
- **Inventory-smart:** Region → DC → Building → Rack → Device filtering.
- **Credential strategy:** JIT, Keychain, or manual prompts; per-device type.
- **Full transcripts & logs:** Per-device `.log`, `.transcript.txt`, `.errors.json`.
- **Extensible:** Add vendors/models/runbooks without changing core code.
- **Dry-run & validation hooks:** Plan before execution; plug custom validators.

---

## 📦 Installation

### 1) Clone

```bash
git clone https://github.com/your-org/configrelay.git
cd configrelay
```

### 2) Create venv

**macOS / Linux**
```bash
python -m venv .venv
. .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3) Install

```bash
pip install -r requirements.txt
# Dev (editable):
pip install -e .
# or End users:
# pip install .
```

Now you can run:

```bash
configrelay --help
```

---

## 🧭 Quick Start

**Direct SSH** to devices from an inventory selection:

```bash
configrelay run   --runbook templates/device/Cisco/iosxe/runbook.yaml   --region ABL --racks ABL1-R1,ABL1-R2   --mode direct   --parallel 20
```

**Console → Device** (bastion/menu) path:

```bash
configrelay run   --runbook templates/console/Linux/ubuntu/runbook.yaml   --region ABL --racks ABL1-R1   --mode console   --parallel 10
```

**Mixed** (decide per device at runtime via runbook logic):

```bash
configrelay run   --runbook templates/_common/mixed_path/runbook.yaml   --region ABL --dc ABL1 --building DH1   --parallel 16
```

---

## ⚙️ CLI Overview

```bash
configrelay --help
```

Common flags:

- `run` — execute a runbook end-to-end  
- `--runbook <path>` — YAML defining steps & transports  
- `--region <name>` — choose region (auto-discovers available)  
- `--dc <name> --building <name> --racks <csv>` — optional narrowing  
- `--devices <csv>` — pick specific devices within racks  
- `--mode <direct|console|mixed>` — transport strategy override  
- `--parallel <N>` — concurrency (default: sensible per OS)  
- `--dry-run` — render plan, do not execute device commands  
- `--log-level <info|debug>` — increase verbosity  
- `--save-outputs` — keep raw/parsed/validated artifacts  
- `--prompt-credentials` — force manual creds (skip stored)  

Examples:

```bash
# Plan only
configrelay run --runbook templates/device/Arista/eos/runbook.yaml --region MFQ --dry-run

# Specific devices
configrelay run --runbook templates/device/Juniper/mx/runbook.yaml   --region MFQ --racks OC14-R21   --devices border-gw-01,border-gw-02   --parallel 8
```

---

## 📁 Project Structure (reference)

```
configrelay/
  modules/
    executor/            # runbook engine
    transports/          # console.py, direct_ssh.py, jumpchain.py
    inventory/           # region_loader.py, inventory.py
    creds/               # cred.py, keychain.py, jit.py
    logging_ext/         # transcript+log helpers
    parsers/             # output parsers (per vendor/model)
    validators/          # JSON validators (default + custom)
  templates/
    console/Linux/ubuntu/runbook.yaml
    device/Cisco/iosxe/runbook.yaml
    device/Arista/eos/runbook.yaml
    device/Juniper/mx/runbook.yaml
    _common/             # include files, mixed-path, shared steps
  inventory/
    ABL/ inventory.json  # generated from region sources
    ABL/ topology.json
  env/
    config.yaml          # REGION_PATH etc.
  logs/
    <runbook>/<ts>/<rack>/<device>/*.log|.transcript.txt|.errors.json
```

---

## 🧩 Runbook Anatomy (example)

```yaml
# templates/device/Cisco/iosxe/runbook.yaml
name: "Cisco IOS XE — Config Push"
transport: direct          # direct | console | mixed
parallel: 16               # default; overridable via CLI
steps:
  - action: session.open_ssh
    host_var: "device_ip"
    username_var: "username"
    password_var: "password"
    timeout: 25

  - action: config.enter_mode
    enter: "conf t"
    prompt_expect: "(config)#"

  - action: config.apply_lines
    source: "templates/device/Cisco/iosxe/snippets/ntp_core.txt"

  - action: config.save
    write_cmd: "write memory"
    expect: "[OK]"

  - action: session.close
```

**Console/Bastion example**:

```yaml
# templates/console/Linux/ubuntu/runbook.yaml
name: "Ubuntu Console — Select & Connect"
transport: console
steps:
  - action: session.open_ssh
    host: "{console_ip}"
    username_var: "console_username"
    password_var: "console_password"
    timeout: 20

  - action: console.menu_select_by_label
    expect_menu: "(?i)Select device:"
    device_label_var: "device_label"

  - action: session.expect
    expect: "(?i)(Username:|login:)"
  - action: session.sendln
    text_var: "device_username"
  - action: session.expect
    expect: "(?i)Password:"
  - action: session.send_secure
    var: "device_password"

  - action: config.apply_lines
    source: "templates/_common/snippets/enable_ntp.txt"

  - action: session.close
```

---

## 🗺 Inventory & Selection

- Auto-discover regions from `env/config.yaml`  
- Build `inventory/<region>/inventory.json` and `topology.json`  
- CLI filters narrow scope (region → DC → building → rack → device).  

---

## 🔐 Credentials

1. **JIT**  
2. **Keychain**  
3. **Manual prompt**  

Force manual:

```bash
configrelay run ... --prompt-credentials
```

---

## 🗃 Outputs & Artifacts

For each run:

```
logs/<runbook>/<timestamp>/<rack>/<device>/
  run.log              # structured logs
  run.transcript.txt   # full terminal IO (sanitized)
  run.errors.json      # line-by-line failures
```

---

## 🧪 Parsers & Validators

```yaml
- action: parse.output
  from_var: "command_output"
  parser: "cisco.interface_description"

- action: validate.parsed
  parsed_var: "parsed"
  expected_source: "json|topology"
  validator: "ifdesc.compare"
```

---

## 🔒 Safe Practices

- Start with `--dry-run`.  
- Use read-only runbooks before writes.  
- Validate after push.  

---

## 🤝 Contributing

1. Fork repo  
2. Create feature branch  
3. Add runbook/templates/modules  
4. Submit PR 🚀  

---

## 📜 License

MIT License © Your Name / Your Org
