// POWERGRID Project Risk Predictor JavaScript

// Application data
const HISTORICAL_DATA = {
    "Substation": {"avg_cost_overrun": 35, "avg_timeline_overrun": 15},
    "Overhead Line": {"avg_cost_overrun": 25, "avg_timeline_overrun": 12},
    "Underground Cable": {"avg_cost_overrun": 55, "avg_timeline_overrun": 25}
};

const RISK_FACTORS = [
    {"name": "Material Cost Fluctuation", "importance": 0.285},
    {"name": "Vendor Score", "importance": 0.198},
    {"name": "Underground Cable Projects", "importance": 0.156},
    {"name": "Regulatory Delays", "importance": 0.132},
    {"name": "Hilly Terrain", "importance": 0.105}
];

const SAMPLE_PROJECTS = [
    {
        "name": "Mumbai Substation",
        "type": "Substation",
        "terrain": "Coastal",
        "weather": "Moderate",
        "budget": 75,
        "timeline": 30,
        "vendor_score": 4.2,
        "material_fluctuation": 0.15,
        "labor_availability": 0.85,
        "regulatory_delays": 45
    },
    {
        "name": "Delhi Underground Cable",
        "type": "Underground Cable",
        "terrain": "Plain",
        "weather": "Extreme",
        "budget": 120,
        "timeline": 36,
        "vendor_score": 3.1,
        "material_fluctuation": 0.25,
        "labor_availability": 0.75,
        "regulatory_delays": 90
    }
];

// Chart instances
let riskFactorsChart, riskMeterChart, historicalChart;

// DOM elements
const form = document.getElementById('projectForm');
const sampleBtn = document.getElementById('sampleBtn');
const clearBtn = document.getElementById('clearBtn');
const exportBtn = document.getElementById('exportBtn');

// Form inputs
const projectType = document.getElementById('projectType');
const terrainType = document.getElementById('terrainType');
const weatherRisk = document.getElementById('weatherRisk');
const originalBudget = document.getElementById('originalBudget');
const originalTimeline = document.getElementById('originalTimeline');
const vendorScore = document.getElementById('vendorScore');
const materialFluctuation = document.getElementById('materialFluctuation');
const laborAvailability = document.getElementById('laborAvailability');
const regulatoryDelays = document.getElementById('regulatoryDelays');

// Slider value displays
const vendorScoreValue = document.getElementById('vendorScoreValue');
const materialFluctuationValue = document.getElementById('materialFluctuationValue');
const laborAvailabilityValue = document.getElementById('laborAvailabilityValue');

// Result displays
const costOverrunDisplay = document.getElementById('costOverrun');
const timelineOverrunDisplay = document.getElementById('timelineOverrun');
const riskLevelDisplay = document.getElementById('riskLevel');
const confidenceScoreDisplay = document.getElementById('confidenceScore');

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    setupEventListeners();
    updateSliderValues();
});

// Event Listeners
function setupEventListeners() {
    // Form input changes
    const formInputs = form.querySelectorAll('input, select');
    formInputs.forEach(input => {
        input.addEventListener('input', calculatePredictions);
        input.addEventListener('change', calculatePredictions);
    });

    // Slider value updates
    vendorScore.addEventListener('input', updateSliderValues);
    materialFluctuation.addEventListener('input', updateSliderValues);
    laborAvailability.addEventListener('input', updateSliderValues);

    // Button actions
    sampleBtn.addEventListener('click', loadSampleProject);
    clearBtn.addEventListener('click', clearForm);
    exportBtn.addEventListener('click', exportResults);
}

// Update slider value displays
function updateSliderValues() {
    vendorScoreValue.textContent = parseFloat(vendorScore.value).toFixed(1);
    materialFluctuationValue.textContent = materialFluctuation.value;
    laborAvailabilityValue.textContent = laborAvailability.value;
}

// Load sample project data
function loadSampleProject() {
    const sample = SAMPLE_PROJECTS[Math.floor(Math.random() * SAMPLE_PROJECTS.length)];
    
    projectType.value = sample.type;
    terrainType.value = sample.terrain;
    weatherRisk.value = sample.weather;
    originalBudget.value = sample.budget;
    originalTimeline.value = sample.timeline;
    vendorScore.value = sample.vendor_score;
    materialFluctuation.value = Math.round(sample.material_fluctuation * 100);
    laborAvailability.value = Math.round(sample.labor_availability * 100);
    regulatoryDelays.value = sample.regulatory_delays;

    updateSliderValues();
    calculatePredictions();
}

// Clear form
function clearForm() {
    form.reset();
    vendorScore.value = 3;
    materialFluctuation.value = 0;
    laborAvailability.value = 75;
    regulatoryDelays.value = 0;
    
    updateSliderValues();
    clearResults();
}

// Clear results display
function clearResults() {
    costOverrunDisplay.textContent = '--';
    timelineOverrunDisplay.textContent = '--';
    riskLevelDisplay.textContent = '--';
    confidenceScoreDisplay.textContent = '--';
    
    riskLevelDisplay.className = 'result-value';
}

