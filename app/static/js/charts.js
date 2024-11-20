// Location Chart - Bar Chart
var ctx = document.getElementById('locationChart').getContext('2d');
var locationChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: chartData.cities,
        datasets: [{
            label: '# of Jobs',
            data: chartData.jobCounts,
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Company Chart - Horizontal Bar Chart
var ctx2 = document.getElementById('companyChart').getContext('2d');
var companyChart = new Chart(ctx2, {
    type: 'horizontalBar',
    data: {
        labels: chartData.companies,
        datasets: [{
            label: '# of Jobs',
            data: chartData.companyJobCounts,
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                beginAtZero: true
            }
        }
    }
});

// Hourly Pay Chart - Line Chart
var ctx3 = document.getElementById('hourlyPayChart').getContext('2d');
var hourlyPayChart = new Chart(ctx3, {
    type: 'line',
    data: {
        labels: chartData.titles,
        datasets: [{
            label: 'Hourly Pay ($)',
            data: chartData.hourlyPays,
            backgroundColor: 'rgba(153, 102, 255, 0.6)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 2,
            fill: false
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Rating Chart - Doughnut Chart
var ctx4 = document.getElementById('ratingChart').getContext('2d');
var ratingChart = new Chart(ctx4, {
    type: 'doughnut',
    data: {
        labels: chartData.ratings,
        datasets: [{
            label: '# of Ratings',
            data: chartData.ratingCounts,
            backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            }
        }
    }
});
