#!/usr/bin/env python3
"""
Complete Lab Integration - Automated Real Progress Tracking System
Creates assessment files for all labs and integrates with dashboard
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

class CompleteLabIntegration:
    def __init__(self):
        self.portfolio_path = Path(__file__).parent.parent
        self.assessments_dir = self.portfolio_path / "lab-assessments"
        self.data_dir = self.portfolio_path / "data"
        self.scripts_dir = self.portfolio_path / "scripts"
        
        # Create directories if they don't exist
        self.assessments_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
        # Lab templates for assessment creation
        self.lab_templates = {
            "lab-active-directory-1.0": {
                "name": "Active Directory Lab v1.0",
                "category": "Identity Management",
                "difficulty": "Intermediate",
                "estimated_hours": 12,
                "phases": [
                    {
                        "name": "Environment Setup",
                        "component": "Virtual Environment Setup",
                        "tasks": [
                            "Set up Windows Server 2019 VM (45 min)",
                            "Configure network settings (30 min)",
                            "Install Active Directory Domain Services (30 min)",
                            "Promote server to domain controller (30 min)",
                            "Configure DNS settings (15 min)"
                        ]
                    },
                    {
                        "name": "User Management",
                        "component": "User and Group Management",
                        "tasks": [
                            "Create organizational units (30 min)",
                            "Add domain users (45 min)",
                            "Configure security groups (30 min)",
                            "Set up service accounts (30 min)",
                            "Configure password policies (20 min)"
                        ]
                    },
                    {
                        "name": "Group Policy",
                        "component": "Group Policy Configuration",
                        "tasks": [
                            "Create basic GPO policies (45 min)",
                            "Configure security settings (30 min)",
                            "Set up software deployment (30 min)",
                            "Test policy application (30 min)",
                            "Document policy settings (30 min)"
                        ]
                    },
                    {
                        "name": "DNS Configuration",
                        "component": "DNS Server Setup",
                        "tasks": [
                            "Configure DNS zones (30 min)",
                            "Set up reverse lookup zones (20 min)",
                            "Configure DNS forwarders (15 min)",
                            "Test DNS resolution (15 min)",
                            "Document DNS configuration (20 min)"
                        ]
                    },
                    {
                        "name": "Security Hardening",
                        "component": "Security Implementation",
                        "tasks": [
                            "Configure firewall rules (30 min)",
                            "Set up audit policies (30 min)",
                            "Implement account lockout policies (20 min)",
                            "Configure event logging (25 min)",
                            "Create security documentation (35 min)"
                        ]
                    }
                ]
            },
            "lab-active-directory-2.0": {
                "name": "Active Directory Lab v2.0",
                "category": "Identity Management",
                "difficulty": "Advanced",
                "estimated_hours": 20,
                "phases": [
                    {
                        "name": "Multi-Forest Setup",
                        "component": "Forest Architecture",
                        "tasks": [
                            "Plan multi-forest architecture (60 min)",
                            "Deploy additional forest (90 min)",
                            "Configure forest functional levels (30 min)",
                            "Set up sites and subnets (45 min)",
                            "Configure replication topology (45 min)"
                        ]
                    },
                    {
                        "name": "Trust Relationships",
                        "component": "Forest Trust Configuration",
                        "tasks": [
                            "Configure forest trusts (60 min)",
                            "Set up external trusts (45 min)",
                            "Configure trust authentication (30 min)",
                            "Test cross-forest access (30 min)",
                            "Document trust relationships (30 min)"
                        ]
                    },
                    {
                        "name": "Advanced GPO",
                        "component": "Advanced Group Policy",
                        "tasks": [
                            "Create WMI filters (45 min)",
                            "Configure preference settings (45 min)",
                            "Set up central store (30 min)",
                            "Implement GPO delegation (30 min)",
                            "Create GPO reports (30 min)"
                        ]
                    },
                    {
                        "name": "Certificate Services",
                        "component": "PKI Implementation",
                        "tasks": [
                            "Install Certificate Authority (60 min)",
                            "Configure certificate templates (45 min)",
                            "Set up auto-enrollment (30 min)",
                            "Configure certificate revocation (30 min)",
                            "Test certificate deployment (30 min)"
                        ]
                    },
                    {
                        "name": "Monitoring Setup",
                        "component": "Monitoring and Reporting",
                        "tasks": [
                            "Install SCOM agents (45 min)",
                            "Configure monitoring rules (60 min)",
                            "Set up performance counters (30 min)",
                            "Create custom reports (45 min)",
                            "Configure alerting (30 min)"
                        ]
                    }
                ]
            },
            "lab-detection-1.0": {
                "name": "Threat Detection Lab",
                "category": "Threat Detection",
                "difficulty": "Advanced",
                "estimated_hours": 24,
                "phases": [
                    {
                        "name": "SIEM Installation",
                        "component": "SIEM Platform Setup",
                        "tasks": [
                            "Install Splunk infrastructure (120 min)",
                            "Configure indexers and search heads (90 min)",
                            "Set up deployment server (60 min)",
                            "Configure SSL certificates (45 min)",
                            "Test basic functionality (30 min)"
                        ]
                    },
                    {
                        "name": "Log Ingestion",
                        "component": "Data Collection",
                        "tasks": [
                            "Configure Windows event collection (60 min)",
                            "Set up Linux log forwarding (45 min)",
                            "Configure network device logging (60 min)",
                            "Set up application log collection (45 min)",
                            "Test log ingestion (30 min)"
                        ]
                    },
                    {
                        "name": "Detection Rules",
                        "component": "Detection Logic",
                        "tasks": [
                            "Create basic detection rules (90 min)",
                            "Configure alerting thresholds (45 min)",
                            "Set up correlation searches (60 min)",
                            "Create custom dashboards (60 min)",
                            "Test detection accuracy (45 min)"
                        ]
                    },
                    {
                        "name": "Threat Hunting",
                        "component": "Proactive Hunting",
                        "tasks": [
                            "Develop hunting queries (120 min)",
                            "Create hunting playbooks (90 min)",
                            "Set up hunting dashboards (60 min)",
                            "Configure threat intelligence feeds (45 min)",
                            "Document hunting procedures (45 min)"
                        ]
                    },
                    {
                        "name": "Incident Response",
                        "component": "Response Procedures",
                        "tasks": [
                            "Create response playbooks (90 min)",
                            "Configure automated responses (60 min)",
                            "Set up incident tracking (45 min)",
                            "Create response dashboards (45 min)",
                            "Test response procedures (60 min)"
                        ]
                    }
                ]
            },
            "lab-soc-helpdesk": {
                "name": "SOC Help Desk Lab",
                "category": "Service Management",
                "difficulty": "Intermediate",
                "estimated_hours": 10,
                "phases": [
                    {
                        "name": "Ticketing System",
                        "component": "ServiceNow Setup",
                        "tasks": [
                            "Install ServiceNow instance (60 min)",
                            "Configure basic incident management (45 min)",
                            "Set up user accounts and roles (30 min)",
                            "Configure email notifications (30 min)",
                            "Test ticket creation (15 min)"
                        ]
                    },
                    {
                        "name": "Workflow Design",
                        "component": "Process Configuration",
                        "tasks": [
                            "Design incident workflow (45 min)",
                            "Configure approval processes (30 min)",
                            "Set up escalation rules (30 min)",
                            "Create workflow documentation (30 min)",
                            "Test workflow execution (15 min)"
                        ]
                    },
                    {
                        "name": "SLA Configuration",
                        "component": "Service Level Agreements",
                        "tasks": [
                            "Define SLA requirements (30 min)",
                            "Configure SLA timers (30 min)",
                            "Set up SLA notifications (20 min)",
                            "Create SLA reports (25 min)",
                            "Test SLA compliance (15 min)"
                        ]
                    },
                    {
                        "name": "Reporting Setup",
                        "component": "Analytics and Reporting",
                        "tasks": [
                            "Create standard reports (45 min)",
                            "Configure automated reporting (30 min)",
                            "Set up performance dashboards (30 min)",
                            "Create custom metrics (30 min)",
                            "Test reporting accuracy (15 min)"
                        ]
                    },
                    {
                        "name": "User Training",
                        "component": "Documentation and Training",
                        "tasks": [
                            "Create user documentation (45 min)",
                            "Develop training materials (30 min)",
                            "Conduct user training sessions (30 min)",
                            "Create troubleshooting guides (30 min)",
                            "Finalize knowledge base (15 min)"
                        ]
                    }
                ]
            }
        }
    
    def create_assessment_file(self, lab_id, template):
        """Create a detailed assessment file for a lab"""
        assessment_file = self.assessments_dir / f"{lab_id}-progress.md"
        
        # Calculate initial progress (assume all tasks are pending initially)
        total_tasks = sum(len(phase['tasks']) for phase in template['phases'])
        
        content = f"""# Lab Progress Assessment - {template['name']}

