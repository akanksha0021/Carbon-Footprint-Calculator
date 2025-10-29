document.addEventListener('DOMContentLoaded', function() {
    // Get form and result elements
    const calculatorForm = document.getElementById('calculator-form');
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error-message');
    const initialMessageDiv = document.getElementById('initial-message');
    const recommendationsCard = document.getElementById('recommendations-card');
    const goodJobCard = document.getElementById('good-job-card');
    const regionSelect = document.getElementById('region');
    const backToTopButton = document.getElementById('backToTop');
    const themeToggle = document.getElementById('checkbox');
    
    // Dark mode toggle
    themeToggle.addEventListener('change', function(e) {
        if (e.target.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });
    
    // Check for saved theme preference
    const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;
    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        
        if (currentTheme === 'dark') {
            themeToggle.checked = true;
        }
    }
    
    // Back to top button functionality
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });
    
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Add animation classes to elements when they appear in viewport
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.card:not(.animated)');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight;
            
            if (elementPosition < screenPosition) {
                element.classList.add('fade-in');
                element.classList.add('animated');
            }
        });
    };
    
    window.addEventListener('scroll', animateOnScroll);
    
    // Load regions from API
    loadRegions();
    
    // Add event listener for form submission
    calculatorForm.addEventListener('submit', function(e) {
        e.preventDefault();
        calculateFootprint();
    });
    
    // Function to load regions from API
    function loadRegions() {
        fetch('/regions')
            .then(response => response.json())
            .then(regions => {
                regions.forEach(region => {
                    const option = document.createElement('option');
                    option.value = region;
                    option.textContent = region;
                    regionSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error loading regions:', error);
            });
    }
    
    // Function to calculate carbon footprint
    function calculateFootprint() {
        // Show loading, hide results and error
        loadingDiv.classList.remove('d-none');
        resultsDiv.classList.add('d-none');
        errorDiv.classList.add('d-none');
        initialMessageDiv.classList.add('d-none');
        
        // Get form data
        const formData = new FormData(calculatorForm);
        
        // Send request to server
        fetch('/calculate', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading
            loadingDiv.classList.add('d-none');
            
            if (data.success) {
                // Display results
                displayResults(data);
                resultsDiv.classList.remove('d-none');
                
                // Add animation classes to results
                const resultCards = document.querySelectorAll('#results .card');
                resultCards.forEach((card, index) => {
                    setTimeout(() => {
                        card.classList.add('fade-in');
                    }, index * 200); // Stagger animations
                });
                
                // Smooth scroll to results
                document.querySelector('#results').scrollIntoView({
                    behavior: 'smooth'
                });
            } else {
                // Show error
                errorDiv.textContent = data.error || 'An error occurred. Please try again.';
                errorDiv.classList.remove('d-none');
                errorDiv.classList.add('fade-in');
            }
        })
        .catch(error => {
            // Hide loading, show error
            loadingDiv.classList.add('d-none');
            errorDiv.textContent = 'Network error. Please check your connection and try again.';
            errorDiv.classList.remove('d-none');
            errorDiv.classList.add('fade-in');
            console.error('Error:', error);
        });
    }
    
    // Function to display results
    function displayResults(data) {
        // Total footprint
        const totalValue = document.getElementById('total-value');
        const totalProgress = document.getElementById('total-progress');
        const globalAverage = document.getElementById('global-average');
        const totalComparison = document.getElementById('total-comparison');
        const regionalComparison = document.getElementById('regional-comparison');
        
        // Set values
        totalValue.textContent = data.footprints.total.toFixed(2);
        globalAverage.textContent = data.global_averages.total.toFixed(2);
        
        // Calculate percentage of global average
        const percentage = (data.footprints.total / data.global_averages.total) * 100;
        
        // Animate progress bar
        totalProgress.style.width = '0%';
        setTimeout(() => {
            totalProgress.style.transition = 'width 1s ease-in-out';
            totalProgress.style.width = `${Math.min(percentage, 200)}%`; // Cap at 200%
        }, 100);
        
        // Set progress bar color based on level
        totalProgress.classList.remove('progress-high', 'progress-moderate', 'progress-low');
        totalProgress.classList.add(`progress-${data.level}`);
        
        // Set comparison text
        if (percentage > 100) {
            totalComparison.textContent = `You're ${(percentage - 100).toFixed(0)}% above the global average`;
        } else {
            totalComparison.textContent = `You're ${(100 - percentage).toFixed(0)}% below the global average`;
        }
        
        // Set regional comparison if provided
        if (data.regional_comparison) {
            regionalComparison.textContent = data.regional_comparison;
            regionalComparison.classList.remove('d-none');
        } else {
            regionalComparison.classList.add('d-none');
        }
        
        // Category breakdown
        const categoryBreakdown = document.getElementById('category-breakdown');
        categoryBreakdown.innerHTML = '';
        
        const categories = ['electricity', 'transportation', 'food', 'waste', 'water'];
        const categoryLabels = {
            'electricity': 'Electricity',
            'transportation': 'Transportation',
            'food': 'Food',
            'waste': 'Waste',
            'water': 'Water'
        };
        
        categories.forEach((category, index) => {
            if (category !== 'total') {
                const value = data.footprints[category];
                const comparison = data.comparisons[category];
                const globalAvg = data.global_averages[category];
                const percentage = (value / globalAvg) * 100;
                const selectedLevel = category === 'food' ? data.selected_levels.meat : data.selected_levels[category];
                
                const categoryItem = document.createElement('div');
                categoryItem.className = 'category-item';
                categoryItem.style.opacity = '0';
                
                let statusIndicator = '';
                let statusIcon = '';
                
                if (comparison === 'high') {
                    statusIndicator = '<span class="badge bg-danger">HIGH</span>';
                    statusIcon = '<i class="fas fa-exclamation-circle text-danger"></i>';
                } else if (comparison === 'moderate') {
                    statusIndicator = '<span class="badge bg-warning text-dark">MODERATE</span>';
                    statusIcon = '<i class="fas fa-exclamation-triangle text-warning"></i>';
                } else {
                    statusIndicator = '<span class="badge bg-success">LOW</span>';
                    statusIcon = '<i class="fas fa-check-circle text-success"></i>';
                }
                
                // Add badge for selected level
                let selectedLevelBadge = '';
                if (selectedLevel === 'high') {
                    selectedLevelBadge = '<span class="badge bg-secondary ms-2">You reported: High</span>';
                } else if (selectedLevel === 'moderate') {
                    selectedLevelBadge = '<span class="badge bg-secondary ms-2">You reported: Moderate</span>';
                } else {
                    selectedLevelBadge = '<span class="badge bg-secondary ms-2">You reported: Low</span>';
                }
                
                categoryItem.innerHTML = `
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h5 class="mb-0">${categoryLabels[category]} ${statusIcon}</h5>
                        <div>
                            ${statusIndicator}
                            ${selectedLevelBadge}
                        </div>
                    </div>
                    <div class="progress mb-2">
                        <div class="progress-bar progress-${comparison}" role="progressbar" 
                            style="width: 0%"></div>
                    </div>
                    <div class="d-flex justify-content-between">
                        <span>Your footprint: ${value.toFixed(2)} tons</span>
                        <span>Global average: ${globalAvg.toFixed(2)} tons</span>
                    </div>
                `;
                
                categoryBreakdown.appendChild(categoryItem);
                
                // Animate each category item with delay
                setTimeout(() => {
                    categoryItem.style.transition = 'opacity 0.5s ease-in-out';
                    categoryItem.style.opacity = '1';
                    
                    // Animate progress bar
                    const progressBar = categoryItem.querySelector('.progress-bar');
                    setTimeout(() => {
                        progressBar.style.transition = 'width 1s ease-in-out';
                        progressBar.style.width = `${Math.min(percentage, 200)}%`;
                    }, 100);
                }, index * 200);
            }
        });
        
        // Recommendations
        const recommendationsDiv = document.getElementById('recommendations');
        recommendationsDiv.innerHTML = '';
        
        if (Object.keys(data.recommendations).length > 0) {
            // Show recommendations card, hide good job card
            recommendationsCard.classList.remove('d-none');
            goodJobCard.classList.add('d-none');
            
            // Add recommendations for each category
            let delayIndex = 0;
            for (const category in data.recommendations) {
                const recommendations = data.recommendations[category];
                
                const categoryDiv = document.createElement('div');
                categoryDiv.className = 'recommendation-category';
                categoryDiv.innerHTML = `<h5>${capitalizeFirstLetter(category)}</h5>`;
                categoryDiv.style.opacity = '0';
                
                recommendations.forEach(recommendation => {
                    const recommendationItem = document.createElement('div');
                    recommendationItem.className = 'recommendation-item';
                    
                    recommendationItem.innerHTML = `
                        <h6>${recommendation.title}</h6>
                        <p>${recommendation.description}</p>
                        <div class="d-flex">
                            <div class="me-3">
                                <small>Impact: <span class="impact-${recommendation.impact.toLowerCase()}">${recommendation.impact}</span></small>
                            </div>
                            <div>
                                <small>Effort: <span class="effort-${recommendation.effort.toLowerCase()}">${recommendation.effort}</span></small>
                            </div>
                        </div>
                    `;
                    
                    categoryDiv.appendChild(recommendationItem);
                });
                
                recommendationsDiv.appendChild(categoryDiv);
                
                // Animate with delay
                setTimeout(() => {
                    categoryDiv.style.transition = 'opacity 0.5s ease-in-out';
                    categoryDiv.style.opacity = '1';
                }, delayIndex * 300);
                delayIndex++;
            }
        } else {
            // Show good job card, hide recommendations card
            goodJobCard.classList.remove('d-none');
            recommendationsCard.classList.add('d-none');
        }
    }
    
    // Helper function to capitalize first letter
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
}); 