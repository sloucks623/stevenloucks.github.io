#!/usr/bin/env python3
"""
Real Progress Tracker - Updates dashboard with actual task completion data
Replaces estimated percentages with real progress based on completed tasks
"""

import json
import os
from datetime import datetime
import re

class RealProgressTracker:
    def __init__(self):
        self.portfolio_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assessments_dir = os.path.join(self.portfolio_path, "lab-assessments")
        self.data_dir = os.path.join(self.portfolio_path, "data")
        
        # Create directories if they don't exist
        os.makedirs(self.assessments_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
    def parse_progress_markdown(self, file_path):
        """Parse progress markdown file and extract real completion data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract lab information
            lab_info = self.extract_lab_info(content)
            
            # Parse phases and tasks
            phases = self.extract_phases(content)
            
            # Calculate real progress
            total_tasks = 0
            completed_tasks = 0
            
            for phase in phases:
                for task in phase['tasks']:
                    total_tasks += 1
                    if task['completed']:
                        completed_tasks += 1
            
            real_progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            return {
                'lab_info': lab_info,
                'phases': phases,
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'real_progress': round(real_progress, 1),
                'last_updated': datetime.now().strftime("%Y-%m-%d")
            }
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def extract_lab_info(self, content):
        """Extract lab information from markdown content"""
        info = {}
        
        # Extract name
        name_match = re.search(r'# Lab Progress Assessment - (.+)', content)
        info['name'] = name_match.group(1) if name_match else 'Unknown Lab'
        
        # Extract category, difficulty, hours
        category_match = re.search(r'\*\*Category\*\*: (.+)', content)
        info['category'] = category_match.group(1) if category_match else 'General'
        
        difficulty_match = re.search(r'\*\*Difficulty\*\*: (.+)', content)
        info['difficulty'] = difficulty_match.group(1) if difficulty_match else 'Intermediate'
        
        hours_match = re.search(r'\*\*Estimated Hours\*\*: (\d+)', content)
        info['estimated_hours'] = int(hours_match.group(1)) if hours_match else 10
        
        return info
    
    def extract_phases(self, content):
        """Extract phases and tasks from markdown content"""
        phases = []
        
        # Find all phase sections
        phase_pattern = r'### (.+?) \((\d+)% Complete\) (.+?)\n\*\*Component\*\*: (.+?)\n(.*?)(?=### |## |$)'
        phase_matches = re.findall(phase_pattern, content, re.DOTALL)
        
        for match in phase_matches:
            phase_name = match[0]
            phase_progress = int(match[1])
            phase_status = match[2]
            component_name = match[3]
            tasks_content = match[4]
            
            # Extract tasks
            tasks = self.extract_tasks(tasks_content)
            
            phases.append({
                'phase_name': phase_name,
                'progress': phase_progress,
                'status': '✅' if phase_progress == 100 else '🔄',
                'component_name': component_name,
                'tasks': tasks
            })
        
        return phases
    
    def extract_tasks(self, tasks_content):
        """Extract individual tasks from content"""
        tasks = []
        
        # Find task lines (both completed [x] and pending [ ])
        task_pattern = r'- \[([ x])\] (.+?) \((\d+) min\)'
        task_matches = re.findall(task_pattern, tasks_content)
        
        for match in task_matches:
            completed = match[0] == 'x'
            task_name = match[1]
            duration_min = int(match[2])
            
            tasks.append({
                'task_name': task_name,
                'completed': completed,
                'duration_minutes': duration_min,
                'status': 'Completed' if completed else 'Pending'
            })
        
        return tasks
    
    def update_lab_status_file(self, progress_data):
        """Update the lab-status.json file with real progress"""
        lab_status_file = os.path.join(self.data_dir, "lab-status.json")
        
        # Load existing data
        try:
            with open(lab_status_file, 'r') as f:
                lab_status = json.load(f)
        except FileNotFoundError:
            lab_status = {}
        
        # Update SOC Automation Lab data
        lab_id = "lab-soc-automation"
        
        if lab_id in lab_status:
            # Update with real progress
            lab_status[lab_id]['progress'] = progress_data['real_progress']
            lab_status[lab_id]['completed_tasks'] = progress_data['completed_tasks']
            lab_status[lab_id]['total_tasks'] = progress_data['total_tasks']
            lab_status[lab_id]['last_updated'] = progress_data['last_updated']
            lab_status[lab_id]['status'] = 'Complete' if progress_data['real_progress'] == 100 else 'In Progress'
            lab_status[lab_id]['status_color'] = '#00ff87' if progress_data['real_progress'] == 100 else '#60efff'
            
            # Update component progress based on phases
            components = {}
            for phase in progress_data['phases']:
                components[phase['component_name']] = phase['progress']
            lab_status[lab_id]['components'] = components
            
            print(f"✅ Updated {lab_id} with real progress: {progress_data['real_progress']}%")
        
        # Save updated data
        with open(lab_status_file, 'w') as f:
            json.dump(lab_status, f, indent=2)
    
    def update_dashboard_summary(self):
        """Update dashboard summary with real progress"""
        lab_status_file = os.path.join(self.data_dir, "lab-status.json")
        dashboard_file = os.path.join(self.data_dir, "dashboard-summary.json")
        
        # Load lab status data
        try:
            with open(lab_status_file, 'r') as f:
                lab_status = json.load(f)
        except FileNotFoundError:
            print("❌ lab-status.json not found")
            return
        
        # Calculate summary statistics
        total_labs = len(lab_status)
        completed_labs = len([lab for lab in lab_status.values() if lab['status'] == 'Complete'])
        in_progress_labs = len([lab for lab in lab_status.values() if lab['status'] == 'In Progress'])
        
        # Calculate overall progress
        total_progress = sum(lab['progress'] for lab in lab_status.values())
        overall_progress = round(total_progress / total_labs, 1) if total_labs > 0 else 0
        
        # Calculate hours
        total_hours = sum(lab.get('estimated_hours', 0) for lab in lab_status.values())
        completed_hours = sum(lab.get('completed_hours', 0) for lab in lab_status.values())
        
        # Category breakdown
        categories = {}
        for lab in lab_status.values():
            category = lab.get('category', 'General')
            if category not in categories:
                categories[category] = {'total': 0, 'completed': 0}
            categories[category]['total'] += 1
            if lab['status'] == 'Complete':
                categories[category]['completed'] += 1
        
        # Create dashboard summary
        dashboard_summary = {
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
        
        # Save dashboard summary
        with open(dashboard_file, 'w') as f:
            json.dump(dashboard_summary, f, indent=2)
        
        print(f"✅ Dashboard updated - Overall Progress: {overall_progress}%")
        print(f"   Completed Labs: {completed_labs}/{total_labs}")
        print(f"   Hours: {completed_hours}/{total_hours}")
    
    def process_all_assessments(self):
        """Process all markdown assessment files"""
        processed_count = 0
        
        # Look for markdown files in assessments directory
        for filename in os.listdir(self.assessments_dir):
            if filename.endswith('-progress.md'):
                file_path = os.path.join(self.assessments_dir, filename)
                print(f"📊 Processing {filename}...")
                
                progress_data = self.parse_progress_markdown(file_path)
                if progress_data:
                    self.update_lab_status_file(progress_data)
                    processed_count += 1
        
        if processed_count > 0:
            self.update_dashboard_summary()
            print(f"✅ Processed {processed_count} assessment files")
        else:
            print("⚠️  No progress files found to process")
    
    def create_example_assessment(self, lab_name):
        """Create an example assessment template"""
        template = f"""# Lab Progress Assessment - {lab_name}

## Lab Information
- **Name**: {lab_name}
- **Category**: General
- **Difficulty**: Intermediate  
- **Tutorial Source**: Custom implementation
- **Estimated Hours**: 10

## Progress Tracking

### Phase 1: Planning & Setup (0% Complete) ⏳
**Component**: Environment Setup
- [ ] Review lab requirements (15 min)
- [ ] Download necessary tools (30 min)
- [ ] Set up virtual environment (45 min)
- [ ] Configure network settings (20 min)

**Lessons Learned**: [Add notes as you work]
**Issues Overcome**: [Document challenges and solutions]

### Phase 2: Implementation (0% Complete) ⏳  
**Component**: Core Implementation
- [ ] Follow tutorial steps (120 min)
- [ ] Configure main services (90 min)
- [ ] Test basic functionality (30 min)
- [ ] Troubleshoot issues (60 min)

**Lessons Learned**: [Add notes as you work]
**Issues Overcome**: [Document challenges and solutions]

### Phase 3: Documentation (0% Complete) ⏳
**Component**: Project Documentation
- [ ] Document procedures (45 min)
- [ ] Create troubleshooting guide (30 min)
- [ ] Write summary report (30 min)
- [ ] Update lab status (15 min)

**Lessons Learned**: [Add notes as you work]
**Issues Overcome**: [Document challenges and solutions]

## Overall Progress Summary
- **Completed Tasks**: 0 out of 12 total tasks
- **Actual Progress**: 0% (0/12 tasks completed)
- **Time Spent**: 0 hours out of 10 estimated
- **Remaining Tasks**: 12 tasks (estimated 10 hours)

## Skills Demonstrated
- 🔄 [Add skills as you complete tasks]

## Key Accomplishments  
- 🔄 [Add accomplishments as you progress]

## Challenges Overcome
- 🔄 [Document challenges and solutions]

## Next Session Goals
1. [Add specific goals for next lab session]
"""
        
        filename = f"{lab_name.lower().replace(' ', '-')}-progress.md"
        file_path = os.path.join(self.assessments_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"✅ Created assessment template: {file_path}")
        return file_path

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Real Progress Tracker')
    parser.add_argument('command', choices=['update', 'create'], help='Command to execute')
    parser.add_argument('--lab-name', help='Lab name for creating new assessment')
    
    args = parser.parse_args()
    
    tracker = RealProgressTracker()
    
    if args.command == 'update':
        print("🔄 Updating dashboard with real progress data...")
        tracker.process_all_assessments()
        
    elif args.command == 'create':
        if not args.lab_name:
            print("❌ Lab name required for create command")
            return
        tracker.create_example_assessment(args.lab_name)
        print("💡 Edit the assessment file and run 'update' to refresh dashboard")

if __name__ == "__main__":
    main()