## Lab Information
- **Name**: {template['name']}
- **Category**: {template['category']}
- **Difficulty**: {template['difficulty']}
- **Tutorial Source**: Custom implementation
- **Estimated Hours**: {template['estimated_hours']}

## Progress Tracking

"""
        
        # Add phases
        for i, phase in enumerate(template['phases'], 1):
            # Start with 0% complete for new assessments
            progress = 0
            status_emoji = "🔄"
            
            content += f"""### Phase {i}: {phase['name']} ({progress}% Complete) {status_emoji}
**Component**: {phase['component']}
"""
            
            # Add tasks
            for task in phase['tasks']:
                # Extract estimated time from task description
                time_match = re.search(r'\((\d+) min\)', task)
                if time_match:
                    task_name = task.replace(f"({time_match.group(1)} min)", "").strip()
                    duration = time_match.group(1)
                else:
                    task_name = task
                    duration = "30"  # Default duration
                
                content += f"- [ ] {task_name} ({duration} min)\n"
            
            content += f"""
**Lessons Learned**: [To be updated as phase progresses]
**Issues Overcome**: [To be updated as challenges are resolved]

"""
        
        # Add summary section
        content += f"""## Overall Progress Summary
- **Completed Tasks**: 0 out of {total_tasks} total tasks
- **Actual Progress**: 0% (0/{total_tasks} tasks completed)
- **Time Spent**: 0 hours out of {template['estimated_hours']} estimated
- **Remaining Tasks**: {total_tasks} tasks (estimated {template['estimated_hours']} hours)

