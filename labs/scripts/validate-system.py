#!/usr/bin/env python3
"""
System Validation - Tests the complete lab progress tracking system
"""

import json
import os
from pathlib import Path

def validate_system():
    """Validate all system components"""
    print("🔍 Validating Lab Progress Tracking System...")
    print("=" * 50)
    
    portfolio_path = Path(__file__).parent.parent
    errors = []
    warnings = []
    
    # Check assessment files
    assessments_dir = portfolio_path / "lab-assessments"
    if not assessments_dir.exists():
        errors.append("Assessment directory missing")
    else:
        expected_files = [
            "soc-automation-progress.md",
            "lab-active-directory-1.0-progress.md", 
            "lab-active-directory-2.0-progress.md",
            "lab-detection-1.0-progress.md",
            "lab-soc-helpdesk-progress.md"
        ]
        
        for file in expected_files:
            if not (assessments_dir / file).exists():
                warnings.append(f"Missing assessment file: {file}")
            else:
                print(f"✅ Found assessment file: {file}")
    
    # Check data files
    data_dir = portfolio_path / "data"
    if not data_dir.exists():
        errors.append("Data directory missing")
    else:
        # Check lab-status.json
        lab_status_file = data_dir / "lab-status.json"
        if not lab_status_file.exists():
            errors.append("lab-status.json missing")
        else:
            try:
                with open(lab_status_file, 'r') as f:
                    lab_data = json.load(f)
                print(f"✅ lab-status.json valid ({len(lab_data)} labs)")
                
                # Validate data structure
                for lab_id, lab in lab_data.items():
                    required_fields = ['name', 'progress', 'status', 'category']
                    for field in required_fields:
                        if field not in lab:
                            warnings.append(f"Lab {lab_id} missing {field}")
                
            except json.JSONDecodeError:
                errors.append("lab-status.json invalid JSON")
        
        # Check dashboard-summary.json
        dashboard_file = data_dir / "dashboard-summary.json"
        if not dashboard_file.exists():
            errors.append("dashboard-summary.json missing")
        else:
            try:
                with open(dashboard_file, 'r') as f:
                    dashboard_data = json.load(f)
                print(f"✅ dashboard-summary.json valid")
                
                # Validate dashboard structure
                required_fields = ['total_labs', 'completed_labs', 'overall_progress']
                for field in required_fields:
                    if field not in dashboard_data:
                        warnings.append(f"Dashboard missing {field}")
                        
            except json.JSONDecodeError:
                errors.append("dashboard-summary.json invalid JSON")
    
    # Check scripts
    scripts_dir = portfolio_path / "scripts"
    if not scripts_dir.exists():
        errors.append("Scripts directory missing")
    else:
        expected_scripts = [
            "update-progress.py",
            "lab-progress-manager.bat",
            "complete-lab-integration.py"
        ]
        
        for script in expected_scripts:
            if not (scripts_dir / script).exists():
                warnings.append(f"Missing script: {script}")
            else:
                print(f"✅ Found script: {script}")
    
    # Check web integration
    js_file = portfolio_path / "js" / "lab-dashboard.js"
    if not js_file.exists():
        errors.append("Dashboard JavaScript missing")
    else:
        print("✅ Dashboard JavaScript found")
    
    css_file = portfolio_path / "css" / "lab-status-widget.css"
    if not css_file.exists():
        errors.append("Dashboard CSS missing")
    else:
        print("✅ Dashboard CSS found")
    
    # Check HTML integration
    index_file = portfolio_path / "index.html"
    if index_file.exists():
        with open(index_file, 'r') as f:
            content = f.read()
            if 'lab-dashboard.js' in content:
                print("✅ Dashboard integrated in index.html")
            else:
                warnings.append("Dashboard not integrated in index.html")
    
    # Calculate system health
    print("\n" + "=" * 50)
    print("📊 System Validation Results:")
    print("=" * 50)
    
    if errors:
        print("❌ ERRORS FOUND:")
        for error in errors:
            print(f"   - {error}")
    
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   - {warning}")
    
    if not errors and not warnings:
        print("✅ System fully validated - all components working correctly!")
        print("\n🎉 Your real-time lab progress tracking system is ready!")
        print("\nNext steps:")
        print("1. Update task completion in assessment files")
        print("2. Run lab-progress-manager.bat to update dashboard")
        print("3. View your portfolio to see real-time progress")
        
        # Show current progress
        try:
            with open(portfolio_path / "data" / "dashboard-summary.json", 'r') as f:
                summary = json.load(f)
            print(f"\n📈 Current Portfolio Status:")
            print(f"   - Overall Progress: {summary['overall_progress']}%")
            print(f"   - Completed Labs: {summary['completed_labs']}/{summary['total_labs']}")
            print(f"   - Last Updated: {summary['last_updated']}")
        except:
            pass
    
    elif not errors:
        print("✅ System operational with minor warnings")
        print("   Review warnings above for optimization opportunities")
    
    else:
        print("❌ System has critical errors")
        print("   Fix errors above before using the system")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    validate_system()
