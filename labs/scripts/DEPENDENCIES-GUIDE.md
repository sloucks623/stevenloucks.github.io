# Installation Guide for GitHub ITIL Automation Dependencies

## Quick Install (Recommended)
```powershell
# Navigate to your scripts directory
cd "c:\Users\New User\stevenloucks.github.io\scripts"

# Install all dependencies at once
pip install -r requirements.txt
```

## Individual Package Installation
```powershell
# Core functionality
pip install requests      # GitHub API calls
pip install rich         # Beautiful terminal output
pip install click        # Better command-line interface

# Optional enhancements
pip install PyYAML       # Configuration files
pip install GitPython    # Alternative Git operations
pip install jsonschema   # Data validation
```

## What Each Package Does

### requests
- **Purpose**: HTTP requests to GitHub API
- **Benefit**: Auto-discover repositories, check permissions
- **Example**: `requests.get("https://api.github.com/users/sloucks623/repos")`

### rich
- **Purpose**: Beautiful terminal output
- **Benefit**: Progress bars, colored text, tables
- **Example**: Shows progress while processing repositories

### click
- **Purpose**: Command-line interface framework
- **Benefit**: Better argument parsing, help text, validation
- **Example**: `@click.command()` decorators for functions

### PyYAML
- **Purpose**: YAML file parsing
- **Benefit**: Configuration files for lab metadata
- **Example**: Store lab descriptions, categories, status

## Verification
After installation, verify with:
```powershell
pip list | findstr "requests\|rich\|click\|PyYAML"
```

## Virtual Environment (Advanced)
For isolation, you can use a virtual environment:
```powershell
python -m venv itil-automation-env
itil-automation-env\Scripts\Activate.ps1
pip install -r requirements.txt
```
