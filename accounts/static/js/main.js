// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })
    
    // Date pickers
    const datePickers = document.querySelectorAll('.datepicker');
    datePickers.forEach(picker => {
        picker.addEventListener('focus', function() {
            this.type = 'date';
        });
    });
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Dynamic dashboard updates
    if (document.getElementById('dashboard-stats')) {
        updateDashboardStats();
    }
});

function updateDashboardStats() {
    // Simulate API call to get stats
    setTimeout(() => {
        document.getElementById('patients-count').textContent = '1,248';
        document.getElementById('appointments-count').textContent = '84';
        document.getElementById('revenue-count').textContent = '$24,560';
        document.getElementById('doctors-count').textContent = '18';
    }, 800);
}