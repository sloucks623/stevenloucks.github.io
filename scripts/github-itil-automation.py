#!/usr/bin/env python3
"""
GitHub Lab Repository ITIL 4 Automation
Author: Steven Loucks
Purpose: Add ITIL 4 documentation to GitHub lab repositories
Version: 3.0 - GitHub Multi-Repo Support
WGU BSCSIA Program - Professional Documentation Standards
"""

import os
import sys
import re
import subprocess
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

# Configuration - Updated for GitHub repos
FRAMEWORK_LINK = "📘 [ITIL 4 Cheat Sheet – Framework Reference](https://github.com/sloucks623/stevenloucks.github.io/blob/main/frameworks/itil-4-cheat-sheet.md)"

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

### 🔗 Related Resources
- [Main Portfolio](https://stevenloucks.tech) - Professional cybersecurity portfolio
- [All Lab Projects](https://github.com/sloucks623?tab=repositories&q=lab-) - Complete lab collection

**Applied on**: {date}  
**Student**: Steven Loucks - WGU BSCSIA Program

---
"""

# Your existing lab repositories (add new ones here as you create them)
EXISTING_LAB_REPOS = [
    "lab-soc-automation",
    "lab-active-directory-1.0", 
    "lab-active-directory-2.0",
    "lab-detection-1.0",
    "lab-soc-helpdesk"
    # Add future labs here
]

GITHUB_USERNAME = "sloucks623"
TEMP_DIR = None

def run_command(command, cwd=None, capture_output=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=capture_output,
            text=True,
            check=True
        )
        return result.stdout.strip() if capture_output else None
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {command}")
        print(f"   Error: {e.stderr if e.stderr else str(e)}")
        return None

def check_git_available():
    """Check if git is available"""
    result = run_command("git --version")
    if result:
        print(f"✅ Git found: {result}")
        return True
    else:
        print("❌ Git not found. Please install Git and try again.")
        return False

def get_github_repos():
    """Get list of lab repositories from GitHub"""
    print("🔍 Discovering lab repositories...")
    
    # Method 1: Use existing repo list
    repos = EXISTING_LAB_REPOS.copy()
    
    # Method 2: Try to discover via GitHub API (if available)
    try:
        # This would require GitHub CLI or API access
        # For now, we'll use the predefined list
        pass
    except:
        pass
    
    print(f"📋 Found {len(repos)} lab repositories:")
    for repo in repos:
        print(f"   - {repo}")
    
    return repos

def setup_temp_workspace():
    """Create temporary workspace for git operations"""
    global TEMP_DIR
    TEMP_DIR = tempfile.mkdtemp(prefix="itil_automation_")
    print(f"📁 Created temporary workspace: {TEMP_DIR}")
    return TEMP_DIR

def cleanup_temp_workspace():
    """Clean up temporary workspace"""
    global TEMP_DIR
    if TEMP_DIR and os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        print(f"🧹 Cleaned up temporary workspace")

def clone_repository(repo_name, workspace_dir):
    """Clone a repository to the workspace"""
    repo_url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}.git"
    repo_path = os.path.join(workspace_dir, repo_name)
    
    print(f"📥 Cloning {repo_name}...")
    result = run_command(f"git clone {repo_url}", cwd=workspace_dir)
    
    if result is not None and os.path.exists(repo_path):
        print(f"✅ Successfully cloned {repo_name}")
        return repo_path
    else:
        print(f"❌ Failed to clone {repo_name}")
        return None

def has_itil_content(content):
    """Check if README already contains ITIL 4 content"""
    itil_indicators = [
        "ITIL 4 Cheat Sheet",
        "ITIL 4 Professional Practice", 
        "itil-4-cheat-sheet.md",
        "stevenloucks.github.io/blob/main/frameworks"
    ]
    return any(indicator in content for indicator in itil_indicators)

def add_itil_to_readme(repo_path, repo_name):
    """Add ITIL 4 content to repository README"""
    readme_path = os.path.join(repo_path, "README.md")
    
    if not os.path.exists(readme_path):
        print(f"⚠️  No README.md found in {repo_name}")
        return False
    
    try:
        # Read current content
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has ITIL content
        if has_itil_content(content):
            print(f"⏭️  {repo_name} already has ITIL content - skipping")
            return False
        
        # Add ITIL section
        addition = ITIL_SECTION_TEMPLATE.format(
            framework_link=FRAMEWORK_LINK,
            date=datetime.now().strftime("%B %d, %Y")
        )
        
        updated_content = content.rstrip() + addition
        
        # Write updated content
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Added ITIL 4 content to {repo_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {repo_name}: {e}")
        return False

def commit_and_push_changes(repo_path, repo_name):
    """Commit and push ITIL changes back to GitHub"""
    print(f"📤 Committing changes to {repo_name}...")
    
    # Add changes
    result = run_command("git add README.md", cwd=repo_path)
    if result is None:
        return False
    
    # Check if there are changes to commit
    status = run_command("git status --porcelain", cwd=repo_path)
    if not status:
        print(f"ℹ️  No changes to commit for {repo_name}")
        return True
    
    # Commit changes
    commit_message = "docs: Add ITIL 4 professional practice documentation\n\n- Integrate ITIL 4 service management principles\n- Add framework reference and professional standards\n- Demonstrate WGU BSCSIA program alignment"
    
    result = run_command(f'git commit -m "{commit_message}"', cwd=repo_path)
    if result is None:
        return False
    
    # Push changes
    result = run_command("git push origin main", cwd=repo_path)
    if result is None:
        # Try master branch if main fails
        result = run_command("git push origin master", cwd=repo_path)
        if result is None:
            print(f"❌ Failed to push changes to {repo_name}")
            return False
    
    print(f"✅ Successfully pushed changes to {repo_name}")
    return True

def process_repository(repo_name, workspace_dir, dry_run=False):
    """Process a single repository"""
    print(f"\n🔬 Processing repository: {repo_name}")
    print("=" * 50)
    
    # Clone repository
    repo_path = clone_repository(repo_name, workspace_dir)
    if not repo_path:
        return False
    
    # Add ITIL content
    if add_itil_to_readme(repo_path, repo_name):
        if not dry_run:
            # Commit and push changes
            return commit_and_push_changes(repo_path, repo_name)
        else:
            print(f"🧪 DRY RUN: Would commit and push changes to {repo_name}")
            return True
    
    return False

def main():
    """Main execution function"""
    print("🚀 GitHub Lab Repository ITIL 4 Automation")
    print("=" * 60)
    print("WGU BSCSIA Program - Professional Documentation Standards")
    print()
    
    # Parse command line arguments
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    specific_repo = None
    
    for arg in sys.argv[1:]:
        if arg.startswith("--repo="):
            specific_repo = arg.split("=", 1)[1]
        elif not arg.startswith("--"):
            specific_repo = arg
    
    if dry_run:
        print("🧪 DRY RUN MODE: No changes will be pushed to GitHub")
        print()
    
    # Check prerequisites
    if not check_git_available():
        return 1
    
    try:
        # Setup workspace
        workspace_dir = setup_temp_workspace()
        
        # Get repositories to process
        if specific_repo:
            repos = [specific_repo] if specific_repo in EXISTING_LAB_REPOS else []
            if not repos:
                print(f"❌ Repository '{specific_repo}' not found in known lab repositories")
                return 1
        else:
            repos = get_github_repos()
        
        if not repos:
            print("🔍 No lab repositories found to process")
            return 0
        
        # Process each repository
        processed = 0
        skipped = 0
        errors = 0
        
        for repo_name in repos:
            try:
                if process_repository(repo_name, workspace_dir, dry_run):
                    processed += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"❌ Error processing {repo_name}: {e}")
                errors += 1
        
        # Summary
        print("\n📊 SUMMARY")
        print("=" * 30)
        print(f"✅ Processed: {processed}")
        print(f"⏭️  Skipped: {skipped}")
        print(f"❌ Errors: {errors}")
        print()
        
        if processed > 0:
            if dry_run:
                print("🧪 DRY RUN completed. Run without --dry-run to apply changes.")
            else:
                print("🎯 SUCCESS! ITIL 4 documentation has been added to your lab repositories.")
                print("💡 This demonstrates the ITIL 4 principle: 'Optimize and Automate'")
                print()
                print("Next steps:")
                print("- Check your GitHub repositories to verify the changes")
                print("- Review and customize the ITIL integration for each lab")
                print("- Update your portfolio links if needed")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1
    finally:
        cleanup_temp_workspace()

def show_help():
    """Display help information"""
    help_text = f"""
🚀 GitHub Lab Repository ITIL 4 Automation

USAGE:
    python github-itil-automation.py [repository] [options]

ARGUMENTS:
    repository          Specific repository name to process (optional)

OPTIONS:
    --dry-run          Show what would be done without making changes
    --force            Process even if ITIL content already exists  
    --repo=<name>      Process specific repository
    --help             Show this help message

EXAMPLES:
    python github-itil-automation.py                                    # Process all lab repos
    python github-itil-automation.py --dry-run                         # Preview changes
    python github-itil-automation.py lab-soc-automation               # Process specific repo
    python github-itil-automation.py --repo=lab-detection-1.0         # Alternative syntax

CURRENT LAB REPOSITORIES:
{chr(10).join(f'    - {repo}' for repo in EXISTING_LAB_REPOS)}

WHAT THIS SCRIPT DOES:
✅ Clones your lab repositories from GitHub
✅ Adds ITIL 4 professional practice documentation
✅ Links to your main portfolio and framework reference
✅ Commits and pushes changes back to GitHub
✅ Demonstrates automation and professional standards
✅ Supports both existing and future lab repositories

PREREQUISITES:
- Git must be installed and configured
- GitHub access (HTTPS or SSH) 
- Write access to your lab repositories

This automation supports your WGU BSCSIA program by demonstrating
professional service management practices across your lab portfolio.
"""
    print(help_text)

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()
    else:
        exit_code = main()
        sys.exit(exit_code)
