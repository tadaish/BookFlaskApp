function drawChart1(type, data, labels, id = "chart1", title = '# Số lượng') {
    const ctx = document.getElementById(id);

    new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: data,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },

        }
    });
}

function drawChart2(type, data2, labels2, id = "chart2", title = 'Doanh thu') {
    const ctx = document.getElementById(id);

    new Chart(ctx, {
        type: type,
        data: {
            labels: labels2,
            datasets: [{
                label: title,
                data: data2,
                borderWidth: 1,
                backgroundColor: ['#FFB3BA', '#A9CCE3', '#FDFD96', '#77DD77', '#CBAACB']
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },

        }
    });
}