#!/usr/bin/env python3
"""
ITIL 4 Lab Documentation Automation Script
Author: Steven Loucks
Purpose: Automatically add ITIL 4 reference links to lab README files
Version: 2.0
WGU BSCSIA Program - Professional Documentation Standards
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path

# Configuration
FRAMEWORK_LINK = "📘 [ITIL 4 Cheat Sheet – Framework Reference](../frameworks/itil-4-cheat-sheet.md)"
ITIL_SECTION_TEMPLATE = """
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
{framework_link}

**Applied on**: {date}  
**Student**: Steven Loucks - WGU BSCSIA Program

---
"""

def find_lab_directories(base_path="."):
    """Find all directories that start with 'lab-'"""
    lab_dirs = []
    try:
        for item in os.listdir(base_path):
            full_path = os.path.join(base_path, item)
            if item.startswith("lab-") and os.path.isdir(full_path):
                lab_dirs.append(full_path)
        return sorted(lab_dirs)
    except PermissionError:
        print(f"❌ Permission denied accessing: {base_path}")
        return []

def check_readme_exists(lab_dir):
    """Check if README.md exists in the lab directory"""
    readme_path = os.path.join(lab_dir, "README.md")
    return os.path.exists(readme_path), readme_path

def has_itil_content(content):
    """Check if README already contains ITIL 4 content"""
    itil_indicators = [
        "ITIL 4 Cheat Sheet",
        "ITIL 4 Professional Practice",
        "itil-4-cheat-sheet.md"
    ]
    return any(indicator in content for indicator in itil_indicators)

def backup_file(file_path):
    """Create a backup of the original file"""
    backup_path = f"{file_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        with open(file_path, 'r', encoding='utf-8') as original:
            with open(backup_path, 'w', encoding='utf-8') as backup:
                backup.write(original.read())
        return backup_path
    except Exception as e:
        print(f"⚠️  Warning: Could not create backup for {file_path}: {e}")
        return None

def add_itil_section(readme_path, framework_link, full_section=True):
    """Add ITIL 4 content to README file"""
    try:
        # Read current content
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has ITIL content
        if has_itil_content(content):
            print(f"⏭️  Skipped (already has ITIL content): {readme_path}")
            return False
        
        # Create backup
        backup_path = backup_file(readme_path)
        if backup_path:
            print(f"💾 Backup created: {backup_path}")
        
        # Determine what to add
        if full_section:
            addition = ITIL_SECTION_TEMPLATE.format(
                framework_link=framework_link,
                date=datetime.now().strftime("%B %d, %Y")
            )
        else:
            addition = f"\n{framework_link}\n"
        
        # Add content
        updated_content = content.rstrip() + addition
        
        # Write updated content
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing {readme_path}: {e}")
        return False

def create_missing_readme(lab_dir):
    """Create a basic README.md for labs that don't have one"""
    readme_path = os.path.join(lab_dir, "README.md")
    lab_name = os.path.basename(lab_dir).replace("lab-", "").replace("-", " ").title()
    
    readme_content = f"""# {lab_name} Lab

## Overview

This lab demonstrates {lab_name.lower()} concepts and implementations in a cybersecurity context.

## Objectives

- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## Prerequisites

- Basic knowledge of cybersecurity concepts
- Access to lab environment

## Lab Steps

### Step 1: Setup
[Detailed setup instructions]

### Step 2: Implementation
[Implementation steps]

### Step 3: Validation
[Testing and validation procedures]

## Results and Analysis

[Document your findings and analysis here]

## Troubleshooting

[Common issues and solutions]

## Conclusion

[Summary of what was learned and achieved]

{ITIL_SECTION_TEMPLATE.format(
    framework_link=FRAMEWORK_LINK,
    date=datetime.now().strftime("%B %d, %Y")
)}
"""
    
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        return True
    except Exception as e:
        print(f"❌ Error creating README for {lab_dir}: {e}")
        return False

def main():
    """Main execution function"""
    print("🚀 ITIL 4 Lab Documentation Automation")
    print("=" * 50)
    
    # Get command line arguments
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    create_missing = "--create-missing" in sys.argv
    full_section = "--full-section" in sys.argv or "--full" in sys.argv
    
    print(f"📁 Scanning directory: {os.path.abspath(base_path)}")
    print(f"🔧 Options: Create missing READMEs: {create_missing}, Full ITIL section: {full_section}")
    print()
    
    # Find lab directories
    lab_dirs = find_lab_directories(base_path)
    
    if not lab_dirs:
        print("🔍 No directories starting with 'lab-' found.")
        return
    
    print(f"📋 Found {len(lab_dirs)} lab directories:")
    for lab_dir in lab_dirs:
        print(f"   - {lab_dir}")
    print()
    
    # Process each lab directory
    processed = 0
    created = 0
    skipped = 0
    errors = 0
    
    for lab_dir in lab_dirs:
        print(f"🔬 Processing: {lab_dir}")
        
        readme_exists, readme_path = check_readme_exists(lab_dir)
        
        if not readme_exists:
            if create_missing:
                print(f"📝 Creating missing README: {readme_path}")
                if create_missing_readme(lab_dir):
                    created += 1
                    print(f"✅ Created README with ITIL content: {readme_path}")
                else:
                    errors += 1
            else:
                print(f"⚠️  No README.md found (use --create-missing to create): {readme_path}")
                skipped += 1
        else:
            # Process existing README
            if add_itil_section(readme_path, FRAMEWORK_LINK, full_section):
                processed += 1
                section_type = "full ITIL section" if full_section else "framework link"
                print(f"✅ Added {section_type}: {readme_path}")
            else:
                skipped += 1
        
        print()
    
    # Summary
    print("📊 SUMMARY")
    print("=" * 20)
    print(f"✅ Processed: {processed}")
    print(f"📝 Created: {created}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Errors: {errors}")
    print()
    
    if processed > 0 or created > 0:
        print("🎯 SUCCESS! ITIL 4 documentation has been integrated into your labs.")
        print("💡 This demonstrates the ITIL 4 principle: 'Optimize and Automate'")
        print()
        print("Next steps:")
        print("- Review the generated/updated README files")
        print("- Customize the ITIL integration for each specific lab")
        print("- Commit changes to your git repositories")

def show_help():
    """Display help information"""
    help_text = """
🚀 ITIL 4 Lab Documentation Automation

USAGE:
    python itil-automation.py [directory] [options]

ARGUMENTS:
    directory           Base directory to scan (default: current directory)

OPTIONS:
    --create-missing    Create README.md files for labs that don't have them
    --full-section      Add complete ITIL 4 section instead of just link
    --help              Show this help message

EXAMPLES:
    python itil-automation.py                                    # Scan current directory
    python itil-automation.py C:\\Labs                           # Scan specific directory
    python itil-automation.py --create-missing                  # Create missing READMEs
    python itil-automation.py --full-section                    # Add full ITIL sections

WHAT THIS SCRIPT DOES:
✅ Scans for directories starting with 'lab-'
✅ Checks README.md files for existing ITIL 4 content
✅ Adds ITIL 4 framework references to documentation
✅ Creates professional service management documentation
✅ Demonstrates ITIL 4 'Optimize and Automate' principle
✅ Maintains backup copies of original files

This automation supports your WGU BSCSIA program by demonstrating
professional documentation and service management practices.
"""
    print(help_text)

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()
    else:
        main()
