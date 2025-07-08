#!/usr/bin/env python3
"""
GitHub Lab Repository ITIL 4 Automation
Author: Steven Loucks
Purpose: Add ITIL 4 documentation to GitHub lab repositories
Version: 3.1 - Enhanced with GitHub API Discovery
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

# New imports for enhanced functionality
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️ Note: 'requests' not available. Using static repo list only.")

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    from rich.panel import Panel
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None
    print("⚠️ Note: 'rich' not available. Using basic output.")

# Configuration - Updated for GitHub repos
FRAMEWORK_LINK = "📘 [ITIL 4 Cheat Sheet – Framework Reference](https://github.com/sloucks623/stevenloucks.github.io/blob/main/frameworks/itil-4-cheat-sheet.md)"

# Compact version for minimal bloat
ITIL_COMPACT_TEMPLATE = """
---
**WGU BSCSIA Portfolio** | {framework_link} | **Applied**: {date}
"""

# Minimal README reference pointing to standalone file
ITIL_MINIMAL_TEMPLATE = """
---
📋 **Professional Standards**: [ITIL 4 Service Management Compliance](./ITIL-4-COMPLIANCE.md) | **WGU BSCSIA Portfolio**
"""

# Content for standalone ITIL compliance file
ITIL_STANDALONE_CONTENT = """# ITIL 4 Service Management Compliance

