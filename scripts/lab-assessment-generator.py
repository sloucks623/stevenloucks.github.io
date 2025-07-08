#!/usr/bin/env python3
"""
Lab Assessment Generator - Creates detailed checklists from lab tutorials
Uses ChatGPT API to analyze tutorials and generate structured assessments

Features:
- Analyzes lab tutorials/guides to extract components and steps
- Generates detailed checklists with sub-tasks
- Creates assessment templates for accurate progress tracking
- Integrates with existing lab dashboard system
- Supports automated progress updates
"""

import json
import os
import requests
from datetime import datetime
import argparse
from pathlib import Path

class LabAssessmentGenerator:
    def __init__(self, openai_api_key=None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.portfolio_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assessments_dir = os.path.join(self.portfolio_path, "lab-assessments")
        os.makedirs(self.assessments_dir, exist_ok=True)
        
    def analyze_lab_tutorial(self, tutorial_text, lab_name):
        """Use ChatGPT to analyze a lab tutorial and extract detailed components"""
        
        prompt = f"""
        Analyze this cybersecurity lab tutorial and extract a detailed component breakdown for progress tracking.

        Lab: {lab_name}
        Tutorial Content: {tutorial_text}

        Please provide a JSON response with this structure:
        {{
            "lab_info": {{
                "name": "Lab Name",
                "description": "Brief description",
                "estimated_hours": 10,
                "difficulty": "Beginner|Intermediate|Advanced",
                "category": "Security Operations|Identity Management|Threat Detection|etc"
            }},
            "phases": [
                {{
                    "phase_name": "Phase 1: Environment Setup",
                    "description": "Setting up the lab environment",
                    "estimated_hours": 2,
                    "components": [
                        {{
                            "component": "Virtual Machine Setup",
                            "description": "Create and configure VMs",
                            "tasks": [
                                "Download VM images",
                                "Configure VM specifications",
                                "Install operating systems",
                                "Configure network settings"
                            ],
                            "validation_criteria": [
                                "VMs can communicate",
                                "All required software installed",
                                "Network connectivity verified"
                            ]
                        }}
                    ]
                }}
            ],
            "learning_objectives": [
                "Objective 1",
                "Objective 2"
            ],
            "prerequisites": [
                "Prerequisite 1",
                "Prerequisite 2"
            ],
            "tools_technologies": [
                "Tool 1",
                "Tool 2"
            ]
        }}

        Focus on:
        1. Breaking down into logical phases/sections
        2. Identifying specific components within each phase
        3. Creating detailed task lists for each component
        4. Defining clear validation criteria for completion
        5. Realistic time estimates based on complexity
        6. Potential troubleshooting areas
        """

        if not self.openai_api_key:
            print("⚠️  No OpenAI API key provided. Creating template structure...")
            return self.create_template_structure(lab_name)

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4",
                    "messages": [
                        {"role": "system", "content": "You are a cybersecurity lab expert who creates detailed, accurate assessment breakdowns."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 3000
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Extract JSON from response
                try:
                    # Find JSON in the response
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    json_str = content[start:end]
                    return json.loads(json_str)
                except:
                    print("⚠️  Failed to parse ChatGPT response. Creating template...")
                    return self.create_template_structure(lab_name)
            else:
                print(f"⚠️  API request failed: {response.status_code}")
                return self.create_template_structure(lab_name)
                
        except Exception as e:
            print(f"⚠️  Error calling OpenAI API: {e}")
            return self.create_template_structure(lab_name)

    def create_template_structure(self, lab_name):
        """Create a template structure when API is not available"""
        return {
            "lab_info": {
                "name": lab_name,
                "description": f"Assessment template for {lab_name}",
                "estimated_hours": 10,
                "difficulty": "Intermediate",
                "category": "General"
            },
            "phases": [
                {
                    "phase_name": "Phase 1: Planning & Setup",
                    "description": "Initial planning and environment setup",
                    "estimated_hours": 2,
                    "components": [
                        {
                            "component": "Environment Setup",
                            "description": "Prepare lab environment",
                            "tasks": [
                                "Review lab requirements",
                                "Download necessary tools",
                                "Configure environment",
                                "Verify connectivity"
                            ],
                            "validation_criteria": [
                                "Environment is ready",
                                "All tools accessible"
                            ]
                        }
                    ]
                },
                {
                    "phase_name": "Phase 2: Implementation",
                    "description": "Core lab implementation",
                    "estimated_hours": 6,
                    "components": [
                        {
                            "component": "Core Implementation",
                            "description": "Implement main lab objectives",
                            "tasks": [
                                "Follow tutorial steps",
                                "Configure services",
                                "Test functionality",
                                "Troubleshoot issues"
                            ],
                            "validation_criteria": [
                                "Services are running",
                                "Functionality verified"
                            ]
                        }
                    ]
                },
                {
                    "phase_name": "Phase 3: Documentation & Testing",
                    "description": "Document findings and test completeness",
                    "estimated_hours": 2,
                    "components": [
                        {
                            "component": "Documentation",
                            "description": "Document the lab process and findings",
                            "tasks": [
                                "Document procedures",
                                "Record troubleshooting steps",
                                "Create summary report",
                                "Update lab status"
                            ],
                            "validation_criteria": [
                                "Documentation complete",
                                "Lab status updated"
                            ]
                        }
                    ]
                }
            ],
            "learning_objectives": [
                "Complete lab tutorial successfully",
                "Document process and findings",
                "Demonstrate practical skills"
            ],
            "prerequisites": [
                "Basic understanding of the topic",
                "Required software/tools available"
            ],
            "tools_technologies": [
                "To be determined based on tutorial"
            ]
        }

    def create_progress_tracker(self, assessment_data, lab_id):
        """Create a progress tracking file for the lab"""
        
        tracker = {
            "lab_id": lab_id,
            "lab_info": assessment_data["lab_info"],
            "created_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "overall_status": "Not Started",
            "overall_progress": 0,
            "phases": []
        }
        
        # Process each phase
        for phase in assessment_data["phases"]:
            phase_tracker = {
                "phase_name": phase["phase_name"],
                "description": phase["description"],
                "estimated_hours": phase["estimated_hours"],
                "status": "Not Started",
                "progress": 0,
                "started_date": None,
                "completed_date": None,
                "components": []
            }
            
            # Process each component
            for component in phase["components"]:
                component_tracker = {
                    "component": component["component"],
                    "description": component["description"],
                    "status": "Not Started",
                    "progress": 0,
                    "tasks": [],
                    "validation_criteria": [],
                    "notes": "",
                    "issues_encountered": [],
                    "solutions_found": [],
                    "time_spent": 0,
                    "started_date": None,
                    "completed_date": None
                }
                
                # Add tasks
                for task in component["tasks"]:
                    component_tracker["tasks"].append({
                        "task": task,
                        "completed": False,
                        "notes": "",
                        "completion_date": None
                    })
                
                # Add validation criteria
                for criteria in component["validation_criteria"]:
                    component_tracker["validation_criteria"].append({
                        "criteria": criteria,
                        "validated": False,
                        "notes": "",
                        "validation_date": None
                    })
                
                phase_tracker["components"].append(component_tracker)
            
            tracker["phases"].append(phase_tracker)
        
        # Add summary sections
        tracker["summary"] = {
            "key_learnings": [],
            "major_challenges": [],
            "solutions_developed": [],
            "skills_demonstrated": [],
            "improvement_areas": [],
            "next_steps": []
        }
        
        return tracker

    def save_assessment(self, assessment_data, lab_id):
        """Save the assessment template and progress tracker"""
        
        # Save assessment template
        template_path = os.path.join(self.assessments_dir, f"{lab_id}-template.json")
        with open(template_path, 'w') as f:
            json.dump(assessment_data, f, indent=2)
        
        # Create progress tracker
        tracker = self.create_progress_tracker(assessment_data, lab_id)
        tracker_path = os.path.join(self.assessments_dir, f"{lab_id}-progress.json")
        with open(tracker_path, 'w') as f:
            json.dump(tracker, f, indent=2)
        
        print(f"✅ Assessment created for {lab_id}")
        print(f"   Template: {template_path}")
        print(f"   Tracker:  {tracker_path}")
        
        return template_path, tracker_path

    def update_dashboard_data(self):
        """Update the main dashboard with real progress data"""
        
        # Load all progress trackers
        progress_files = [f for f in os.listdir(self.assessments_dir) if f.endswith('-progress.json')]
        
        lab_data = {}
        dashboard_summary = {
            "total_labs": 0,
            "completed_labs": 0,
            "in_progress_labs": 0,
            "not_started_labs": 0,
            "overall_progress": 0,
            "total_hours": 0,
            "completed_hours": 0,
            "categories": {},
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "portfolio_url": "https://stevenloucks.tech",
            "github_profile": "https://github.com/sloucks623"
        }
        
        total_progress = 0
        
        for progress_file in progress_files:
            with open(os.path.join(self.assessments_dir, progress_file), 'r') as f:
                progress = json.load(f)
            
            lab_id = progress["lab_id"]
            info = progress["lab_info"]
            
            # Calculate real progress
            total_tasks = 0
            completed_tasks = 0
            
            for phase in progress["phases"]:
                for component in phase["components"]:
                    total_tasks += len(component["tasks"])
                    completed_tasks += sum(1 for task in component["tasks"] if task["completed"])
            
            real_progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            # Determine status
            if real_progress == 0:
                status = "Not Started"
            elif real_progress == 100:
                status = "Complete"
            else:
                status = "In Progress"
            
            # Create lab entry
            lab_data[lab_id] = {
                "id": lab_id,
                "name": info["name"],
                "description": info["description"],
                "category": info["category"],
                "difficulty": info["difficulty"],
                "status": status,
                "progress": round(real_progress, 1),
                "estimated_hours": info["estimated_hours"],
                "completed_hours": progress.get("time_spent", 0),
                "last_updated": progress["last_updated"][:10],
                "status_color": "#00ff87" if status == "Complete" else "#60efff" if status == "In Progress" else "#805ad5",
                "components": {},
                "technologies": [],
                "itil_compliance": True,
                "github_url": f"https://github.com/sloucks623/{lab_id}",
                "itil_compliance_url": f"https://github.com/sloucks623/{lab_id}/blob/main/ITIL-4-COMPLIANCE.md"
            }
            
            # Add component progress
            for phase in progress["phases"]:
                for component in phase["components"]:
                    comp_total = len(component["tasks"])
                    comp_completed = sum(1 for task in component["tasks"] if task["completed"])
                    comp_progress = (comp_completed / comp_total * 100) if comp_total > 0 else 0
                    lab_data[lab_id]["components"][component["component"]] = round(comp_progress)
            
            # Update dashboard summary
            dashboard_summary["total_labs"] += 1
            if status == "Complete":
                dashboard_summary["completed_labs"] += 1
            elif status == "In Progress":
                dashboard_summary["in_progress_labs"] += 1
            else:
                dashboard_summary["not_started_labs"] += 1
            
            dashboard_summary["total_hours"] += info["estimated_hours"]
            dashboard_summary["completed_hours"] += progress.get("time_spent", 0)
            
            # Category tracking
            category = info["category"]
            if category not in dashboard_summary["categories"]:
                dashboard_summary["categories"][category] = {"total": 0, "completed": 0}
            dashboard_summary["categories"][category]["total"] += 1
            if status == "Complete":
                dashboard_summary["categories"][category]["completed"] += 1
            
            total_progress += real_progress
        
        if dashboard_summary["total_labs"] > 0:
            dashboard_summary["overall_progress"] = round(total_progress / dashboard_summary["total_labs"], 1)
        
        # Save updated data
        data_dir = os.path.join(self.portfolio_path, "data")
        os.makedirs(data_dir, exist_ok=True)
        
        with open(os.path.join(data_dir, "lab-status.json"), 'w') as f:
            json.dump(lab_data, f, indent=2)
        
        with open(os.path.join(data_dir, "dashboard-summary.json"), 'w') as f:
            json.dump(dashboard_summary, f, indent=2)
        
        print(f"✅ Dashboard updated with real progress data")
        print(f"   Total Labs: {dashboard_summary['total_labs']}")
        print(f"   Overall Progress: {dashboard_summary['overall_progress']}%")
        
        return lab_data, dashboard_summary

def main():
    parser = argparse.ArgumentParser(description="Lab Assessment Generator")
    parser.add_argument("--lab-name", required=True, help="Name of the lab")
    parser.add_argument("--tutorial-file", help="Path to tutorial file")
    parser.add_argument("--tutorial-url", help="URL to tutorial")
    parser.add_argument("--tutorial-text", help="Direct tutorial text")
    parser.add_argument("--api-key", help="OpenAI API key")
    parser.add_argument("--update-dashboard", action="store_true", help="Update dashboard with current progress")
    
    args = parser.parse_args()
    
    generator = LabAssessmentGenerator(args.api_key)
    
    if args.update_dashboard:
        generator.update_dashboard_data()
        return
    
    # Get tutorial content
    tutorial_text = ""
    if args.tutorial_file:
        with open(args.tutorial_file, 'r') as f:
            tutorial_text = f.read()
    elif args.tutorial_url:
        print(f"📥 Fetching tutorial from: {args.tutorial_url}")
        # Add URL fetching logic here
        tutorial_text = "Tutorial content from URL"
    elif args.tutorial_text:
        tutorial_text = args.tutorial_text
    else:
        print("⚠️  No tutorial content provided. Creating template structure...")
        tutorial_text = ""
    
    # Generate assessment
    lab_id = args.lab_name.lower().replace(" ", "-")
    assessment = generator.analyze_lab_tutorial(tutorial_text, args.lab_name)
    generator.save_assessment(assessment, lab_id)
    
    print(f"\n📋 Assessment created for '{args.lab_name}'")
    print(f"   Edit the progress tracker as you work through the lab")
    print(f"   Run with --update-dashboard to refresh the portfolio")

if __name__ == "__main__":
    main()
