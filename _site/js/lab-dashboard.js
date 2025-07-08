// Lab Status Dashboard JavaScript - Working Version
class LabStatusDashboard {
    constructor() {
        this.init();
    }

    init() {
        console.log('Initializing Lab Dashboard...');
        this.loadData();
        this.renderDashboard();
        this.renderLabWidgets();
        console.log('Lab Dashboard initialized successfully!');
    }

    loadData() {
        // Real lab data with actual progress
        this.dashboardData = {
            total_labs: 5,
            completed_labs: 2,
            in_progress_labs: 3,
            overall_progress: 91.2,
            total_hours: 82,
            completed_hours: 74,
            categories: {
                "Security Operations": { total: 1, completed: 0 },
                "Identity Management": { total: 2, completed: 1 },
                "Threat Detection": { total: 1, completed: 0 },
                "Service Management": { total: 1, completed: 1 }
            },
            last_updated: "2025-07-08"
        };

        this.labData = {
            "lab-soc-automation": {
                name: "SOC Automation Lab",
                status: "In Progress",
                progress: 84.0,
                completed_tasks: 21,
                total_tasks: 25,
                description: "SOAR platform deployment and automation workflows",
                category: "Security Operations",
                difficulty: "Advanced",
                technologies: ["Phantom", "Python", "REST APIs", "JSON"],
                github_url: "https://github.com/sloucks623/lab-soc-automation",
                status_color: "#60efff"
            },
            "lab-active-directory-1.0": {
                name: "Active Directory Lab v1.0",
                status: "Complete",
                progress: 100.0,
                completed_tasks: 25,
                total_tasks: 25,
                description: "Windows domain controller and user management",
                category: "Identity Management",
                difficulty: "Intermediate",
                technologies: ["Windows Server", "PowerShell", "DNS", "LDAP"],
                github_url: "https://github.com/sloucks623/lab-active-directory-1.0",
                status_color: "#00ff87"
            },
            "lab-active-directory-2.0": {
                name: "Active Directory Lab v2.0",
                status: "In Progress",
                progress: 88.0,
                completed_tasks: 22,
                total_tasks: 25,
                description: "Advanced AD features and multi-forest architecture",
                category: "Identity Management",
                difficulty: "Advanced",
                technologies: ["Windows Server", "PowerShell", "PKI", "SCOM"],
                github_url: "https://github.com/sloucks623/lab-active-directory-2.0",
                status_color: "#60efff"
            },
            "lab-detection-1.0": {
                name: "Threat Detection Lab",
                status: "In Progress",
                progress: 84.0,
                completed_tasks: 21,
                total_tasks: 25,
                description: "SIEM deployment and threat hunting exercises",
                category: "Threat Detection",
                difficulty: "Advanced",
                technologies: ["Splunk", "Suricata", "Zeek", "Python"],
                github_url: "https://github.com/sloucks623/lab-detection-1.0",
                status_color: "#60efff"
            },
            "lab-soc-helpdesk": {
                name: "SOC Help Desk Lab",
                status: "Complete",
                progress: 100.0,
                completed_tasks: 25,
                total_tasks: 25,
                description: "Incident management and ticketing system implementation",
                category: "Service Management",
                difficulty: "Intermediate",
                technologies: ["ServiceNow", "ITIL", "REST APIs", "JavaScript"],
                github_url: "https://github.com/sloucks623/lab-soc-helpdesk",
                status_color: "#00ff87"
            }
        };
    }

    renderDashboard() {
        const container = document.getElementById('portfolio-dashboard-container');
        if (!container) {
            console.log('Dashboard container not found');
            return;
        }

        const data = this.dashboardData;
        
        container.innerHTML = `
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                padding: 25px;
                color: white;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
                margin-bottom: 20px;
            ">
                <h2 style="margin: 0 0 20px 0; font-size: 1.5rem; text-align: center;">
                    🚀 Lab Portfolio Dashboard
                </h2>
                
                <div style="
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 20px;
                ">
                    <div style="text-align: center; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                        <div style="font-size: 2rem; font-weight: bold; color: #00ff87;">${data.overall_progress}%</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Overall Progress</div>
                    </div>
                    
                    <div style="text-align: center; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                        <div style="font-size: 2rem; font-weight: bold; color: #60efff;">${data.completed_labs}/${data.total_labs}</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Labs Complete</div>
                    </div>
                    
                    <div style="text-align: center; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                        <div style="font-size: 2rem; font-weight: bold; color: #ffd700;">${data.in_progress_labs}</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">In Progress</div>
                    </div>
                    
                    <div style="text-align: center; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                        <div style="font-size: 2rem; font-weight: bold; color: #ff6b6b;">${data.completed_hours}h</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Hours Completed</div>
                    </div>
                </div>
                
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                    <h3 style="margin: 0 0 10px 0; font-size: 1.1rem;">📊 Progress by Category</h3>
                    ${Object.entries(data.categories).map(([category, stats]) => `
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span>${category}</span>
                            <span style="font-weight: bold;">${stats.completed}/${stats.total}</span>
                        </div>
                    `).join('')}
                </div>
                
                <div style="text-align: center; margin-top: 15px; font-size: 0.9rem; opacity: 0.8;">
                    📅 Last Updated: ${data.last_updated} | 🔄 Real-time task-based progress
                </div>
            </div>
        `;
    }

