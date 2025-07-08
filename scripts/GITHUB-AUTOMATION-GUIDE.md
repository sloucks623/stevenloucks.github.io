# GitHub Lab ITIL 4 Automation - Quick Start Guide

## 🎯 What This Does

This automation adds professional ITIL 4 service management documentation to all your GitHub lab repositories automatically. It demonstrates the ITIL 4 principle "Optimize and Automate" in action!

## 🚀 Quick Start (Easiest Way)

1. **Navigate to scripts folder:**
   ```cmd
   cd "c:\Users\New User\stevenloucks.github.io\scripts"
   ```

2. **Run a dry-run first (safe preview):**
   ```cmd
   run-github-itil.bat --dry-run
   ```

3. **If you like what you see, run for real:**
   ```cmd
   run-github-itil.bat
   ```

## 📋 Your Current Lab Repositories

The automation will process these existing repositories:
- `lab-soc-automation`
- `lab-active-directory-1.0`
- `lab-active-directory-2.0` 
- `lab-detection-1.0`

## 🎛️ Advanced Options

### Process One Repository at a Time
```cmd
run-github-itil.bat lab-soc-automation
```

### Preview Changes Only (Dry Run)
```cmd
run-github-itil.bat --dry-run
```

### Direct Python Usage
```cmd
python github-itil-automation.py --help
python github-itil-automation.py --dry-run
python github-itil-automation.py lab-detection-1.0
```

## 📋 What Gets Added to Each Lab

The automation adds a professional ITIL 4 section to each lab's README.md:

```markdown
---

## 🎯 ITIL 4 Professional Practice

This lab demonstrates professional service management practices aligned with ITIL 4 principles:

- **Focus on Value**: Clear learning objectives and measurable outcomes
- **Start Where You Are**: Assessment of current state before implementation  
- **Progress Iteratively**: Phased approach with feedback loops
- **Collaborate and Promote Visibility**: Transparent documentation and knowledge sharing
- **Think and Work Holistically**: End-to-end process consideration
- **Keep It Simple and Practical**: Streamlined, actionable procedures
- **Optimize and Automate**: Continuous improvement and automation

### 📚 References
📘 [ITIL 4 Cheat Sheet – Framework Reference](https://github.com/sloucks623/stevenloucks.github.io/blob/main/frameworks/itil-4-cheat-sheet.md)

### 🔗 Related Resources
- [Main Portfolio](https://stevenloucks.tech) - Professional cybersecurity portfolio
- [All Lab Projects](https://github.com/sloucks623?tab=repositories&q=lab-) - Complete lab collection

**Applied on**: [Current Date]  
**Student**: Steven Loucks - WGU BSCSIA Program

---
```

## 🛡️ Safety Features

- **Backup Protection**: Won't overwrite existing ITIL content
- **Dry Run Mode**: Preview changes before applying
- **Error Handling**: Graceful handling of network/Git issues
- **Temporary Workspace**: Uses temp folders for Git operations

## 🔧 Prerequisites

- Git installed and configured
- GitHub access (your existing setup works)
- Python 3.x (the batch file finds it automatically)

## 🆘 Troubleshooting

### "Git not found"
- Install Git: https://git-scm.com/download/win
- Or use GitHub Desktop which includes Git

### "Permission denied" 
- Make sure you're logged into GitHub in your terminal
- Try: `git config --list` to verify your setup

### "Repository not found"
- Check that your repository names match exactly
- Verify you have access to your repositories

### Python issues
- The batch file handles Python detection automatically
- If issues persist, install Python from Microsoft Store

## 🎓 Professional Benefits

This automation demonstrates several professional capabilities:

1. **ITIL 4 Knowledge**: Service management framework application
2. **Automation Skills**: Python scripting and Git automation  
3. **Documentation Standards**: Consistent professional documentation
4. **Portfolio Management**: Centralized framework management
5. **DevOps Practices**: Infrastructure as code principles

## 📈 Future Lab Integration

When you create new lab repositories:

1. **Name them with `lab-` prefix** (you're already doing this!)
2. **Add to the script**: Edit `EXISTING_LAB_REPOS` list in `github-itil-automation.py`
3. **Run automation**: Execute the script to add ITIL content
4. **Update portfolio**: Your main site will automatically link to them

## 🎯 Next Steps After Running

1. **Review Changes**: Check each repository on GitHub
2. **Customize Content**: Tailor ITIL applications to each specific lab
3. **Update Portfolio**: Ensure your main site links are current
4. **Document Process**: This automation itself is a portfolio demonstration!

---

**Author**: Steven Loucks - WGU BSCSIA Program  
**Last Updated**: July 7, 2025  
**Purpose**: Professional service management documentation automation