**Laboratory**: {lab_name}  
**Applied**: {date}  
**Student**: Steven Loucks - WGU BSCSIA Program  
**Portfolio**: [stevenloucks.tech](https://stevenloucks.tech)

## 🎯 ITIL 4 Professional Practice Demonstration

This laboratory demonstrates professional service management practices aligned with ITIL 4 principles:

### Core ITIL 4 Principles Applied

- **Focus on Value**: Clear learning objectives and measurable outcomes
- **Start Where You Are**: Assessment of current state before implementation  
- **Progress Iteratively**: Phased approach with feedback loops
- **Collaborate and Promote Visibility**: Transparent documentation and knowledge sharing
- **Think and Work Holistically**: End-to-end process consideration
- **Keep It Simple and Practical**: Streamlined, actionable procedures
- **Optimize and Automate**: Continuous improvement and automation

### Service Management Value Chain

This lab incorporates elements from the ITIL 4 Service Value Chain:

- **Plan**: Strategic planning and architectural design
- **Improve**: Continuous improvement through documentation and iteration
- **Engage**: Stakeholder communication through clear documentation
- **Design & Transition**: Implementation planning and controlled deployment
- **Obtain/Build**: Resource acquisition and environment construction
- **Deliver & Support**: Operational procedures and troubleshooting guides

### Professional Documentation Standards

- Structured approach to technical documentation
- Version control and change management
- Incident tracking and resolution procedures
- Knowledge management and transfer

### 📚 References and Resources

- 📘 [ITIL 4 Cheat Sheet – Framework Reference]({framework_link})
- 🔗 [Main Portfolio](https://stevenloucks.tech) - Professional cybersecurity portfolio
- 📁 [All Lab Projects](https://github.com/sloucks623?tab=repositories&q=lab-) - Complete lab collection
- 🎓 [WGU BSCSIA Program](https://www.wgu.edu/online-it-degrees/cybersecurity-information-assurance-bachelors-program.html)

### Academic Integration

This laboratory fulfills WGU BSCSIA program requirements by demonstrating:

1. **Technical Competency**: Hands-on implementation skills
2. **Professional Standards**: Industry framework adherence  
3. **Documentation Quality**: Clear, structured technical writing
4. **Service Management**: Understanding of operational best practices

---
*This compliance documentation demonstrates integration of academic learning with industry best practices, preparing for professional cybersecurity roles.*
"""

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
    if HAS_RICH:
        console.print("🔍 Discovering lab repositories...", style="cyan")
    else:
        print("🔍 Discovering lab repositories...")
    
    # Method 1: Use existing repo list
    repos = EXISTING_LAB_REPOS.copy()
    api_repos = []
    
    # Method 2: Try to discover via GitHub API (if available)
    if HAS_REQUESTS:
        try:
            if HAS_RICH:
                with console.status("[cyan]Querying GitHub API..."):
                    response = requests.get(f"https://api.github.com/users/{GITHUB_USERNAME}/repos", timeout=10)
                    response.raise_for_status()
                    
                    all_repos = response.json()
                    api_repos = [repo['name'] for repo in all_repos if repo['name'].startswith('lab-')]
            else:
                response = requests.get(f"https://api.github.com/users/{GITHUB_USERNAME}/repos", timeout=10)
                response.raise_for_status()
                
                all_repos = response.json()
                api_repos = [repo['name'] for repo in all_repos if repo['name'].startswith('lab-')]
            
            # Combine static and API repos
            repos = list(set(repos) | set(api_repos))
            repos.sort()  # Sort alphabetically
            
            if HAS_RICH:
                console.print(f"📋 API discovered {len(api_repos)} lab repositories", style="green")
            else:
                print(f"📋 API discovered {len(api_repos)} lab repositories")
                
        except requests.RequestException as e:
            if HAS_RICH:
                console.print(f"⚠️ GitHub API request failed: {e}", style="yellow")
            else:
                print(f"⚠️ GitHub API request failed: {e}")
        except Exception as e:
            if HAS_RICH:
                console.print(f"⚠️ Error discovering repos from GitHub API: {e}", style="yellow")
            else:
                print(f"⚠️ Error discovering repos from GitHub API: {e}")
    
    # Display results
    if HAS_RICH and repos:
        table = Table(title="Lab Repositories")
        table.add_column("Repository", style="cyan")
        table.add_column("Source", style="magenta")
        
        for repo in repos:
            source = "API + Static" if repo in api_repos and repo in EXISTING_LAB_REPOS else "API" if repo in api_repos else "Static"
            table.add_row(repo, source)
        
        console.print(table)
    else:
        print(f"📋 Total: {len(repos)} lab repositories:")
        for repo in repos:
            source = " (API)" if repo in api_repos else " (static)"
            print(f"   - {repo}{source}")
    
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
        "stevenloucks.github.io/blob/main/frameworks",
        "ITIL-4-COMPLIANCE.md"
    ]
    return any(indicator in content for indicator in itil_indicators)

def remove_existing_itil_content(content):
    """Remove existing ITIL content from README"""
    # Remove the full ITIL section
    patterns = [
        r'---\s*\n\s*## 🎯 ITIL 4 Professional Practice.*?---\s*\n',
        r'## 🎯 ITIL 4 Professional Practice.*?(?=##|$)',
        r'---\s*\n\*\*WGU BSCSIA Portfolio\*\*.*?\n',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    return content.rstrip()

def create_itil_compliance_file(repo_path, repo_name):
    """Create standalone ITIL-4-COMPLIANCE.md file"""
    compliance_path = os.path.join(repo_path, "ITIL-4-COMPLIANCE.md")
    
    # Generate lab name from repo name
    lab_name = repo_name.replace("lab-", "").replace("-", " ").title()
    
    compliance_content = ITIL_STANDALONE_CONTENT.format(
        lab_name=lab_name,
        framework_link=FRAMEWORK_LINK,
        date=datetime.now().strftime("%B %d, %Y")
    )
    
    try:
        with open(compliance_path, 'w', encoding='utf-8') as f:
            f.write(compliance_content)
        print(f"✅ Created ITIL compliance file: {compliance_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating ITIL compliance file: {e}")
        return False

def add_itil_to_readme(repo_path, repo_name, compact_mode=False, standalone_mode=False):
    """Add ITIL 4 content to repository README"""
    readme_path = os.path.join(repo_path, "README.md")
    
    if not os.path.exists(readme_path):
        print(f"⚠️  No README.md found in {repo_name}")
        return False
    
    try:
        # Read current content
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove any existing ITIL content first
        content = remove_existing_itil_content(content)
        
        # Create standalone ITIL file if in standalone mode
        if standalone_mode:
            create_itil_compliance_file(repo_path, repo_name)
            addition = ITIL_MINIMAL_TEMPLATE
        elif compact_mode:
            addition = ITIL_COMPACT_TEMPLATE.format(
                framework_link=FRAMEWORK_LINK,
                date=datetime.now().strftime("%B %Y")
            )
        else:
            addition = ITIL_SECTION_TEMPLATE.format(
                framework_link=FRAMEWORK_LINK,
                date=datetime.now().strftime("%B %d, %Y")
            )
        
        updated_content = content.rstrip() + addition
        
        # Write updated content
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        mode_text = "standalone ITIL file + minimal README reference" if standalone_mode else "compact ITIL footer" if compact_mode else "full ITIL section"
        print(f"✅ Added {mode_text} to {repo_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {repo_name}: {e}")
        return False

def commit_and_push_changes(repo_path, repo_name, standalone_mode=False):
    """Commit and push ITIL changes back to GitHub"""
    print(f"📤 Committing changes to {repo_name}...")
    
    # Add changes (README and possibly ITIL compliance file)
    result = run_command("git add README.md", cwd=repo_path)
    if result is None:
        return False
    
    # Add ITIL compliance file if in standalone mode
    if standalone_mode:
        result = run_command("git add ITIL-4-COMPLIANCE.md", cwd=repo_path)
        if result is None:
            return False
    
    # Check if there are changes to commit
    status = run_command("git status --porcelain", cwd=repo_path)
    if not status:
        print(f"ℹ️  No changes to commit for {repo_name}")
        return True
    
    # Commit changes
    if standalone_mode:
        commit_message = "docs: Refactor ITIL 4 documentation to standalone file\n\n- Move detailed ITIL 4 content to ITIL-4-COMPLIANCE.md\n- Add minimal reference in README\n- Improve README focus and readability\n- Demonstrate WGU BSCSIA program alignment"
    else:
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

def process_repository(repo_name, workspace_dir, dry_run=False, compact_mode=False, standalone_mode=False):
    """Process a single repository"""
    print(f"\n🔬 Processing repository: {repo_name}")
    print("=" * 50)
    
    # Clone repository
    repo_path = clone_repository(repo_name, workspace_dir)
    if not repo_path:
        return False
    
    # Add ITIL content
    if add_itil_to_readme(repo_path, repo_name, compact_mode, standalone_mode):
        if not dry_run:
            # Commit and push changes
            return commit_and_push_changes(repo_path, repo_name, standalone_mode)
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
    compact_mode = "--compact" in sys.argv
    standalone_mode = "--standalone" in sys.argv
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
        
        # Process each repository with progress tracking
        processed = 0
        skipped = 0
        errors = 0
        
        if HAS_RICH:
            # Use rich progress bar
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console
            ) as progress:
                task = progress.add_task("Processing repositories...", total=len(repos))
                
                for repo_name in repos:
                    progress.update(task, description=f"Processing {repo_name}...")
                    try:
                        if process_repository(repo_name, workspace_dir, dry_run, compact_mode, standalone_mode):
                            processed += 1
                        else:
                            skipped += 1
                    except Exception as e:
                        console.print(f"❌ Error processing {repo_name}: {e}", style="red")
                        errors += 1
                    
                    progress.advance(task)
                
                progress.update(task, description="✅ All repositories processed!")
        else:
            # Fallback for basic output
            for i, repo_name in enumerate(repos, 1):
                print(f"\n[{i}/{len(repos)}] Processing {repo_name}...")
                try:
                    if process_repository(repo_name, workspace_dir, dry_run, compact_mode, standalone_mode):
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
    --compact          Use minimal ITIL footer instead of full section
    --standalone       Create separate ITIL-4-COMPLIANCE.md file with minimal README reference
    --force            Process even if ITIL content already exists  
    --repo=<name>      Process specific repository
    --help             Show this help message

EXAMPLES:
    python github-itil-automation.py                                    # Process all lab repos
    python github-itil-automation.py --dry-run                         # Preview changes
    python github-itil-automation.py --standalone                      # Create standalone ITIL files
    python github-itil-automation.py --compact                         # Use compact footer mode
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
