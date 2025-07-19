#!/usr/bin/env python3
"""
Simple Progress Updater - Updates dashboard with real progress from assessment files
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

def update_progress_from_assessments():
    """Update lab progress based on assessment files"""
    
    # Get paths
    portfolio_path = Path(__file__).parent.parent
    assessments_dir = portfolio_path / "lab-assessments"
    data_dir = portfolio_path / "data"
    
    # Load current lab status
    lab_status_file = data_dir / "lab-status.json"
    try:
        with open(lab_status_file, 'r') as f:
            lab_status = json.load(f)
    except FileNotFoundError:
        print("❌ lab-status.json not found")
        return
    
    # Process each assessment file
    for assessment_file in assessments_dir.glob("*-progress.md"):
        lab_id = assessment_file.stem.replace("-progress", "")
        
        if lab_id not in lab_status:
            print(f"⚠️  Lab {lab_id} not found in lab-status.json")
            continue
            
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
            
            # Update lab data
            lab_status[lab_id]['progress'] = progress
            lab_status[lab_id]['completed_tasks'] = completed_tasks
            lab_status[lab_id]['total_tasks'] = total_tasks
            lab_status[lab_id]['last_updated'] = datetime.now().strftime("%Y-%m-%d")
            lab_status[lab_id]['status'] = 'Complete' if progress == 100 else 'In Progress'
            lab_status[lab_id]['status_color'] = '#00ff87' if progress == 100 else '#60efff'
            
            print(f"✅ Updated {lab_id}: {progress}% complete ({completed_tasks}/{total_tasks} tasks)")
            
        except Exception as e:
            print(f"❌ Error processing {assessment_file}: {e}")
    
    # Save updated lab status
    with open(lab_status_file, 'w') as f:
        json.dump(lab_status, f, indent=2)
    
    # Update dashboard summary
    total_labs = len(lab_status)
    completed_labs = sum(1 for lab in lab_status.values() if lab['status'] == 'Complete')
    in_progress_labs = total_labs - completed_labs
    
    # Calculate overall progress
    total_progress = sum(lab['progress'] for lab in lab_status.values())
    overall_progress = round(total_progress / total_labs, 1) if total_labs > 0 else 0
    
    # Calculate hours
    total_hours = sum(lab.get('estimated_hours', 0) for lab in lab_status.values())
    completed_hours = sum(lab.get('completed_hours', 0) for lab in lab_status.values())
    
    # Count by category
    categories = {}
    for lab in lab_status.values():
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
    
    dashboard_file = data_dir / "dashboard-summary.json"
    with open(dashboard_file, 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    print(f"✅ Updated dashboard summary: {overall_progress}% overall progress")
    print(f"📊 {completed_labs}/{total_labs} labs completed")

if __name__ == "__main__":
    print("🔄 Updating dashboard with real progress data...")
    update_progress_from_assessments()
    print("✅ Dashboard update complete!")