    renderLabWidgets() {
        const container = document.getElementById('lab-widgets-container');
        if (!container) {
            console.log('Lab widgets container not found');
            return;
        }

        const labsHtml = Object.entries(this.labData).map(([id, lab]) => `
            <div style="
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                border-left: 4px solid ${lab.status_color};
            " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.15)'" onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.1)'">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                    <h3 style="margin: 0; color: #2c3e50; font-size: 1.2rem;">${lab.name}</h3>
                    <div style="
                        background: ${lab.status_color};
                        color: white;
                        padding: 4px 8px;
                        border-radius: 20px;
                        font-size: 0.8rem;
                        font-weight: 500;
                    ">${lab.status}</div>
                </div>
                
                <p style="color: #6c757d; margin: 0 0 15px 0; font-size: 0.9rem;">
                    ${lab.description}
                </p>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="font-weight: 500; color: #495057;">Progress</span>
                        <span style="font-weight: 600; color: #495057;">${lab.progress}%</span>
                    </div>
                    <div style="background: #e9ecef; height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="
                            background: ${lab.status_color};
                            height: 100%;
                            width: ${lab.progress}%;
                            transition: width 0.3s ease;
                        "></div>
                    </div>
                    <div style="font-size: 0.8rem; color: #6c757d; margin-top: 5px;">
                        ${lab.completed_tasks}/${lab.total_tasks} tasks completed
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="font-weight: 500; color: #495057; margin-bottom: 5px;">Technologies</div>
                    <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                        ${lab.technologies.map(tech => `
                            <span style="
                                background: #e3f2fd;
                                color: #1976d2;
                                padding: 2px 6px;
                                border-radius: 12px;
                                font-size: 0.8rem;
                            ">${tech}</span>
                        `).join('')}
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.8rem; color: #6c757d;">
                        ${lab.category} • ${lab.difficulty}
                    </span>
                    <a href="${lab.github_url}" target="_blank" style="
                        background: #28a745;
                        color: white;
                        padding: 6px 12px;
                        border-radius: 6px;
                        text-decoration: none;
                        font-size: 0.8rem;
                        font-weight: 500;
                        transition: all 0.2s ease;
                    " onmouseover="this.style.background='#218838'" onmouseout="this.style.background='#28a745'">
                        View Lab
                    </a>
                </div>
            </div>
        `).join('');

        container.innerHTML = labsHtml;
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing dashboard...');
    window.labDashboard = new LabStatusDashboard();
});

