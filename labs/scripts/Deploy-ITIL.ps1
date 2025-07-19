# ITIL 4 Lab Documentation Automation Script
# Author: Steven Loucks
# Purpose: Automatically inject ITIL 4 reference materials into lab repositories
# Version: 1.0

param(
    [Parameter(Mandatory=$false)]
    [string]$LabPath = ".",
    
    [Parameter(Mandatory=$false)]
    [string]$TemplateSource = "c:\Users\New User\stevenloucks.github.io\templates",
    
    [Parameter(Mandatory=$false)]
    [switch]$Force = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$Verbose = $false
)

# Color coding for output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Main automation function
function Deploy-ITILReference {
    param(
        [string]$TargetPath,
        [string]$SourcePath
    )
    
    Write-ColorOutput "🚀 ITIL 4 Lab Documentation Deployment Starting..." "Cyan"
    Write-ColorOutput "Target: $TargetPath" "Yellow"
    Write-ColorOutput "Source: $SourcePath" "Yellow"
    
    # Check if target is a git repository
    $isGitRepo = Test-Path (Join-Path $TargetPath ".git")
    if ($isGitRepo) {
        Write-ColorOutput "✅ Git repository detected" "Green"
    } else {
        Write-ColorOutput "⚠️  No git repository found - continuing anyway" "Yellow"
    }
    
    # Create docs directory structure
    $docsPath = Join-Path $TargetPath "docs"
    $itilPath = Join-Path $docsPath "itil-reference"
    
    if (!(Test-Path $docsPath)) {
        New-Item -ItemType Directory -Path $docsPath -Force | Out-Null
        Write-ColorOutput "📁 Created docs directory" "Green"
    }
    
    if (!(Test-Path $itilPath)) {
        New-Item -ItemType Directory -Path $itilPath -Force | Out-Null
        Write-ColorOutput "📁 Created ITIL reference directory" "Green"
    }
    
    # Copy ITIL 4 cheat sheet
    $sourceCheatSheet = Join-Path $SourcePath "itil-4-cheat-sheet.md"
    $targetCheatSheet = Join-Path $itilPath "itil-4-reference.md"
    
    if (Test-Path $sourceCheatSheet) {
        Copy-Item $sourceCheatSheet $targetCheatSheet -Force
        Write-ColorOutput "📋 ITIL 4 cheat sheet deployed" "Green"
    } else {
        Write-ColorOutput "❌ Source cheat sheet not found: $sourceCheatSheet" "Red"
        return $false
    }
    
    # Create lab-specific ITIL integration
    Create-LabITILIntegration -LabPath $TargetPath
    
    # Create automation badge/widget
    Create-ITILWidget -LabPath $TargetPath
    
    # Update README if it exists
    Update-ReadmeWithITIL -LabPath $TargetPath
    
    Write-ColorOutput "🎯 ITIL 4 deployment completed successfully!" "Green"
    return $true
}

function Create-LabITILIntegration {
    param([string]$LabPath)
    
    $integrationContent = @"
# ITIL 4 Integration for This Lab

## Applied ITIL 4 Principles

### 🎯 Focus on Value
**How this lab demonstrates value:**
- [ ] Document the business/learning objective
- [ ] Identify stakeholders (you, instructor, future employers)
- [ ] Measure success criteria

### 🔄 Progress Iteratively
**Implementation approach:**
- [ ] Phase 1: Basic setup and configuration
- [ ] Phase 2: Advanced features and testing
- [ ] Phase 3: Documentation and optimization

### 👥 Collaborate and Promote Visibility
**Documentation standards:**
- [ ] Clear step-by-step procedures
- [ ] Screenshots and diagrams
- [ ] Troubleshooting section
- [ ] Lessons learned

### 🔧 Keep It Simple and Practical
**Practical application:**
- [ ] Real-world scenarios
- [ ] Production-ready configurations
- [ ] Industry best practices

## Lab Documentation Checklist

### Pre-Lab (Plan)
- [ ] Objective clearly defined
- [ ] Prerequisites identified
- [ ] Risk assessment completed
- [ ] Resources allocated

### During Lab (Design & Transition)
- [ ] Step-by-step documentation
- [ ] Screenshots captured
- [ ] Commands and outputs recorded
- [ ] Issues and resolutions noted

### Post-Lab (Deliver & Support)
- [ ] Results validated
- [ ] Documentation reviewed
- [ ] Lessons learned captured
- [ ] Next steps identified

### Continuous Improvement
- [ ] Metrics collected
- [ ] Feedback gathered
- [ ] Process optimized
- [ ] Knowledge shared

---

**Reference**: See [ITIL 4 Complete Reference](./itil-reference/itil-4-reference.md) for detailed guidance.

**Lab Date**: $(Get-Date -Format "yyyy-MM-dd")  
**Student**: Steven Loucks - WGU BSCSIA Program
"@

    $integrationPath = Join-Path $LabPath "docs\ITIL-INTEGRATION.md"
    Set-Content -Path $integrationPath -Value $integrationContent -Encoding UTF8
    Write-ColorOutput "🔗 ITIL integration guide created" "Green"
}