// Main prediction calculation
function calculatePredictions() {
    if (!validateForm()) {
        clearResults();
        return;
    }

    const inputs = getFormInputs();
    const costOverrunPct = calculateCostOverrun(inputs);
    const timelineOverrunPct = calculateTimelineOverrun(inputs);
    const riskCategory = calculateRiskLevel(costOverrunPct, timelineOverrunPct);
    const confidence = calculateConfidence(inputs);

    displayResults(costOverrunPct, timelineOverrunPct, riskCategory, confidence);
    updateCharts(inputs, costOverrunPct, timelineOverrunPct, riskCategory);
}

// Validate form inputs
function validateForm() {
    const requiredFields = [projectType, terrainType, weatherRisk, originalBudget, originalTimeline];
    return requiredFields.every(field => field.value.trim() !== '');
}

// Get form input values
function getFormInputs() {
    return {
        projectType: projectType.value,
        terrainType: terrainType.value,
        weatherRisk: weatherRisk.value,
        originalBudget: parseFloat(originalBudget.value) || 0,
        originalTimeline: parseFloat(originalTimeline.value) || 0,
        vendorScore: parseFloat(vendorScore.value) || 3,
        materialFluctuation: parseFloat(materialFluctuation.value) || 0,
        laborAvailability: parseFloat(laborAvailability.value) || 75,
        regulatoryDelays: parseFloat(regulatoryDelays.value) || 0
    };
}

// Calculate cost overrun percentage
function calculateCostOverrun(inputs) {
    const baseOverrun = HISTORICAL_DATA[inputs.projectType]?.avg_cost_overrun || 30;
    
    let overrun = baseOverrun;
    
    // Material cost fluctuation impact
    overrun += inputs.materialFluctuation * 0.8;
    
    // Vendor score impact (inverse relationship)
    overrun += (5 - inputs.vendorScore) * 8;
    
    // Labor availability impact (inverse relationship)
    overrun += (100 - inputs.laborAvailability) * 0.3;
    
    // Terrain impact
    const terrainMultipliers = { Plain: 1, Coastal: 1.1, Desert: 1.15, Hilly: 1.2 };
    overrun *= terrainMultipliers[inputs.terrainType] || 1;
    
    // Weather impact
    const weatherMultipliers = { Normal: 1, Moderate: 1.1, Extreme: 1.25 };
    overrun *= weatherMultipliers[inputs.weatherRisk] || 1;
    
    // Regulatory delays impact
    overrun += inputs.regulatoryDelays * 0.1;
    
    return Math.max(0, Math.round(overrun * 10) / 10);
}

// Calculate timeline overrun percentage
function calculateTimelineOverrun(inputs) {
    const baseOverrun = HISTORICAL_DATA[inputs.projectType]?.avg_timeline_overrun || 15;
    
    let overrun = baseOverrun;
    
    // Vendor score impact
    overrun += (5 - inputs.vendorScore) * 4;
    
    // Labor availability impact
    overrun += (100 - inputs.laborAvailability) * 0.2;
    
    // Terrain impact
    const terrainMultipliers = { Plain: 1, Coastal: 1.05, Desert: 1.1, Hilly: 1.15 };
    overrun *= terrainMultipliers[inputs.terrainType] || 1;
    
    // Weather impact
    const weatherMultipliers = { Normal: 1, Moderate: 1.15, Extreme: 1.3 };
    overrun *= weatherMultipliers[inputs.weatherRisk] || 1;
    
    // Regulatory delays direct impact
    overrun += inputs.regulatoryDelays * 0.15;
    
    return Math.max(0, Math.round(overrun * 10) / 10);
}

// Calculate overall risk level
function calculateRiskLevel(costOverrun, timelineOverrun) {
    const avgOverrun = (costOverrun + timelineOverrun) / 2;
    
    if (avgOverrun < 20) return 'LOW';
    if (avgOverrun < 40) return 'MEDIUM';
    return 'HIGH';
}

// Calculate confidence score
function calculateConfidence(inputs) {
    let confidence = 85; // Base confidence
    
    // Reduce confidence for extreme values
    if (inputs.vendorScore < 2 || inputs.vendorScore > 4.5) confidence -= 10;
    if (Math.abs(inputs.materialFluctuation) > 20) confidence -= 5;
    if (inputs.laborAvailability < 60) confidence -= 8;
    if (inputs.regulatoryDelays > 60) confidence -= 7;
    
    // Weather and terrain uncertainty
    if (inputs.weatherRisk === 'Extreme') confidence -= 5;
    if (inputs.terrainType === 'Hilly') confidence -= 3;
    
    return Math.max(60, Math.min(95, confidence));
}