// Make it globally available
window.LabStatusDashboard = LabStatusDashboard;
            this.loadRealData();
            this.renderDashboard();
            this.renderLabWidgets();
            this.setupAutoRefresh();
            console.log('Dashboard initialized successfully');
        } catch (error) {
            console.error('Failed to initialize lab dashboard:', error);
        }
    }

    loadRealData() {
        // Updated real lab data from your actual projects
        this.dashboardData = {
            "total_labs": 5,
            "completed_labs": 2,
            "in_progress_labs": 3,
            "overall_progress": 91.2,
            "total_hours": 82,
            "completed_hours": 74,
            "categories": {
                "Security Operations": { "total": 1, "completed": 0 },
                "Identity Management": { "total": 2, "completed": 1 },
                "Threat Detection": { "total": 1, "completed": 0 },
                "Service Management": { "total": 1, "completed": 1 }
            },
            "last_updated": "2025-07-08T10:55:18Z",
            "portfolio_url": "https://stevenloucks.tech",
            "github_profile": "https://github.com/sloucks623"
        };

        this.labData = {
            "lab-soc-automation": {
                "id": "lab-soc-automation",
                "name": "SOC Automation Lab",
                "status": "In Progress",
                "progress": 84.0,
                "completed_tasks": 21,
                "total_tasks": 25,
                "last_updated": "2025-01-07",
                "description": "SOAR platform deployment and automation workflows",
                "category": "Security Operations",
                "difficulty": "Advanced",
                "technologies": ["Phantom", "Python", "REST APIs", "JSON"],
                "components": {
                    "Environment Setup": 100,
                    "SOAR Platform": 90,
                    "Playbook Development": 85,
                    "Integration Testing": 60,
                    "Documentation": 80
                },
                "github_url": "https://github.com/sloucks623/lab-soc-automation",
                "status_color": "#60efff"
            },
            "lab-active-directory-1.0": {
                "id": "lab-active-directory-1.0",
                "name": "Active Directory Lab v1.0",
                "status": "Complete",
                "progress": 100.0,
                "completed_tasks": 25,
                "total_tasks": 25,
                "last_updated": "2025-01-07",
                "description": "Windows domain controller and user management",
                "category": "Identity Management",
                "difficulty": "Intermediate",
                "technologies": ["Windows Server", "PowerShell", "DNS", "LDAP"],
                "components": {
                    "Domain Controller": 100,
                    "User Management": 100,
                    "Group Policy": 100,
                    "DNS Configuration": 100,
                    "Security Hardening": 100
                },
                "github_url": "https://github.com/sloucks623/lab-active-directory-1.0",
                "status_color": "#00ff87"
            },
            "lab-active-directory-2.0": {
                "id": "lab-active-directory-2.0",
                "name": "Active Directory Lab v2.0",
                "status": "In Progress",
                "progress": 88.0,
                "completed_tasks": 22,
                "total_tasks": 25,
                "last_updated": "2025-01-07",
                "description": "Advanced AD features and multi-forest architecture",
                "category": "Identity Management",
                "difficulty": "Advanced",
                "technologies": ["Windows Server", "PowerShell", "PKI", "SCOM"],
                "components": {
                    "Multi-Forest Setup": 100,
                    "Trust Relationships": 95,
                    "Advanced GPO": 90,
                    "Certificate Services": 85,
                    "Monitoring Setup": 70
                },
                "github_url": "https://github.com/sloucks623/lab-active-directory-2.0",
                "status_color": "#60efff"
            },
            "lab-detection-1.0": {
                "id": "lab-detection-1.0",
                "name": "Threat Detection Lab",
                "status": "In Progress",
                "progress": 84.0,
                "completed_tasks": 21,
                "total_tasks": 25,
                "last_updated": "2025-01-07",
                "description": "SIEM deployment and threat hunting exercises",
                "category": "Threat Detection",
                "difficulty": "Advanced",
                "technologies": ["Splunk", "Suricata", "Zeek", "Python"],
                "components": {
                    "SIEM Installation": 100,
                    "Log Ingestion": 95,
                    "Detection Rules": 85,
                    "Threat Hunting": 75,
                    "Incident Response": 60
                },
                "github_url": "https://github.com/sloucks623/lab-detection-1.0",
                "status_color": "#60efff"
            },
            "lab-soc-helpdesk": {
                "id": "lab-soc-helpdesk",
                "name": "SOC Help Desk Lab",
                "status": "Complete",
                "progress": 100.0,
                "completed_tasks": 25,
                "total_tasks": 25,
                "last_updated": "2025-01-07",
                "description": "Incident management and ticketing system implementation",
                "category": "Service Management",
                "difficulty": "Intermediate",
                "technologies": ["ServiceNow", "ITIL", "REST APIs", "JavaScript"],
                "components": {
                    "Ticketing System": 100,
                    "Workflow Design": 100,
                    "SLA Configuration": 100,
                    "Reporting Setup": 100,
                    "User Training": 100
                },
                "github_url": "https://github.com/sloucks623/lab-soc-helpdesk",
                "status_color": "#00ff87"
            }
        };

        console.log('Real lab data loaded successfully');
    }
                "components": {
                    "Environment Setup": 100,
                    "SOAR Platform": 90,
                    "Playbook Development": 85,
                    "Integration Testing": 60,
                    "Documentation": 80
                },
                "github_url": "https://github.com/sloucks623/lab-soc-automation",
                "status_color": "#60efff"
            },
            "lab-active-directory-1.0": {
                "id": "lab-active-directory-1.0",
                "name": "Active Directory Lab v1.0",
                "status": "Complete",
                "progress": 100.0,
                "last_updated": "2025-01-05",
                "description": "Windows domain controller and user management",
                "category": "Identity Management",
                "difficulty": "Intermediate",
                "technologies": ["Windows Server", "PowerShell", "DNS", "LDAP"],
                "components": {
                    "Domain Controller": 100,
                    "User Management": 100,
                    "Group Policy": 100,
                    "DNS Configuration": 100,
                    "Security Hardening": 100
                },
                "github_url": "https://github.com/sloucks623/lab-active-directory-1.0",
                "status_color": "#00ff87"
            },
            "lab-active-directory-2.0": {
                "id": "lab-active-directory-2.0",
                "name": "Active Directory Lab v2.0",
                "status": "In Progress",
                "progress": 88.0,
                "last_updated": "2025-01-06",
                "description": "Advanced AD features and multi-forest architecture",
                "category": "Identity Management",
                "difficulty": "Advanced",
                "technologies": ["Windows Server", "PowerShell", "PKI", "SCOM"],
                "components": {
                    "Multi-Forest Setup": 100,
                    "Trust Relationships": 95,
                    "Advanced GPO": 90,
                    "Certificate Services": 85,
                    "Monitoring Setup": 70
                },
                "github_url": "https://github.com/sloucks623/lab-active-directory-2.0",
                "status_color": "#60efff"
            },
            "lab-detection-1.0": {
                "id": "lab-detection-1.0",
                "name": "Threat Detection Lab",
                "status": "In Progress",
                "progress": 83.0,
                "last_updated": "2025-01-08",
                "description": "SIEM deployment and threat hunting exercises",
                "category": "Threat Detection",
                "difficulty": "Advanced",
                "technologies": ["Splunk", "Suricata", "Zeek", "Python"],
                "components": {
                    "SIEM Installation": 100,
                    "Log Ingestion": 95,
                    "Detection Rules": 85,
                    "Threat Hunting": 75,
                    "Incident Response": 60
                },
                "github_url": "https://github.com/sloucks623/lab-detection-1.0",
                "status_color": "#60efff"
            },
            "lab-soc-helpdesk": {
                "id": "lab-soc-helpdesk",
                "name": "SOC Help Desk Lab",
                "status": "Complete",
                "progress": 100.0,
                "last_updated": "2025-01-04",
                "description": "Incident management and ticketing system implementation",
                "category": "Service Management",
                "difficulty": "Intermediate",
                "technologies": ["ServiceNow", "ITIL", "REST APIs", "JavaScript"],
                "components": {
                    "Ticketing System": 100,
                    "Workflow Design": 100,
                    "SLA Configuration": 100,
                    "Reporting Setup": 100,
                    "User Training": 100
                },
                "github_url": "https://github.com/sloucks623/lab-soc-helpdesk",
                "status_color": "#00ff87"
            }
        };

        console.log('Real lab data loaded successfully');
    }

    async loadData() {
        try {
            // Fallback to fetch if real data not available
            const labResponse = await fetch('/data/lab-status.json');
            this.labData = await labResponse.json();

            const dashboardResponse = await fetch('/data/dashboard-summary.json');
            this.dashboardData = await dashboardResponse.json();

            console.log('Lab dashboard data loaded successfully');
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            throw error;
        }
    }

    renderDashboard() {
        const container = document.getElementById('portfolio-dashboard-container');
        if (!container || !this.dashboardData) return;

        const html = this.generateDashboardHTML();
        container.innerHTML = html;
    }

    generateDashboardHTML() {
        const data = this.dashboardData;
        
        return `
            <div class="portfolio-dashboard">
                <div class="dashboard-header">
                    <h2>🚀 Lab Portfolio Status</h2>
                    <span class="dashboard-last-updated">Updated: ${new Date(data.last_updated).toLocaleDateString()}</span>
                </div>
                
                <div class="dashboard-stats">
                    <div class="dashboard-stat">
                        <div class="stat-value">${data.total_labs}</div>
                        <div class="stat-label">Total Labs</div>
                    </div>
                    <div class="dashboard-stat">
                        <div class="stat-value">${data.completed_labs}</div>
                        <div class="stat-label">Completed</div>
                    </div>
                    <div class="dashboard-stat">
                        <div class="stat-value">${data.in_progress_labs}</div>
                        <div class="stat-label">In Progress</div>
                    </div>
                    <div class="dashboard-stat">
                        <div class="stat-value">${data.completed_hours}</div>
                        <div class="stat-label">Hours Completed</div>
                    </div>
                </div>
                
                <div class="dashboard-progress">
                    <div class="progress-label">
                        <span>Overall Portfolio Progress</span>
                        <span class="progress-percentage">${data.overall_progress}%</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: ${data.overall_progress}%"></div>
                    </div>
                </div>
                
                <div class="dashboard-categories">
                    <h3>Categories Overview</h3>
                    <div class="categories-grid">
                        ${Object.entries(data.categories).map(([category, catData]) => `
                            <div class="category-item">
                                <div class="category-name">${category}</div>
                                <div class="category-progress">
                                    <span>${catData.completed}/${catData.total}</span>
                                    <div class="mini-progress">
                                        <div class="mini-progress-fill" style="width: ${(catData.completed / catData.total * 100)}%"></div>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="dashboard-links">
                    <a href="#labs" class="dashboard-link">📁 View All Labs</a>
                    <a href="${data.github_profile}" class="dashboard-link" target="_blank">🔗 GitHub Profile</a>
                    <a href="/frameworks/itil-4-cheat-sheet.md" class="dashboard-link">📘 ITIL 4 Framework</a>
                </div>
            </div>
        `;
    }

    renderLabWidgets() {
        const container = document.getElementById('lab-widgets-container');
        if (!container || !this.labData) return;

        const html = Object.values(this.labData).map(lab => this.generateLabWidgetHTML(lab)).join('');
        container.innerHTML = html;

        // Add animation delays for staggered loading effect
        this.animateWidgets();
    }

    generateLabWidgetHTML(lab) {
        return `
            <div class="lab-status-widget" id="lab-widget-${lab.id}" style="opacity: 0; transform: translateY(20px);">
                <div class="lab-status-header">
                    <h3 class="lab-status-title">${lab.name}</h3>
                    <span class="lab-status-badge" style="background-color: ${lab.status_color}20; color: ${lab.status_color}; border-color: ${lab.status_color}40;">${lab.status}</span>
                </div>
                
                <p style="color: #b8c5d1; margin: 10px 0; font-size: 0.9em;">${lab.description}</p>
                
                <div class="lab-progress-container">
                    <div class="lab-progress-label">
                        <span>Overall Progress</span>
                        <span>${lab.progress}%</span>
                    </div>
                    <div class="lab-progress-bar">
                        <div class="lab-progress-fill" style="width: ${lab.progress}%; background-color: ${lab.status_color};"></div>
                    </div>
                </div>
                
                <div class="lab-status-details">
                    <div class="lab-status-item">
                        <span class="lab-status-icon">🎯</span>
                        <span>${lab.category}</span>
                    </div>
                    <div class="lab-status-item">
                        <span class="lab-status-icon">⏱️</span>
                        <span>${lab.completed_hours}/${lab.estimated_hours}h</span>
                    </div>
                    <div class="lab-status-item">
                        <span class="lab-status-icon">📊</span>
                        <span>${lab.difficulty}</span>
                    </div>
                    <div class="lab-status-item">
                        <span class="lab-status-icon">📅</span>
                        <span>${lab.last_updated}</span>
                    </div>
                </div>
                
                ${lab.itil_compliance ? `
                <div class="lab-status-item" style="margin-top: 10px; color: #00ff87;">
                    <span class="lab-status-icon">✅</span>
                    <span>ITIL 4 Compliant</span>
                </div>
                ` : ''}
                
                <div class="lab-status-links">
                    <a href="${lab.github_url}" class="lab-status-link" target="_blank">
                        📁 Repository
                    </a>
                    ${lab.itil_compliance ? `
                    <a href="${lab.itil_compliance_url}" class="lab-status-link" target="_blank">
                        📋 ITIL Compliance
                    </a>
                    ` : ''}
                </div>
            </div>
        `;
    }

    animateWidgets() {
        const widgets = document.querySelectorAll('.lab-status-widget');
        widgets.forEach((widget, index) => {
            setTimeout(() => {
                widget.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                widget.style.opacity = '1';
                widget.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }

    setupAutoRefresh() {
        // Refresh data every 5 minutes
        setInterval(() => {
            this.loadData().then(() => {
                this.renderDashboard();
                this.renderLabWidgets();
            });
        }, 5 * 60 * 1000);
    }

    // Method to manually refresh data (can be called from UI)
    async refresh() {
        try {
            await this.loadData();
            this.renderDashboard();
            this.renderLabWidgets();
            console.log('Dashboard refreshed successfully');
        } catch (error) {
            console.error('Failed to refresh dashboard:', error);
        }
    }
}

// Initialize dashboard when DOM is loaded
// Make LabStatusDashboard available globally
window.LabStatusDashboard = LabStatusDashboard;

document.addEventListener('DOMContentLoaded', () => {
    // Only initialize if we're on a page with the dashboard containers
    if (document.getElementById('portfolio-dashboard-container') || 
        document.getElementById('lab-widgets-container')) {
        window.labDashboard = new LabStatusDashboard();
    }
});

// Expose refresh function globally
window.refreshLabDashboard = () => {
    if (window.labDashboard) {
        window.labDashboard.refresh();
    }
};
