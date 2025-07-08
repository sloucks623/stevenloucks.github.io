/**
 * Lab Progress Dashboard
 * Dynamically loads and displays lab progress data for the portfolio
 */

class LabProgressDashboard {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.dashboardData = null;
        this.isLoading = false;
        
        if (!this.container) {
            console.error(`Container with ID '${containerId}' not found`);
            return;
        }
        
        this.init();
    }
    
    async init() {
        await this.loadDashboardData();
        this.render();
    }
    
    async loadDashboardData() {
        this.isLoading = true;
        this.showLoadingState();
        
        try {
            // Try to load local dashboard data first
            const response = await fetch('/data/lab-dashboard.json');
            
            if (response.ok) {
                this.dashboardData = await response.json();
                console.log('✅ Lab dashboard data loaded successfully');
            } else {
                throw new Error(`Failed to load dashboard data: ${response.status}`);
            }
        } catch (error) {
            console.warn('⚠️ Could not load lab dashboard data:', error.message);
            // Fallback to static data if needed
            this.dashboardData = this.getFallbackData();
        } finally {
            this.isLoading = false;
        }
    }
    
    getFallbackData() {
        return {
            summary: {
                total_labs: 4,
                completed_labs: 0,
                in_progress_labs: 2,
                not_started_labs: 2,
                overall_completion: 25,
                last_updated: new Date().toISOString()
            },
            labs: [
                {
                    repository: "lab-soc-automation",
                    name: "SOC Automation Lab",
                    description: "Automating alert triage using Shuffle, Elastic Stack, and Slack integrations",
                    completion_percentage: 45,
                    status: "In Progress",
                    priority: "High",
                    github_url: "https://github.com/sloucks623/lab-soc-automation",
                    components_total: 7,
                    components_completed: 3
                },
                {
                    repository: "lab-active-directory-1.0",
                    name: "Active Directory Lab 1.0",
                    description: "Set up a basic AD domain controller with DHCP, DNS, OUs, and users",
                    completion_percentage: 60,
                    status: "In Progress",
                    priority: "Medium",
                    github_url: "https://github.com/sloucks623/lab-active-directory-1.0",
                    components_total: 7,
                    components_completed: 4
                },
                {
                    repository: "lab-active-directory-2.0",
                    name: "Active Directory Lab 2.0",
                    description: "Expanded AD with GPOs, PowerShell automation, and segmentation",
                    completion_percentage: 0,
                    status: "Not Started",
                    priority: "Medium",
                    github_url: "https://github.com/sloucks623/lab-active-directory-2.0",
                    components_total: 7,
                    components_completed: 0
                },
                {
                    repository: "lab-detection-1.0",
                    name: "Detection Lab 1.0",
                    description: "Standalone detection-focused environment with EDR, IDS, logging pipeline, and MITRE ATT&CK mapping",
                    completion_percentage: 0,
                    status: "Not Started",
                    priority: "High",
                    github_url: "https://github.com/sloucks623/lab-detection-1.0",
                    components_total: 8,
                    components_completed: 0
                }
            ]
        };
    }
    
    showLoadingState() {
        this.container.innerHTML = `
            <div class="lab-progress-dashboard">
                <div class="lab-progress-loading">
                    Loading lab progress data...
                </div>
            </div>
        `;
    }
    
    showErrorState(error) {
        this.container.innerHTML = `
            <div class="lab-progress-dashboard">
                <div class="lab-progress-error">
                    <h4>Unable to load lab progress data</h4>
                    <p>${error}</p>
                    <small>Using fallback data for demonstration.</small>
                </div>
            </div>
        `;
    }
    
    getProgressClass(percentage) {
        if (percentage === 0) return 'progress-0';
        if (percentage < 30) return 'progress-low';
        if (percentage < 70) return 'progress-medium';
        return 'progress-high';
    }
    
    getStatusClass(status) {
        switch (status.toLowerCase()) {
            case 'complete': return 'status-complete';
            case 'in progress': return 'status-in-progress';
            default: return 'status-not-started';
        }
    }
    
    formatDate(isoString) {
        const date = new Date(isoString);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
    }
    
    render() {
        if (!this.dashboardData) {
            this.showErrorState('No dashboard data available');
            return;
        }
        
        const { summary, labs } = this.dashboardData;
        
        const dashboardHTML = `
            <div class="lab-progress-dashboard">
                <div class="progress-header">
                    <h3>🔬 Lab Progress Overview</h3>
                    <div class="overall-stats">
                        <div class="progress-stat">
                            <span class="stat-number">${summary.total_labs}</span>
                            <span class="stat-label">Total Labs</span>
                        </div>
                        <div class="progress-stat">
                            <span class="stat-number">${summary.completed_labs}</span>
                            <span class="stat-label">Complete</span>
                        </div>
                        <div class="progress-stat">
                            <span class="stat-number">${summary.in_progress_labs}</span>
                            <span class="stat-label">In Progress</span>
                        </div>
                        <div class="progress-stat">
                            <span class="stat-number">${summary.overall_completion}%</span>
                            <span class="stat-label">Overall</span>
                        </div>
                    </div>
                    <div class="overall-progress-bar">
                        <div class="overall-progress-fill ${this.getProgressClass(summary.overall_completion)}" 
                             style="width: ${summary.overall_completion}%"></div>
                    </div>
                </div>
                
                <div class="lab-progress-grid">
                    ${labs.map(lab => this.renderLabItem(lab)).join('')}
                </div>
                
                <div style="text-align: center; margin-top: 1rem; font-size: 0.8rem; color: #a0aec0;">
                    Last updated: ${this.formatDate(summary.last_updated)}
                </div>
            </div>
        `;
        
        this.container.innerHTML = dashboardHTML;
        
        // Add click handlers for lab items
        this.addEventHandlers();
    }
    
    renderLabItem(lab) {
        return `
            <div class="lab-progress-item" data-repo="${lab.repository}">
                <div class="lab-progress-header">
                    <h4 class="lab-progress-title">${lab.name}</h4>
                    <span class="lab-status-badge ${this.getStatusClass(lab.status)}">
                        ${lab.status}
                    </span>
                </div>
                
                <div class="lab-progress-bar">
                    <div class="lab-progress-fill ${this.getProgressClass(lab.completion_percentage)}" 
                         style="width: ${lab.completion_percentage}%"></div>
                </div>
                
                <div class="lab-progress-details">
                    <div class="components-info">
                        <span>📋 ${lab.components_completed}/${lab.components_total} components</span>
                    </div>
                    <span class="progress-percentage">${lab.completion_percentage}%</span>
                </div>
            </div>
        `;
    }
    
    addEventHandlers() {
        // Add click handlers to open GitHub repos
        const labItems = this.container.querySelectorAll('.lab-progress-item');
        labItems.forEach(item => {
            item.addEventListener('click', () => {
                const repo = item.dataset.repo;
                const lab = this.dashboardData.labs.find(l => l.repository === repo);
                if (lab) {
                    window.open(lab.github_url, '_blank');
                }
            });
            
            // Add hover cursor
            item.style.cursor = 'pointer';
        });
    }
    
    // Public method to refresh data
    async refresh() {
        await this.loadDashboardData();
        this.render();
    }
    
    // Public method to get summary data
    getSummary() {
        return this.dashboardData ? this.dashboardData.summary : null;
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Check if progress dashboard container exists
    const progressContainer = document.getElementById('lab-progress-dashboard');
    if (progressContainer) {
        window.labProgressDashboard = new LabProgressDashboard('lab-progress-dashboard');
    }
});

// Export for manual initialization if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LabProgressDashboard;
}
