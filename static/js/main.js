/**
 * Examination Timetabling System - Main JavaScript File
 * Provides interactive functionality and utility functions
 */

// Global variables
let currentUser = null;
let optimizationRunning = false;

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    initializeSystem();
    setupEventListeners();
    loadUserPreferences();
});

/**
 * Initialize the system
 */
function initializeSystem() {
    console.log('Initializing Examination Timetabling System...');
    
    // Check for user session
    checkUserSession();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize charts if Chart.js is available
    if (typeof Chart !== 'undefined') {
        initializeCharts();
    }
    
    // Add loading animations
    addLoadingAnimations();
}

/**
 * Setup global event listeners
 */
function setupEventListeners() {
    // Form submissions
    document.addEventListener('submit', handleFormSubmission);
    
    // Button clicks
    document.addEventListener('click', handleButtonClicks);
    
    // Window events
    window.addEventListener('resize', handleWindowResize);
    window.addEventListener('beforeunload', handleBeforeUnload);
    
    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
}

/**
 * Handle form submissions
 */
function handleFormSubmission(event) {
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (submitBtn) {
        // Show loading state
        showLoadingState(submitBtn);
        
        // Validate form
        if (!validateForm(form)) {
            event.preventDefault();
            hideLoadingState(submitBtn);
            return false;
        }
    }
}

/**
 * Handle button clicks
 */
function handleButtonClicks(event) {
    const button = event.target.closest('button');
    if (!button) return;
    
    const action = button.dataset.action;
    
    switch (action) {
        case 'export':
            handleExport(button);
            break;
        case 'delete':
            handleDelete(button);
            break;
        case 'duplicate':
            handleDuplicate(button);
            break;
        case 'optimize':
            handleOptimize(button);
            break;
    }
}

/**
 * Handle window resize
 */
function handleWindowResize() {
    // Debounce resize events
    clearTimeout(window.resizeTimeout);
    window.resizeTimeout = setTimeout(() => {
        updateResponsiveElements();
    }, 250);
}

/**
 * Handle before unload
 */
function handleBeforeUnload(event) {
    if (optimizationRunning) {
        event.preventDefault();
        event.returnValue = 'Optimization is running. Are you sure you want to leave?';
        return event.returnValue;
    }
}

/**
 * Handle keyboard shortcuts
 */
function handleKeyboardShortcuts(event) {
    // Ctrl/Cmd + S: Save
    if ((event.ctrlKey || event.metaKey) && event.key === 's') {
        event.preventDefault();
        handleSave();
    }
    
    // Ctrl/Cmd + O: Optimize
    if ((event.ctrlKey || event.metaKey) && event.key === 'o') {
        event.preventDefault();
        handleOptimize();
    }
    
    // Escape: Close modals
    if (event.key === 'Escape') {
        closeAllModals();
    }
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize charts
 */
function initializeCharts() {
    // Find all chart canvases
    const chartCanvases = document.querySelectorAll('canvas[data-chart]');
    
    chartCanvases.forEach(canvas => {
        const chartType = canvas.dataset.chart;
        const chartData = JSON.parse(canvas.dataset.chartData || '{}');
        
        createChart(canvas, chartType, chartData);
    });
}

/**
 * Create a chart
 */
function createChart(canvas, type, data) {
    const ctx = canvas.getContext('2d');
    
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: data.title || 'Chart'
            }
        }
    };
    
    switch (type) {
        case 'line':
            return new Chart(ctx, {
                type: 'line',
                data: data,
                options: { ...defaultOptions, ...data.options }
            });
        case 'bar':
            return new Chart(ctx, {
                type: 'bar',
                data: data,
                options: { ...defaultOptions, ...data.options }
            });
        case 'pie':
            return new Chart(ctx, {
                type: 'pie',
                data: data,
                options: { ...defaultOptions, ...data.options }
            });
        default:
            console.warn('Unknown chart type:', type);
    }
}

/**
 * Add loading animations
 */
function addLoadingAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

/**
 * Show loading state
 */
function showLoadingState(element) {
    const originalText = element.innerHTML;
    element.dataset.originalText = originalText;
    
    element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    element.disabled = true;
    element.classList.add('loading');
}

/**
 * Hide loading state
 */
function hideLoadingState(element) {
    if (element.dataset.originalText) {
        element.innerHTML = element.dataset.originalText;
        delete element.dataset.originalText;
    }
    
    element.disabled = false;
    element.classList.remove('loading');
}

