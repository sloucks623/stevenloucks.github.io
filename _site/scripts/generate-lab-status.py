#!/usr/bin/env python3
"""
Lab Status Data Generator
Generates JSON data files for website lab status widgets and dashboard
"""

import json
import os
import requests
from datetime import datetime, timedelta
import random

# Lab configuration with realistic progress data
LAB_CONFIG = {
    "lab-soc-automation": {
        "name": "SOC Automation Lab",
        "description": "SOAR platform deployment and automation workflows",
        "category": "Security Operations",
        "difficulty": "Advanced",
        "estimated_hours": 16,
        "completed_hours": 14,
        "status": "In Progress",
        "last_updated": "2025-01-07",
        "components": {
            "Environment Setup": 100,
            "SOAR Platform": 90,
            "Playbook Development": 85,
            "Integration Testing": 60,
            "Documentation": 80
        },
        "technologies": ["Phantom", "Python", "REST APIs", "JSON"],
        "itil_compliance": True
    },
    "lab-active-directory-1.0": {
        "name": "Active Directory Lab v1.0",
        "description": "Windows domain controller and user management",
        "category": "Identity Management",
        "difficulty": "Intermediate",
        "estimated_hours": 12,
        "completed_hours": 12,
        "status": "Complete",
        "last_updated": "2025-01-05",
        "components": {
            "Domain Controller": 100,
            "User Management": 100,
            "Group Policy": 100,
            "DNS Configuration": 100,
            "Security Hardening": 100
        },
        "technologies": ["Windows Server", "PowerShell", "DNS", "LDAP"],
        "itil_compliance": True
    },
    "lab-active-directory-2.0": {
        "name": "Active Directory Lab v2.0",
        "description": "Advanced AD features and multi-forest architecture",
        "category": "Identity Management",
        "difficulty": "Advanced",
        "estimated_hours": 20,
        "completed_hours": 18,
        "status": "In Progress",
        "last_updated": "2025-01-06",
        "components": {
            "Multi-Forest Setup": 100,
            "Trust Relationships": 95,
            "Advanced GPO": 90,
            "Certificate Services": 85,
            "Monitoring Setup": 70
        },
        "technologies": ["Windows Server", "PowerShell", "PKI", "SCOM"],
        "itil_compliance": True
    },
    "lab-detection-1.0": {
        "name": "Threat Detection Lab",
        "description": "SIEM deployment and threat hunting exercises",
        "category": "Threat Detection",
        "difficulty": "Advanced",
        "estimated_hours": 24,
        "completed_hours": 20,
        "status": "In Progress",
        "last_updated": "2025-01-08",
        "components": {
            "SIEM Installation": 100,
            "Log Ingestion": 95,
            "Detection Rules": 85,
            "Threat Hunting": 75,
            "Incident Response": 60
        },
        "technologies": ["Splunk", "Suricata", "Zeek", "Python"],
        "itil_compliance": True
    },
    "lab-soc-helpdesk": {
        "name": "SOC Help Desk Lab",
        "description": "Incident management and ticketing system implementation",
        "category": "Service Management",
        "difficulty": "Intermediate",
        "estimated_hours": 10,
        "completed_hours": 10,
        "status": "Complete",
        "last_updated": "2025-01-04",
        "components": {
            "Ticketing System": 100,
            "Workflow Design": 100,
            "SLA Configuration": 100,
            "Reporting Setup": 100,
            "User Training": 100
        },
        "technologies": ["ServiceNow", "ITIL", "REST APIs", "JavaScript"],
        "itil_compliance": True
    }
}

def calculate_overall_progress(components):
    """Calculate overall progress from component progress"""
    if not components:
        return 0
    return sum(components.values()) / len(components)

def get_status_color(status, progress):
    """Get color code for status"""
    if status == "Complete":
        return "#00ff87"
    elif status == "In Progress":
        if progress >= 80:
            return "#60efff"
        elif progress >= 50:
            return "#ffd700"
        else:
            return "#ff6b6b"
    else:
        return "#888888"

def generate_lab_status_data():
    """Generate lab status data for website"""
    labs_data = {}
    
    for lab_id, config in LAB_CONFIG.items():
        overall_progress = calculate_overall_progress(config["components"])
        
        labs_data[lab_id] = {
            "id": lab_id,
            "name": config["name"],
            "description": config["description"],
            "category": config["category"],
            "difficulty": config["difficulty"],
            "status": config["status"],
            "progress": round(overall_progress, 1),
            "estimated_hours": config["estimated_hours"],
            "completed_hours": config["completed_hours"],
            "last_updated": config["last_updated"],
            "status_color": get_status_color(config["status"], overall_progress),
            "components": config["components"],
            "technologies": config["technologies"],
            "itil_compliance": config["itil_compliance"],
            "github_url": f"https://github.com/sloucks623/{lab_id}",
            "itil_compliance_url": f"https://github.com/sloucks623/{lab_id}/blob/main/ITIL-4-COMPLIANCE.md"
        }
    
    return labs_data

def generate_dashboard_summary(labs_data):
    """Generate dashboard summary data"""
    total_labs = len(labs_data)
    completed_labs = sum(1 for lab in labs_data.values() if lab["status"] == "Complete")
    in_progress_labs = sum(1 for lab in labs_data.values() if lab["status"] == "In Progress")
    
    total_hours = sum(lab["estimated_hours"] for lab in labs_data.values())
    completed_hours = sum(lab["completed_hours"] for lab in labs_data.values())
    
    overall_progress = (completed_hours / total_hours * 100) if total_hours > 0 else 0
    
    # Get categories
    categories = {}
    for lab in labs_data.values():
        cat = lab["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "completed": 0}
        categories[cat]["total"] += 1
        if lab["status"] == "Complete":
            categories[cat]["completed"] += 1
    
    return {
        "total_labs": total_labs,
        "completed_labs": completed_labs,
        "in_progress_labs": in_progress_labs,
        "overall_progress": round(overall_progress, 1),
        "total_hours": total_hours,
        "completed_hours": completed_hours,
        "categories": categories,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "portfolio_url": "https://stevenloucks.tech",
        "github_profile": "https://github.com/sloucks623"
    }

def save_data_files():
    """Save lab data and dashboard data to JSON files"""
    # Generate lab data
    labs_data = generate_lab_status_data()
    dashboard_data = generate_dashboard_summary(labs_data)
    
    # Create data directory if it doesn't exist
    data_dir = "c:\\Users\\New User\\stevenloucks.github.io\\data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Save individual lab data
    with open(os.path.join(data_dir, "lab-status.json"), "w") as f:
        json.dump(labs_data, f, indent=2)
    
    # Save dashboard summary
    with open(os.path.join(data_dir, "dashboard-summary.json"), "w") as f:
        json.dump(dashboard_data, f, indent=2)
    
    print(f"✅ Generated lab status data for {len(labs_data)} laboratories")
    print(f"✅ Overall portfolio progress: {dashboard_data['overall_progress']}%")
    print(f"✅ Data files saved to: {data_dir}")
    
    return labs_data, dashboard_data

if __name__ == "__main__":
    save_data_files()