function Create-ITILWidget {
    param([string]$LabPath)
    
    $widgetContent = @"
<!-- ITIL 4 Reference Widget -->
<div style="border: 2px solid #007acc; padding: 15px; margin: 20px 0; background-color: #f0f8ff; border-radius: 8px;">
    <h3 style="color: #007acc; margin-top: 0;">🎯 ITIL 4 Professional Practice</h3>
    <p><strong>This lab demonstrates ITIL 4 service management principles in action.</strong></p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin: 10px 0;">
        <div style="background: white; padding: 10px; border-radius: 4px; border-left: 4px solid #28a745;">
            <strong>Focus on Value</strong><br>
            <small>Clear objectives & outcomes</small>
        </div>
        <div style="background: white; padding: 10px; border-radius: 4px; border-left: 4px solid #ffc107;">
            <strong>Iterative Progress</strong><br>
            <small>Phased implementation</small>
        </div>
        <div style="background: white; padding: 10px; border-radius: 4px; border-left: 4px solid #17a2b8;">
            <strong>Collaborate</strong><br>
            <small>Transparent documentation</small>
        </div>
        <div style="background: white; padding: 10px; border-radius: 4px; border-left: 4px solid #6f42c1;">
            <strong>Continuous Improvement</strong><br>
            <small>Metrics & optimization</small>
        </div>
    </div>
    <p style="margin-bottom: 0;">
        📚 <a href="./docs/itil-reference/itil-4-reference.md">View Complete ITIL 4 Reference</a> |
        🔗 <a href="./docs/ITIL-INTEGRATION.md">Lab ITIL Integration Guide</a>
    </p>
</div>
"@

    $widgetPath = Join-Path $LabPath "docs\itil-widget.html"
    Set-Content -Path $widgetPath -Value $widgetContent -Encoding UTF8
    Write-ColorOutput "🎨 ITIL widget created" "Green"
}

function Update-ReadmeWithITIL {
    param([string]$LabPath)
    
    $readmePath = Join-Path $LabPath "README.md"
    
    if (Test-Path $readmePath) {
        $currentContent = Get-Content $readmePath -Raw
        
        # Check if ITIL content already exists
        if ($currentContent -match "ITIL 4 Professional Practice") {
            Write-ColorOutput "📝 README already contains ITIL content - skipping update" "Yellow"
            return
        }
        
        # Add ITIL section after title
        $itilSection = @"

## 🎯 ITIL 4 Professional Practice Applied

This lab demonstrates professional service management practices aligned with ITIL 4 principles:

- **Focus on Value**: Clear learning objectives and measurable outcomes
- **Iterative Progress**: Phased implementation with feedback loops  
- **Collaboration**: Transparent documentation and knowledge sharing
- **Holistic Thinking**: End-to-end process consideration
- **Continuous Improvement**: Metrics collection and optimization

📚 **[Complete ITIL 4 Reference Guide](./docs/itil-reference/itil-4-reference.md)**  
🔗 **[Lab ITIL Integration Checklist](./docs/ITIL-INTEGRATION.md)**

---
"@

        # Insert after the first heading
        $updatedContent = $currentContent -replace '(#[^#\n]*\n)', "`$1$itilSection"
        Set-Content -Path $readmePath -Value $updatedContent -Encoding UTF8
        Write-ColorOutput "📝 README updated with ITIL content" "Green"
    } else {
        Write-ColorOutput "⚠️  No README.md found - consider creating one" "Yellow"
    }
}

function Show-Usage {
    Write-ColorOutput @"
🚀 ITIL 4 Lab Documentation Automation

USAGE:
    .\Deploy-ITIL.ps1 [-LabPath <path>] [-TemplateSource <path>] [-Force] [-Verbose]

PARAMETERS:
    -LabPath        : Target lab directory (default: current directory)
    -TemplateSource : Source directory for ITIL templates
    -Force          : Overwrite existing files
    -Verbose        : Show detailed output

EXAMPLES:
    .\Deploy-ITIL.ps1                                    # Deploy to current directory
    .\Deploy-ITIL.ps1 -LabPath "C:\Labs\ActiveDirectory" # Deploy to specific lab
    .\Deploy-ITIL.ps1 -Force                            # Overwrite existing files

WHAT THIS SCRIPT DOES:
✅ Creates docs/itil-reference/ directory structure
✅ Copies ITIL 4 cheat sheet and reference materials
✅ Creates lab-specific ITIL integration guide
✅ Generates professional HTML widget for documentation
✅ Updates README.md with ITIL 4 professional practice section
✅ Maintains git repository compatibility

"@ "Cyan"
}

# Main execution
if ($args -contains "-help" -or $args -contains "--help" -or $args -contains "/?") {
    Show-Usage
    exit 0
}

try {
    $result = Deploy-ITILReference -TargetPath $LabPath -SourcePath $TemplateSource
    
    if ($result) {
        Write-ColorOutput @"

🎉 SUCCESS! ITIL 4 documentation deployed successfully.

NEXT STEPS:
1. Review the generated documentation in the docs/ folder
2. Customize the ITIL integration guide for your specific lab
3. Include the ITIL widget in your lab documentation
4. Commit changes to your git repository

PROFESSIONAL TIP:
This automation demonstrates ITIL 4 'Optimize and Automate' principle in action!

"@ "Green"
    }
} catch {
    Write-ColorOutput "❌ Error: $($_.Exception.Message)" "Red"
    Write-ColorOutput "Run with -Verbose for detailed output" "Yellow"
}