/**
 * Validate form
 */
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    return isValid;
}

/**
 * Show field error
 */
function showFieldError(field, message) {
    clearFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = message;
    
    field.classList.add('is-invalid');
    field.parentNode.appendChild(errorDiv);
}

/**
 * Clear field error
 */
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
    
    return notification;
}

/**
 * Handle export functionality
 */
function handleExport(button) {
    const format = button.dataset.format || 'pdf';
    const id = button.dataset.id;
    
    if (!id) {
        showNotification('Export ID not found', 'error');
        return;
    }
    
    showNotification(`Exporting to ${format.toUpperCase()}...`, 'info');
    
    // Simulate export process
    setTimeout(() => {
        showNotification(`Successfully exported to ${format.toUpperCase()}`, 'success');
    }, 2000);
}

/**
 * Handle delete functionality
 */
function handleDelete(button) {
    const id = button.dataset.id;
    const name = button.dataset.name || 'item';
    
    if (!confirm(`Are you sure you want to delete ${name}?`)) {
        return;
    }
    
    // Show loading state
    showLoadingState(button);
    
    // Simulate delete process
    setTimeout(() => {
        hideLoadingState(button);
        showNotification(`Successfully deleted ${name}`, 'success');
        
        // Remove the element from DOM
        const element = button.closest('.card, .row, tr');
        if (element) {
            element.remove();
        }
    }, 1000);
}

/**
 * Handle duplicate functionality
 */
function handleDuplicate(button) {
    const id = button.dataset.id;
    
    showNotification('Duplicating item...', 'info');
    
    // Simulate duplicate process
    setTimeout(() => {
        showNotification('Item duplicated successfully', 'success');
    }, 1000);
}

/**
 * Handle optimize functionality
 */
function handleOptimize(button) {
    if (optimizationRunning) {
        showNotification('Optimization already running', 'warning');
        return;
    }
    
    optimizationRunning = true;
    showNotification('Starting optimization...', 'info');
    
    // Simulate optimization process
    setTimeout(() => {
        optimizationRunning = false;
        showNotification('Optimization completed successfully', 'success');
    }, 5000);
}

/**
 * Handle save functionality
 */
function handleSave() {
    showNotification('Saving changes...', 'info');
    
    // Simulate save process
    setTimeout(() => {
        showNotification('Changes saved successfully', 'success');
    }, 1000);
}

/**
 * Update responsive elements
 */
function updateResponsiveElements() {
    const isMobile = window.innerWidth < 768;
    
    // Update navigation
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        navbar.classList.toggle('navbar-expanded', !isMobile);
    }
    
    // Update sidebar
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('sidebar-collapsed', isMobile);
    }
}

/**
 * Close all modals
 */
function closeAllModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        const modalInstance = bootstrap.Modal.getInstance(modal);
        if (modalInstance) {
            modalInstance.hide();
        }
    });
}

/**
 * Check user session
 */
function checkUserSession() {
    // This would typically check with the server
    const userElement = document.querySelector('[data-user]');
    if (userElement) {
        currentUser = JSON.parse(userElement.dataset.user);
    }
}

/**
 * Load user preferences
 */
function loadUserPreferences() {
    const theme = localStorage.getItem('theme') || 'light';
    const language = localStorage.getItem('language') || 'en';
    
    applyTheme(theme);
    applyLanguage(language);
}

/**
 * Apply theme
 */
function applyTheme(theme) {
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

/**
 * Apply language
 */
function applyLanguage(language) {
    document.documentElement.setAttribute('lang', language);
    localStorage.setItem('language', language);
}

/**
 * Utility function to format date
 */
function formatDate(date, format = 'YYYY-MM-DD') {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    
    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day);
}

/**
 * Utility function to format time
 */
function formatTime(time, format = 'HH:mm') {
    if (typeof time === 'string') {
        time = new Date(`2000-01-01T${time}`);
    }
    
    const hours = String(time.getHours()).padStart(2, '0');
    const minutes = String(time.getMinutes()).padStart(2, '0');
    
    return format
        .replace('HH', hours)
        .replace('mm', minutes);
}

/**
 * Utility function to debounce
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Utility function to throttle
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for global use
window.TimetablingSystem = {
    showNotification,
    formatDate,
    formatTime,
    debounce,
    throttle,
    applyTheme,
    applyLanguage
};
