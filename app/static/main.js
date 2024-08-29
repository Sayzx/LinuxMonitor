var ctx = document.getElementById('ping-chart').getContext('2d');
var pingChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['1', '2', '3', '4', '5'],
        datasets: [{
            label: 'Statistiques de Ping',
            borderColor: 'blue',
            data: [10, 20, 30, 25, 35]
        }]
    }
});