## Skills Demonstrated
- 🔄 [Skills will be updated as lab progresses]

## Key Accomplishments  
- [To be updated as milestones are achieved]

## Challenges Overcome
- [To be updated as challenges are resolved]

## Next Session Goals
- [To be updated based on current progress]

**Estimated completion**: [To be determined based on progress]
"""
        
        # Write the assessment file
        with open(assessment_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created assessment file: {assessment_file}")
        return assessment_file
    
    def update_lab_status_from_assessment(self, lab_id, assessment_file):
        """Update lab status based on assessment file"""
        try:
            with open(assessment_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count completed vs total tasks
            completed_tasks = len(re.findall(r'- \[x\]', content))
            total_tasks = len(re.findall(r'- \[[ x]\]', content))
            
            if total_tasks == 0:
                progress = 0
            else:
                progress = round((completed_tasks / total_tasks) * 100, 1)
            
            # Load existing lab status
            lab_status_file = self.data_dir / "lab-status.json"
            try:
                with open(lab_status_file, 'r') as f:
                    lab_status = json.load(f)
            except FileNotFoundError:
                lab_status = {}
            
            # Update lab data
            if lab_id in lab_status:
                lab_status[lab_id]['progress'] = progress
                lab_status[lab_id]['completed_tasks'] = completed_tasks
                lab_status[lab_id]['total_tasks'] = total_tasks
                lab_status[lab_id]['last_updated'] = datetime.now().strftime("%Y-%m-%d")
                lab_status[lab_id]['status'] = 'Complete' if progress == 100 else 'In Progress'
                lab_status[lab_id]['status_color'] = '#00ff87' if progress == 100 else '#60efff'
                
                # Save updated status
                with open(lab_status_file, 'w') as f:
                    json.dump(lab_status, f, indent=2)
                
                print(f"✅ Updated {lab_id}: {progress}% complete ({completed_tasks}/{total_tasks} tasks)")
            else:
                print(f"⚠️  Lab {lab_id} not found in lab-status.json")
                
        except Exception as e:
            print(f"❌ Error updating lab status: {e}")
    
    def create_all_assessments(self):
        """Create assessment files for all labs"""
        print("🚀 Creating assessment files for all labs...")
        
        for lab_id, template in self.lab_templates.items():
            assessment_file = self.assessments_dir / f"{lab_id}-progress.md"
            
            if assessment_file.exists():
                print(f"⏭️  Assessment file already exists: {assessment_file}")
                # Update progress anyway
                self.update_lab_status_from_assessment(lab_id, assessment_file)
            else:
                # Create new assessment file
                self.create_assessment_file(lab_id, template)
                self.update_lab_status_from_assessment(lab_id, assessment_file)
    
    def update_dashboard_summary(self):
        """Update dashboard summary with real data"""
        lab_status_file = self.data_dir / "lab-status.json"
        dashboard_file = self.data_dir / "dashboard-summary.json"
        
        try:
            with open(lab_status_file, 'r') as f:
                lab_data = json.load(f)
            
            total_labs = len(lab_data)
            completed_labs = sum(1 for lab in lab_data.values() if lab['status'] == 'Complete')
            in_progress_labs = total_labs - completed_labs
            
            # Calculate overall progress
            total_progress = sum(lab['progress'] for lab in lab_data.values())
            overall_progress = round(total_progress / total_labs, 1) if total_labs > 0 else 0
            
            # Calculate hours
            total_hours = sum(lab.get('estimated_hours', 0) for lab in lab_data.values())
            completed_hours = sum(lab.get('completed_hours', 0) for lab in lab_data.values())
            
            # Count by category
            categories = {}
            for lab in lab_data.values():
                category = lab.get('category', 'General')
                if category not in categories:
                    categories[category] = {'total': 0, 'completed': 0}
                categories[category]['total'] += 1
                if lab['status'] == 'Complete':
                    categories[category]['completed'] += 1
            
            dashboard_data = {
                "total_labs": total_labs,
                "completed_labs": completed_labs,
                "in_progress_labs": in_progress_labs,
                "overall_progress": overall_progress,
                "total_hours": total_hours,
                "completed_hours": completed_hours,
                "categories": categories,
                "last_updated": datetime.now().isoformat(),
                "portfolio_url": "https://stevenloucks.tech",
                "github_profile": "https://github.com/sloucks623"
            }
            
            with open(dashboard_file, 'w') as f:
                json.dump(dashboard_data, f, indent=2)
            
            print(f"✅ Updated dashboard summary: {overall_progress}% overall progress")
            
        except Exception as e:
            print(f"❌ Error updating dashboard summary: {e}")
    
    def run_complete_integration(self):
        """Run the complete integration process"""
        print("🔥 Starting Complete Lab Integration...")
        print("=" * 50)
        
        # Step 1: Create all assessment files
        self.create_all_assessments()
        
        # Step 2: Update dashboard summary
        self.update_dashboard_summary()
        
        print("\n" + "=" * 50)
        print("✅ Complete Lab Integration finished!")
        print(f"📁 Assessment files created in: {self.assessments_dir}")
        print(f"📊 Dashboard data updated in: {self.data_dir}")
        print("\nNext steps:")
        print("1. Update task completion in assessment files (change [ ] to [x])")
        print("2. Run this script again to update dashboard progress")
        print("3. View updated dashboard on your portfolio website")

if __name__ == "__main__":
    integration = CompleteLabIntegration()
    integration.run_complete_integration()
