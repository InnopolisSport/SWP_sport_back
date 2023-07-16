//Fetch default analytics data for all sports and all groups
function fetchDefaultAnalytics() {
    return fetch('/api/analytics/attendance')
        .then(response => response.json())
        .then(data => data);
}

//Create default array for all sports and all groups with date + number
var all_analytics_array = await fetchDefaultAnalytics();
console.log(all_analytics_array);

//Create array with date + number as a dictionary
var default_array_with_dicts = [];
for (let key in all_analytics_array) {
    var dict = {};
    dict["date"] = key;
    dict["students"] = all_analytics_array[key];
    default_array_with_dicts.push(dict);
}

console.log(default_array_with_dicts);
// Convert date strings to actual Date objects
var parsedData = default_array_with_dicts.map(item => ({
    x: new Date(item["date"]),
    y: item["students"],
}));

//Get HTML elements
const ctx = document.getElementById('attendanceChart').getContext('2d');

// Create a line chart
const attendance_chart = new Chart(ctx, {
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
                     unit: 'week'
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

//export {attendance_chart, getParsedData};
export default attendance_chart;
