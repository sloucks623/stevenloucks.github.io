#!/usr/bin/env python3
"""
Intelligent Lab Progress Tracker with ChatGPT Integration
Automatically analyzes lab tutorials and creates dynamic progress tracking

Features:
- Fetches tutorial content from URLs
- Uses ChatGPT to analyze and break down complex tutorials
- Generates detailed, component-based checklists
- Creates real-time progress tracking
- Integrates with existing dashboard system
- Supports automated progress updates
"""

import json
import os
import requests
from datetime import datetime
import argparse
from pathlib import Path
import re
from urllib.parse import urlparse
import time
import yaml

class IntelligentLabTracker:
    def __init__(self, openai_api_key=None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.portfolio_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assessments_dir = os.path.join(self.portfolio_path, "lab-assessments")
        self.progress_dir = os.path.join(self.portfolio_path, "lab-progress")
        self.data_dir = os.path.join(self.portfolio_path, "data")
        
        # Create directories
        os.makedirs(self.assessments_dir, exist_ok=True)
        os.makedirs(self.progress_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
    def fetch_tutorial_content(self, url):
        """Fetch content from a tutorial URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Basic HTML content extraction (can be enhanced with BeautifulSoup)
            content = response.text
            
            # Remove HTML tags for text analysis
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
            content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
            content = re.sub(r'<[^>]+>', '', content)
            content = re.sub(r'\s+', ' ', content).strip()
            
            return content
            
        except Exception as e:
            print(f"⚠️  Error fetching tutorial content: {e}")
            return None

    def analyze_tutorial_with_chatgpt(self, content, lab_name, tutorial_url=None):
        """Use ChatGPT to analyze tutorial content and create detailed breakdown"""
        
        prompt = f"""
        Analyze this cybersecurity lab tutorial and create a comprehensive assessment breakdown for progress tracking.

        Lab: {lab_name}
        Tutorial URL: {tutorial_url or 'N/A'}
        
        Content: {content[:4000]}...  # Truncate for API limits

        Please provide a JSON response with this exact structure:
        {{
            "lab_info": {{
                "name": "{lab_name}",
                "description": "Brief description based on content",
                "estimated_hours": 8,
                "difficulty": "Beginner|Intermediate|Advanced",
                "category": "Identity Management|Network Security|Threat Detection|Security Operations|Compliance|etc",
                "tutorial_url": "{tutorial_url or ''}",
                "prerequisites": ["Prerequisite 1", "Prerequisite 2"],
                "learning_objectives": ["Objective 1", "Objective 2"]
            }},
            "phases": [
                {{
                    "phase_id": "phase_1",
                    "phase_name": "Phase 1: Environment Setup",
                    "description": "Setting up the lab environment",
                    "estimated_hours": 2,
                    "components": [
                        {{
                            "component_id": "vm_setup",
                            "component_name": "Virtual Machine Setup",
                            "description": "Create and configure VMs",
                            "estimated_minutes": 45,
                            "tasks": [
                                {{
                                    "task_id": "download_vm",
                                    "task_name": "Download VM images",
                                    "description": "Download required VM images",
                                    "estimated_minutes": 15,
                                    "validation_criteria": "VM images downloaded successfully"
                                }},
                                {{
                                    "task_id": "configure_vm",
                                    "task_name": "Configure VM specifications",
                                    "description": "Set RAM, CPU, storage specifications",
                                    "estimated_minutes": 10,
                                    "validation_criteria": "VM specifications configured correctly"
                                }}
                            ],
                            "validation_criteria": [
                                "VMs can communicate",
                                "All required software installed",
                                "Network connectivity verified"
                            ],
                            "troubleshooting_tips": [
                                "Common virtualization issues",
                                "Network connectivity problems"
                            ]
                        }}
                    ]
                }}
            ],
            "tools_technologies": ["Tool 1", "Tool 2"],
            "common_issues": [
                {{
                    "issue": "Common problem",
                    "solution": "How to resolve",
                    "prevention": "How to prevent"
                }}
            ]
        }}

        Requirements:
        1. Break down into logical phases (3-5 phases typical)
        2. Each phase should have 2-5 components
        3. Each component should have 2-8 specific tasks
        4. Include realistic time estimates
        5. Provide clear validation criteria
        6. Include troubleshooting tips
        7. Focus on measurable, trackable progress
        8. Consider ITIL service management principles where applicable
        """

        if not self.openai_api_key:
            print("⚠️  No OpenAI API key provided. Creating template structure...")
            return self.create_intelligent_template(lab_name, tutorial_url)

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
                        {"role": "system", "content": "You are a cybersecurity lab expert who creates detailed, accurate assessment breakdowns for tracking progress. Always respond with valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 4000
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
                    return self.create_intelligent_template(lab_name, tutorial_url)
            else:
                print(f"⚠️  API request failed: {response.status_code}")
                return self.create_intelligent_template(lab_name, tutorial_url)
                
        except Exception as e:
            print(f"⚠️  Error calling OpenAI API: {e}")
            return self.create_intelligent_template(lab_name, tutorial_url)

    def create_intelligent_template(self, lab_name, tutorial_url=None):
        """Create an intelligent template structure"""
        return {
            "lab_info": {
                "name": lab_name,
                "description": f"Intelligent assessment template for {lab_name}",
                "estimated_hours": 10,
                "difficulty": "Intermediate",
                "category": "General",
                "tutorial_url": tutorial_url or "",
                "prerequisites": ["Basic networking knowledge", "Virtual machine experience"],
                "learning_objectives": ["Complete lab successfully", "Document findings", "Troubleshoot issues"]
            },
            "phases": [
                {
                    "phase_id": "phase_1",
                    "phase_name": "Phase 1: Planning & Setup",
                    "description": "Initial planning and environment setup",
                    "estimated_hours": 2,
                    "components": [
                        {
                            "component_id": "planning",
                            "component_name": "Lab Planning",
                            "description": "Plan the lab approach and gather requirements",
                            "estimated_minutes": 30,
                            "tasks": [
                                {
                                    "task_id": "review_tutorial",
                                    "task_name": "Review Tutorial",
                                    "description": "Read through the entire tutorial",
                                    "estimated_minutes": 15,
                                    "validation_criteria": "Tutorial reviewed and understood"
                                },
                                {
                                    "task_id": "gather_resources",
                                    "task_name": "Gather Resources",
                                    "description": "Collect all necessary resources and tools",
                                    "estimated_minutes": 15,
                                    "validation_criteria": "All resources ready"
                                }
                            ],
                            "validation_criteria": ["Lab approach documented", "Resources identified"],
                            "troubleshooting_tips": ["Check system requirements", "Verify network access"]
                        }
                    ]
                }
            ],
            "tools_technologies": ["Virtual Machine", "Network Tools", "Security Tools"],
            "common_issues": [
                {
                    "issue": "Network connectivity problems",
                    "solution": "Check firewall settings and network configuration",
                    "prevention": "Test network setup before starting"
                }
            ]
        }

    def create_progress_tracker(self, assessment_data):
        """Create a progress tracker from assessment data"""
        lab_name = assessment_data['lab_info']['name']
        
        progress_data = {
            "lab_info": assessment_data['lab_info'],
            "progress_summary": {
                "overall_progress": 0,
                "completed_tasks": 0,
                "total_tasks": 0,
                "estimated_remaining_hours": assessment_data['lab_info']['estimated_hours'],
                "actual_hours_spent": 0,
                "started_date": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "status": "Not Started"
            },
            "phase_progress": [],
            "task_history": []
        }
        
        # Calculate total tasks and initialize progress
        total_tasks = 0
        for phase in assessment_data['phases']:
            phase_progress = {
                "phase_id": phase['phase_id'],
                "phase_name": phase['phase_name'],
                "progress": 0,
                "status": "Not Started",
                "started_date": None,
                "completed_date": None,
                "components": []
            }
            
            for component in phase['components']:
                component_progress = {
                    "component_id": component['component_id'],
                    "component_name": component['component_name'],
                    "progress": 0,
                    "status": "Not Started",
                    "started_date": None,
                    "completed_date": None,
                    "tasks": []
                }
                
                for task in component['tasks']:
                    task_progress = {
                        "task_id": task['task_id'],
                        "task_name": task['task_name'],
                        "status": "Not Started",
                        "completed_date": None,
                        "notes": "",
                        "time_spent_minutes": 0
                    }
                    component_progress['tasks'].append(task_progress)
                    total_tasks += 1
                
                phase_progress['components'].append(component_progress)
            
            progress_data['phase_progress'].append(phase_progress)
        
        progress_data['progress_summary']['total_tasks'] = total_tasks
        
        return progress_data

    def update_task_progress(self, lab_name, task_id, status, notes="", time_spent=0):
        """Update progress for a specific task"""
        progress_file = os.path.join(self.progress_dir, f"{lab_name.replace(' ', '_').lower()}_progress.json")
        
        if not os.path.exists(progress_file):
            print(f"⚠️  Progress file not found: {progress_file}")
            return False
        
        try:
            with open(progress_file, 'r') as f:
                progress_data = json.load(f)
            
            # Find and update the task
            task_found = False
            for phase in progress_data['phase_progress']:
                for component in phase['components']:
                    for task in component['tasks']:
                        if task['task_id'] == task_id:
                            task['status'] = status
                            task['notes'] = notes
                            task['time_spent_minutes'] = time_spent
                            if status == "Completed":
                                task['completed_date'] = datetime.now().isoformat()
                            task_found = True
                            break
                    if task_found:
                        break
                if task_found:
                    break
            
            if not task_found:
                print(f"⚠️  Task {task_id} not found")
                return False
            
            # Recalculate progress
            self.recalculate_progress(progress_data)
            
            # Save updated progress
            with open(progress_file, 'w') as f:
                json.dump(progress_data, f, indent=2)
            
            # Update dashboard
            self.update_dashboard_data()
            
            print(f"✅ Task {task_id} updated to {status}")
            return True
            
        except Exception as e:
            print(f"⚠️  Error updating task progress: {e}")
            return False

    def recalculate_progress(self, progress_data):
        """Recalculate overall progress based on completed tasks"""
        completed_tasks = 0
        total_tasks = 0
        total_time_spent = 0
        
        for phase in progress_data['phase_progress']:
            phase_completed = 0
            phase_total = 0
            
            for component in phase['components']:
                component_completed = 0
                component_total = 0
                
                for task in component['tasks']:
                    component_total += 1
                    total_tasks += 1
                    total_time_spent += task.get('time_spent_minutes', 0)
                    
                    if task['status'] == "Completed":
                        component_completed += 1
                        completed_tasks += 1
                
                # Update component progress
                if component_total > 0:
                    component['progress'] = (component_completed / component_total) * 100
                    if component['progress'] == 100:
                        component['status'] = "Completed"
                        if not component['completed_date']:
                            component['completed_date'] = datetime.now().isoformat()
                    elif component['progress'] > 0:
                        component['status'] = "In Progress"
                        if not component['started_date']:
                            component['started_date'] = datetime.now().isoformat()
                
                phase_completed += component_completed
                phase_total += component_total
            
            # Update phase progress
            if phase_total > 0:
                phase['progress'] = (phase_completed / phase_total) * 100
                if phase['progress'] == 100:
                    phase['status'] = "Completed"
                    if not phase['completed_date']:
                        phase['completed_date'] = datetime.now().isoformat()
                elif phase['progress'] > 0:
                    phase['status'] = "In Progress"
                    if not phase['started_date']:
                        phase['started_date'] = datetime.now().isoformat()
        
        # Update overall progress
        overall_progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        progress_data['progress_summary'].update({
            'overall_progress': round(overall_progress, 1),
            'completed_tasks': completed_tasks,
            'total_tasks': total_tasks,
            'actual_hours_spent': round(total_time_spent / 60, 2),
            'last_updated': datetime.now().isoformat()
        })
        
        # Update status
        if overall_progress == 100:
            progress_data['progress_summary']['status'] = "Completed"
        elif overall_progress > 0:
            progress_data['progress_summary']['status'] = "In Progress"
        else:
            progress_data['progress_summary']['status'] = "Not Started"

    def update_dashboard_data(self):
        """Update dashboard data with current progress"""
        try:
            # Load current dashboard data
            dashboard_file = os.path.join(self.data_dir, "dashboard-summary.json")
            if os.path.exists(dashboard_file):
                with open(dashboard_file, 'r') as f:
                    dashboard_data = json.load(f)
            else:
                dashboard_data = {"labs": [], "summary": {}}
            
            # Update with progress data
            progress_files = list(Path(self.progress_dir).glob("*_progress.json"))
            
            updated_labs = []
            for progress_file in progress_files:
                try:
                    with open(progress_file, 'r') as f:
                        progress_data = json.load(f)
                    
                    lab_summary = {
                        "name": progress_data['lab_info']['name'],
                        "description": progress_data['lab_info']['description'],
                        "category": progress_data['lab_info']['category'],
                        "progress": progress_data['progress_summary']['overall_progress'],
                        "status": progress_data['progress_summary']['status'],
                        "estimated_hours": progress_data['lab_info']['estimated_hours'],
                        "actual_hours": progress_data['progress_summary']['actual_hours_spent'],
                        "completed_tasks": progress_data['progress_summary']['completed_tasks'],
                        "total_tasks": progress_data['progress_summary']['total_tasks'],
                        "last_updated": progress_data['progress_summary']['last_updated']
                    }
                    
                    updated_labs.append(lab_summary)
                    
                except Exception as e:
                    print(f"⚠️  Error processing {progress_file}: {e}")
            
            # Update dashboard
            dashboard_data['labs'] = updated_labs
            dashboard_data['summary'] = {
                "total_labs": len(updated_labs),
                "completed_labs": len([lab for lab in updated_labs if lab['status'] == 'Completed']),
                "in_progress_labs": len([lab for lab in updated_labs if lab['status'] == 'In Progress']),
                "total_hours_spent": sum(lab['actual_hours'] for lab in updated_labs),
                "last_updated": datetime.now().isoformat()
            }
            
            # Save updated dashboard
            with open(dashboard_file, 'w') as f:
                json.dump(dashboard_data, f, indent=2)
            
            print("✅ Dashboard data updated")
            
        except Exception as e:
            print(f"⚠️  Error updating dashboard: {e}")

    def create_lab_from_url(self, lab_name, tutorial_url):
        """Create a complete lab assessment and progress tracker from a URL"""
        print(f"🔄 Creating lab assessment for: {lab_name}")
        print(f"📖 Tutorial URL: {tutorial_url}")
        
        # Fetch tutorial content
        print("📥 Fetching tutorial content...")
        content = self.fetch_tutorial_content(tutorial_url)
        if not content:
            print("⚠️  Failed to fetch tutorial content. Using template.")
            content = f"Tutorial for {lab_name} - content not available"
        
        # Analyze with ChatGPT
        print("🤖 Analyzing with ChatGPT...")
        assessment_data = self.analyze_tutorial_with_chatgpt(content, lab_name, tutorial_url)
        
        # Save assessment
        assessment_file = os.path.join(self.assessments_dir, f"{lab_name.replace(' ', '_').lower()}_assessment.json")
        with open(assessment_file, 'w') as f:
            json.dump(assessment_data, f, indent=2)
        
        # Create progress tracker
        print("📊 Creating progress tracker...")
        progress_data = self.create_progress_tracker(assessment_data)
        
        # Save progress tracker
        progress_file = os.path.join(self.progress_dir, f"{lab_name.replace(' ', '_').lower()}_progress.json")
        with open(progress_file, 'w') as f:
            json.dump(progress_data, f, indent=2)
        
        # Update dashboard
        self.update_dashboard_data()
        
        print(f"✅ Lab assessment and progress tracker created!")
        print(f"📄 Assessment: {assessment_file}")
        print(f"📊 Progress: {progress_file}")
        
        return assessment_file, progress_file

    def list_tasks(self, lab_name):
        """List all tasks for a lab with their current status"""
        progress_file = os.path.join(self.progress_dir, f"{lab_name.replace(' ', '_').lower()}_progress.json")
        
        if not os.path.exists(progress_file):
            print(f"⚠️  Progress file not found for {lab_name}")
            return
        
        try:
            with open(progress_file, 'r') as f:
                progress_data = json.load(f)
            
            print(f"\n📋 Tasks for {lab_name}:")
            print(f"Overall Progress: {progress_data['progress_summary']['overall_progress']:.1f}%")
            print(f"Status: {progress_data['progress_summary']['status']}")
            print("-" * 60)
            
            for phase in progress_data['phase_progress']:
                print(f"\n🔶 {phase['phase_name']} ({phase['progress']:.1f}%)")
                for component in phase['components']:
                    print(f"  📦 {component['component_name']} ({component['progress']:.1f}%)")
                    for task in component['tasks']:
                        status_icon = "✅" if task['status'] == "Completed" else "🔄" if task['status'] == "In Progress" else "⏳"
                        print(f"    {status_icon} {task['task_name']} - {task['status']}")
                        if task['notes']:
                            print(f"        💬 {task['notes']}")
            
        except Exception as e:
            print(f"⚠️  Error listing tasks: {e}")

def main():
    parser = argparse.ArgumentParser(description='Intelligent Lab Progress Tracker')
    parser.add_argument('command', choices=['create', 'update', 'list', 'dashboard'], 
                       help='Command to execute')
    parser.add_argument('--lab-name', help='Lab name')
    parser.add_argument('--tutorial-url', help='Tutorial URL')
    parser.add_argument('--task-id', help='Task ID to update')
    parser.add_argument('--status', choices=['Not Started', 'In Progress', 'Completed'], 
                       help='Task status')
    parser.add_argument('--notes', help='Task notes')
    parser.add_argument('--time-spent', type=int, help='Time spent in minutes')
    
    args = parser.parse_args()
    
    tracker = IntelligentLabTracker()
    
    if args.command == 'create':
        if not args.lab_name or not args.tutorial_url:
            print("⚠️  Lab name and tutorial URL required for create command")
            return
        tracker.create_lab_from_url(args.lab_name, args.tutorial_url)
    
    elif args.command == 'update':
        if not args.lab_name or not args.task_id or not args.status:
            print("⚠️  Lab name, task ID, and status required for update command")
            return
        tracker.update_task_progress(args.lab_name, args.task_id, args.status, 
                                   args.notes or "", args.time_spent or 0)
    
    elif args.command == 'list':
        if not args.lab_name:
            print("⚠️  Lab name required for list command")
            return
        tracker.list_tasks(args.lab_name)
    
    elif args.command == 'dashboard':
        tracker.update_dashboard_data()
        print("✅ Dashboard updated")

if __name__ == "__main__":
    main()
