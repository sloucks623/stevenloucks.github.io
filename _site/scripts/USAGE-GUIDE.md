# ITIL 4 Automation Usage Guide

## Quick Start

### Option 1: Simple Batch File (Recommended for beginners)
```batch
# Navigate to the scripts folder
cd "c:\Users\New User\stevenloucks.github.io\scripts"

# Run the automation (handles Python version automatically)
run-itil.bat

# Or with options:
run-itil.bat --create-missing --full-section
```

### Option 2: PowerShell Script
```powershell
# Navigate to scripts folder
cd "c:\Users\New User\stevenloucks.github.io\scripts"

# Run with PowerShell wrapper
.\run-itil-automation.ps1

# With options:
.\run-itil-automation.ps1 -CreateMissing -FullSection
```

### Option 3: Direct Python (if you know your Python command)
```bash
# If you have python3:
python3 itil-automation.py --help

# If you have Windows Python launcher:
py -3 itil-automation.py --help

# If you have standard python:
python itil-automation.py --help
```

## What The Script Does

1. **Scans for Lab Directories**: Looks for folders starting with "lab-"
2. **Checks README Files**: Examines existing README.md files
3. **Adds ITIL 4 Content**: Inserts professional service management references
4. **Creates Backups**: Saves original files before modification
5. **Reports Results**: Shows what was processed, created, or skipped

## Command Options

- `--create-missing`: Creates README.md files for labs that don't have them
- `--full-section`: Adds complete ITIL 4 section instead of just a link
- `--help`: Shows detailed help information

## Examples

### Basic Usage (Current Directory)
```batch
run-itil.bat
```

### Scan Specific Directory
```batch
run-itil.bat "C:\MyLabs"
```

### Create Missing READMEs and Add Full Sections
```batch
run-itil.bat --create-missing --full-section
```

## Troubleshooting

### Python Version Prompts
If Windows asks you to choose a Python version:

1. **Quick Fix**: Use the batch file `run-itil.bat` - it handles version selection
2. **Permanent Fix**: Set a default Python version:
   ```batch
   py -3 --version
   ```

### Python Not Found
1. Install Python from Microsoft Store (search "Python 3.11")
2. Or install from https://python.org/downloads
3. Make sure to check "Add Python to PATH" during installation

### Permission Errors
1. Run Command Prompt as Administrator
2. Or move your lab folders to a location you have write access to

## Professional Benefits

This automation demonstrates several ITIL 4 principles:

- **Optimize and Automate**: Reduces manual documentation tasks
- **Focus on Value**: Ensures consistent professional documentation
- **Collaborate and Promote Visibility**: Standardizes knowledge sharing
- **Progress Iteratively**: Improves documentation incrementally

## WGU BSCSIA Integration

This tool helps you:
- Demonstrate professional service management knowledge
- Apply ITIL 4 principles in practical lab work
- Create portfolio-ready documentation
- Show automation and scripting skills
- Maintain consistent professional standards across projects

---

**Author**: Steven Loucks - WGU BSCSIA Program  
**Last Updated**: July 7, 2025
