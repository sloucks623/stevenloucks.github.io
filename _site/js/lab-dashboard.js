// Lab Status Dashboard JavaScript - Cleaned Version
class LabStatusDashboard {
    constructor() {
        this.init();
    }

    init() {
        try {
            this.loadData();
            this.renderDashboard();
            this.renderLabWidgets();
            console.log('Lab Dashboard initialized successfully!');
        } catch (error) {
            this.showError('Failed to initialize dashboard.');
            console.error('Dashboard initialization error:', error);
        }
    }

    loadData() {
        // Hardcoded real lab data
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
            this.showError('Dashboard container not found.');
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
            this.showError('Lab widgets container not found.');
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
                margin-bottom: 10px;
            " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.15)'" onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.1)'">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                    <h3 style="margin: 0; color: #2c3e50; font-size: 1.2rem;">${lab.name}</h3>
                    <div style="
                        background: ${lab.status_color};
                        color: white;
                        padding: 4px 8px;
                        border-radius: 20px;
                        font-size: 0.8rem;
                        font-weight: 500;">
                        ${lab.status}
                    </div>
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
                                font-size: 0.8rem;">
                                ${tech}
                            </span>
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
                        transition: all 0.2s ease;"
                        onmouseover="this.style.background='#218838'" onmouseout="this.style.background='#28a745'">
                        View Lab
                    </a>
                </div>
            </div>
        `).join('');
        container.innerHTML = labsHtml;
    }

    showError(message) {
        const container = document.getElementById('portfolio-dashboard-container');
        if (container) {
            container.innerHTML = `<div style="color: #ff6b6b; font-weight: bold; padding: 1rem; text-align: center;">${message}</div>`;
        }
    }
}

// Make LabStatusDashboard available globally
window.LabStatusDashboard = LabStatusDashboard;

// Only initialize if dashboard containers exist
if (document.getElementById('portfolio-dashboard-container') || document.getElementById('lab-widgets-container')) {
    window.labDashboard = new LabStatusDashboard();
}