// Display results
function displayResults(costOverrun, timelineOverrun, riskCategory, confidence) {
    costOverrunDisplay.textContent = `+${costOverrun}%`;
    timelineOverrunDisplay.textContent = `+${timelineOverrun}%`;
    confidenceScoreDisplay.textContent = `${confidence}%`;
    
    riskLevelDisplay.textContent = riskCategory;
    riskLevelDisplay.className = `result-value risk-${riskCategory.toLowerCase()}`;
}

// Initialize charts
function initializeCharts() {
    initializeRiskFactorsChart();
    initializeRiskMeterChart();
    initializeHistoricalChart();
}

// Risk Factors Chart
function initializeRiskFactorsChart() {
    const ctx = document.getElementById('riskFactorsChart').getContext('2d');
    
    riskFactorsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: RISK_FACTORS.map(factor => factor.name),
            datasets: [{
                label: 'Importance Score',
                data: RISK_FACTORS.map(factor => (factor.importance * 100).toFixed(1)),
                backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F'],
                borderWidth: 0,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Impact: ${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 30,
                    title: { display: true, text: 'Impact (%)' }
                },
                x: {
                    ticks: { maxRotation: 45 }
                }
            }
        }
    });
}

// Risk Meter Chart (Doughnut)
function initializeRiskMeterChart() {
    const ctx = document.getElementById('riskMeterChart').getContext('2d');
    
    riskMeterChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Low Risk', 'Medium Risk', 'High Risk'],
            datasets: [{
                data: [33, 33, 34],
                backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

// Historical Comparison Chart
function initializeHistoricalChart() {
    const ctx = document.getElementById('historicalChart').getContext('2d');
    
    const projectTypes = Object.keys(HISTORICAL_DATA);
    const costOverruns = projectTypes.map(type => HISTORICAL_DATA[type].avg_cost_overrun);
    const timelineOverruns = projectTypes.map(type => HISTORICAL_DATA[type].avg_timeline_overrun);
    
    historicalChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: projectTypes,
            datasets: [
                {
                    label: 'Average Cost Overrun (%)',
                    data: costOverruns,
                    backgroundColor: '#1FB8CD',
                    borderRadius: 4
                },
                {
                    label: 'Average Timeline Overrun (%)',
                    data: timelineOverruns,
                    backgroundColor: '#FFC185',
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Overrun (%)' }
                }
            }
        }
    });
}

// Update charts based on current predictions
function updateCharts(inputs, costOverrun, timelineOverrun, riskCategory) {
    // Update risk meter to show current project risk
    const riskValues = riskCategory === 'LOW' ? [70, 20, 10] : 
                      riskCategory === 'MEDIUM' ? [20, 60, 20] : [10, 20, 70];
    
    riskMeterChart.data.datasets[0].data = riskValues;
    riskMeterChart.update('none');
    
    // Update historical chart to include current project
    if (inputs.projectType && inputs.projectType in HISTORICAL_DATA) {
        const currentIndex = Object.keys(HISTORICAL_DATA).indexOf(inputs.projectType);
        const updatedLabels = [...historicalChart.data.labels];
        const updatedCostData = [...historicalChart.data.datasets[0].data];
        const updatedTimelineData = [...historicalChart.data.datasets[1].data];
        
        // Highlight current project prediction
        historicalChart.data.datasets[0].backgroundColor = updatedCostData.map((_, index) => 
            index === currentIndex ? '#DB4545' : '#1FB8CD'
        );
        historicalChart.data.datasets[1].backgroundColor = updatedTimelineData.map((_, index) => 
            index === currentIndex ? '#D2BA4C' : '#FFC185'
        );
        
        historicalChart.update('none');
    }
}

// Export results functionality
function exportResults() {
    if (!validateForm()) {
        alert('Please fill in all required fields before exporting.');
        return;
    }

    const inputs = getFormInputs();
    const costOverrunPct = calculateCostOverrun(inputs);
    const timelineOverrunPct = calculateTimelineOverrun(inputs);
    const riskCategory = calculateRiskLevel(costOverrunPct, timelineOverrunPct);
    const confidence = calculateConfidence(inputs);

    const reportData = {
        projectDetails: inputs,
        predictions: {
            costOverrun: costOverrunPct,
            timelineOverrun: timelineOverrunPct,
            riskLevel: riskCategory,
            confidence: confidence
        },
        timestamp: new Date().toISOString()
    };

    // Simulate file download
    const dataStr = JSON.stringify(reportData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `POWERGRID_Risk_Analysis_${Date.now()}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();

    // Show success message
    const originalText = exportBtn.textContent;
    exportBtn.textContent = 'Exported!';
    exportBtn.style.background = 'var(--color-success)';
    
    setTimeout(() => {
        exportBtn.textContent = originalText;
        exportBtn.style.background = '';
    }, 2000);
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(amount * 10000000); // Convert crores to rupees
}

function formatPercentage(value) {
    return `${value.toFixed(1)}%`;
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('Application error:', e.error);
    // Could show user-friendly error message here
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log(`App loaded in ${loadTime}ms`);
    });
}