const ctx = document.getElementById('attendanceChart').getContext('2d');

// Prepare the data
var data = [
    { date: '2023-01-01', students: 40 },
    { date: '2023-02-01', students: 25 },
    { date: '2023-03-01', students: 0 },
    { date: '2023-04-01', students: 50 },
    { date: '2023-05-01', students: 30 }
];

// Convert date strings to actual Date objects
var parsedData = data.map(item => ({
    x: new Date(item.date),
    y: item.students
}));

// Create a line chart
new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Number of Students',
            data: parsedData,
            borderColor: '#008141',
            backgroundColor: '#00814122',
            pointRadius: 4,
            pointBackgroundColor: '#008141',
            pointBorderColor: '#ffffff',
            pointHoverRadius: 6,
            pointHoverBackgroundColor: '#008141',
            pointHoverBorderColor: '#ffffff',
            lineTension: 0,
            borderWidth: 2
        }]
    },
    options: {
        scales: {
             x: {
              type: 'time',
                 time: {
                     unit: 'month'
                 },
                  ticks: {
                      source: 'data' // Force x-axis ticks to be based on data points
                  }
             },
            y: {
                type: 'linear',
                ticks: {
                    beginAtZero: true // Start y-axis from zero
                }
            }
        }
    }
});
