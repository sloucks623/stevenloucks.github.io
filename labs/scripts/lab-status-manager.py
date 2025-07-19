#!/usr/bin/env python3
"""
Lab Status Manager - Automates progress tracking across cybersecurity lab repositories
Integrates with the existing ITIL automation and portfolio website.

Features:
- Creates/updates LAB-STATUS.json in each repository
- Generates visual progress widgets for portfolio
- Auto-discovers labs and tracks completion status
- Supports both individual component tracking and overall progress
- Generates dashboard data for portfolio integration
"""

import json
import os
import requests
from datetime import datetime
import argparse
from pathlib import Path

class LabStatusManager:
    def __init__(self, github_token=None, username="sloucks623", portfolio_path=None):
        self.github_token = github_token
        self.username = username
        self.portfolio_path = portfolio_path or os.getcwd()
        self.headers = {"Authorization": f"token {github_token}"} if github_token else {}
        
        # Lab configuration - easily expandable
        self.lab_configs = {
            "lab-soc-automation": {
                "name": "SOC Automation Lab",
                "description": "Automating alert triage using Shuffle, Elastic Stack, and Slack integrations",
                "components": [
                    "Environment Setup",
                    "Shuffle Configuration", 
                    "Elastic Stack Deployment",
                    "Alert Automation",
                    "Slack Integration",
                    "Testing & Validation",
                    "Documentation"
                ]
            },
            "lab-active-directory-1.0": {
                "name": "Active Directory Lab 1.0",
                "description": "Set up a basic AD domain controller with DHCP, DNS, OUs, and users",
                "components": [
                    "Domain Controller Setup",
                    "DHCP Configuration",
                    "DNS Configuration", 
                    "Organizational Units",
                    "User Management",
                    "Group Policies",
                    "Documentation"
                ]
            },
            "lab-active-directory-2.0": {
                "name": "Active Directory Lab 2.0", 
                "description": "Expanded AD with GPOs, PowerShell automation, and segmentation",
                "components": [
                    "Advanced GPO Configuration",
                    "PowerShell Automation",
                    "Network Segmentation",
                    "Security Hardening",
                    "Monitoring Setup",
                    "Testing & Validation",
                    "Documentation"
                ]
            },
            "lab-detection-1.0": {
                "name": "Detection Lab 1.0",
                "description": "Standalone detection-focused environment with EDR, IDS, logging pipeline, and MITRE ATT&CK mapping",
                "components": [
                    "Environment Setup",
                    "EDR Deployment",
                    "IDS Configuration",
                    "Logging Pipeline",
                    "MITRE ATT&CK Mapping",
                    "Alert Rules",
                    "Testing & Validation",
                    "Documentation"
                ]
            }
        }
    
    def create_lab_status_template(self, repo_name):
        """Create a LAB-STATUS.json template for a repository"""
        if repo_name not in self.lab_configs:
            print(f"⚠️  Unknown lab: {repo_name}")
            return None
            
        config = self.lab_configs[repo_name]
        
        # Create status structure with components
        components_status = {}
        for component in config["components"]:
            components_status[component] = {
                "completed": False,
                "notes": "",
                "completion_date": None
            }
        
        status_data = {
            "lab_info": {
                "name": config["name"],
                "description": config["description"],
                "repository": f"https://github.com/{self.username}/{repo_name}",
                "created_date": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            },
            "overall_status": {
                "completion_percentage": 0,
                "status": "Not Started",  # Not Started, In Progress, Complete
                "priority": "Medium",  # Low, Medium, High
                "estimated_hours": None,
                "actual_hours": None
            },
            "components": components_status,
            "milestones": [
                {
                    "name": "Initial Setup",
                    "completed": False,
                    "completion_date": None
                },
                {
                    "name": "Core Implementation", 
                    "completed": False,
                    "completion_date": None
                },
                {
                    "name": "Testing & Validation",
                    "completed": False,
                    "completion_date": None
                },
                {
                    "name": "Documentation Complete",
                    "completed": False,
                    "completion_date": None
                }
            ],
            "itil_compliance": {
                "documented": True,  # Automatically true if using our automation
                "processes_mapped": False,
                "improvements_identified": False
            }
        }
        
        return status_data
    
    def update_completion_percentage(self, status_data):
        """Calculate completion percentage based on components and milestones"""
        components = status_data.get("components", {})
        milestones = status_data.get("milestones", [])
        
        # Calculate component completion
        total_components = len(components)
        completed_components = sum(1 for comp in components.values() if comp.get("completed", False))
        
        # Calculate milestone completion
        total_milestones = len(milestones)
        completed_milestones = sum(1 for milestone in milestones if milestone.get("completed", False))
        
        # Weight: 70% components, 30% milestones
        if total_components > 0 and total_milestones > 0:
            component_percentage = (completed_components / total_components) * 0.7
            milestone_percentage = (completed_milestones / total_milestones) * 0.3
            total_percentage = int((component_percentage + milestone_percentage) * 100)
        else:
            total_percentage = 0
        
        # Update status based on percentage
        if total_percentage == 0:
            status = "Not Started"
        elif total_percentage < 100:
            status = "In Progress"
        else:
            status = "Complete"
        
        status_data["overall_status"]["completion_percentage"] = total_percentage
        status_data["overall_status"]["status"] = status
        status_data["lab_info"]["last_updated"] = datetime.now().isoformat()
        
        return status_data
    
    def get_repo_content(self, repo_name, file_path):
        """Get content of a file from GitHub repository"""
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/contents/{file_path}"
        response = requests.get(url, headers=self.headers)
        return response
    
    def create_or_update_status_file(self, repo_name, dry_run=False):
        """Create or update LAB-STATUS.json in a repository"""
        print(f"\n🔄 Processing {repo_name}...")
        
        # Check if status file already exists
        response = self.get_repo_content(repo_name, "LAB-STATUS.json")
        
        if response.status_code == 200:
            # File exists, load and update
            import base64
            content = base64.b64decode(response.json()["content"]).decode("utf-8")
            try:
                existing_status = json.loads(content)
                print(f"   📄 Found existing LAB-STATUS.json")
                
                # Update completion percentage and timestamps
                updated_status = self.update_completion_percentage(existing_status)
                
                if dry_run:
                    print(f"   🔍 [DRY RUN] Would update completion percentage: {updated_status['overall_status']['completion_percentage']}%")
                    return updated_status
                else:
                    # Update the file
                    self.commit_status_file(repo_name, updated_status, response.json()["sha"])
                    return updated_status
                    
            except json.JSONDecodeError:
                print(f"   ⚠️  Invalid JSON in existing file, recreating...")
        
        # Create new status file
        status_data = self.create_lab_status_template(repo_name)
        if not status_data:
            return None
            
        if dry_run:
            print(f"   🔍 [DRY RUN] Would create new LAB-STATUS.json")
            print(f"   📊 Components: {len(status_data['components'])}")
            print(f"   🎯 Milestones: {len(status_data['milestones'])}")
            return status_data
        else:
            self.commit_status_file(repo_name, status_data)
            return status_data
    
    def commit_status_file(self, repo_name, status_data, sha=None):
        """Commit LAB-STATUS.json to repository"""
        import base64
        
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/contents/LAB-STATUS.json"
        
        content = json.dumps(status_data, indent=2)
        encoded_content = base64.b64encode(content.encode()).decode()
        
        payload = {
            "message": "🔄 Auto-update lab status tracking",
            "content": encoded_content
        }
        
        if sha:
            payload["sha"] = sha
        
        response = requests.put(url, headers=self.headers, json=payload)
        
        if response.status_code in [200, 201]:
            print(f"   ✅ Successfully {'updated' if sha else 'created'} LAB-STATUS.json")
        else:
            print(f"   ❌ Failed to {'update' if sha else 'create'} LAB-STATUS.json: {response.status_code}")
            print(f"   🔍 Response: {response.text}")
    
    def generate_portfolio_dashboard_data(self, lab_statuses):
        """Generate dashboard data for portfolio integration"""
        dashboard_data = {
            "summary": {
                "total_labs": len(lab_statuses),
                "completed_labs": 0,
                "in_progress_labs": 0,
                "not_started_labs": 0,
                "overall_completion": 0,
                "last_updated": datetime.now().isoformat()
            },
            "labs": []
        }
        
        total_percentage = 0
        
        for repo_name, status_data in lab_statuses.items():
            if not status_data:
                continue
                
            lab_info = status_data.get("lab_info", {})
            overall_status = status_data.get("overall_status", {})
            
            lab_summary = {
                "repository": repo_name,
                "name": lab_info.get("name", repo_name),
                "description": lab_info.get("description", ""),
                "completion_percentage": overall_status.get("completion_percentage", 0),
                "status": overall_status.get("status", "Not Started"),
                "priority": overall_status.get("priority", "Medium"),
                "github_url": f"https://github.com/{self.username}/{repo_name}",
                "components_total": len(status_data.get("components", {})),
                "components_completed": sum(1 for comp in status_data.get("components", {}).values() if comp.get("completed", False))
            }
            
            dashboard_data["labs"].append(lab_summary)
            total_percentage += lab_summary["completion_percentage"]
            
            # Update summary counts
            status = lab_summary["status"]
            if status == "Complete":
                dashboard_data["summary"]["completed_labs"] += 1
            elif status == "In Progress":
                dashboard_data["summary"]["in_progress_labs"] += 1
            else:
                dashboard_data["summary"]["not_started_labs"] += 1
        
        # Calculate overall completion
        if dashboard_data["summary"]["total_labs"] > 0:
            dashboard_data["summary"]["overall_completion"] = int(total_percentage / dashboard_data["summary"]["total_labs"])
        
        return dashboard_data
    
    def save_portfolio_dashboard(self, dashboard_data):
        """Save dashboard data to portfolio directory"""
        dashboard_path = os.path.join(self.portfolio_path, "data", "lab-dashboard.json")
        os.makedirs(os.path.dirname(dashboard_path), exist_ok=True)
        
        with open(dashboard_path, "w") as f:
            json.dump(dashboard_data, f, indent=2)
        
        print(f"\n📊 Portfolio dashboard data saved to: {dashboard_path}")
        return dashboard_path
    
    def run_status_update(self, repos=None, dry_run=False):
        """Main method to run status updates across all labs"""
        if repos is None:
            repos = list(self.lab_configs.keys())
        
        print(f"🚀 Starting lab status update for {len(repos)} repositories...")
        if dry_run:
            print("🔍 DRY RUN MODE - No changes will be made")
        
        lab_statuses = {}
        
        for repo_name in repos:
            if repo_name in self.lab_configs:
                status_data = self.create_or_update_status_file(repo_name, dry_run)
                lab_statuses[repo_name] = status_data
            else:
                print(f"⚠️  Skipping unknown repository: {repo_name}")
        
        # Generate dashboard data
        if lab_statuses:
            dashboard_data = self.generate_portfolio_dashboard_data(lab_statuses)
            
            if not dry_run:
                self.save_portfolio_dashboard(dashboard_data)
            
            # Print summary
            print(f"\n📈 Summary:")
            print(f"   Total Labs: {dashboard_data['summary']['total_labs']}")
            print(f"   Completed: {dashboard_data['summary']['completed_labs']}")
            print(f"   In Progress: {dashboard_data['summary']['in_progress_labs']}")
            print(f"   Not Started: {dashboard_data['summary']['not_started_labs']}")
            print(f"   Overall Completion: {dashboard_data['summary']['overall_completion']}%")
        
        return lab_statuses

def main():
    parser = argparse.ArgumentParser(description="Lab Status Manager - Automate progress tracking")
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument("--username", default="sloucks623", help="GitHub username")
    parser.add_argument("--portfolio-path", help="Path to portfolio directory")
    parser.add_argument("--repos", nargs="*", help="Specific repositories to update")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    
    args = parser.parse_args()
    
    # Get GitHub token from environment if not provided
    github_token = args.token or os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("⚠️  Warning: No GitHub token provided. Using read-only mode.")
        print("   Set GITHUB_TOKEN environment variable or use --token for write access.")
    
    manager = LabStatusManager(
        github_token=github_token,
        username=args.username,
        portfolio_path=args.portfolio_path
    )
    
    manager.run_status_update(repos=args.repos, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
