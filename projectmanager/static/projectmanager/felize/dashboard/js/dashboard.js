function initializePendingItemCountPanels() {
    $.get(pendingItemDataApiUrl, function (data, status) {
        $("#active_projects_count").removeClass('loader').html(data.active_projects_count);
        $("#closed_projects_count").removeClass('loader').html(data.closed_projects_count);
        $("#pending_milestones_count").removeClass('loader').html(data.pending_milestones_count);
        $("#pending_tasks_count").removeClass('loader').html(data.pending_tasks_count);
        $("#unallocated_employee_count").removeClass('loader').html(data.unallocated_employee_count);
    });
}

$(document).ready(function (e) {
    initializePendingItemCountPanels();
});


var barChartData = {
    labels: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    datasets: [{
        label: 'Dataset 1',
        backgroundColor: 'red',
        data: [
            12,
            31,
            4,
            18,
            7,
            29,
            32
        ]
    }, {
        label: 'Dataset 2',
        backgroundColor: 'blue',
        data: [
            43,
            12,
            21,
            10,
            4,
            41,
            18
        ]
    }]

};

window.onload = function () {
    var ctx1 = document.getElementById('canvas').getContext('2d');
    window.myBar = new Chart(ctx1, {
        type: 'bar',
        data: barChartData,
        options: {
            title: {
                display: true,
                text: 'Billable time by resource type'
            },
            tooltips: {
                mode: 'index',
                intersect: false
            },
            responsive: true,
            scales: {
                xAxes: [{
                    stacked: true,
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    });
    var ctx2 = document.getElementById('canvas1').getContext('2d');
    var config = {
        type: 'pie',
        data: {
            datasets: [{
                data: [
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                ],
                backgroundColor: [
                    'red',
                    'orange',
                    'yellow',
                    'green',
                    'blue',
                ],
                label: 'Dataset 1'
            }],
            labels: [
                'Red',
                'Orange',
                'Yellow',
                'Green',
                'Blue'
            ]
        },
        options: {
            responsive: true
        }
    };
    window.myPie = new Chart(ctx2, config);
};

var randomScalingFactor = function () {
    return Math.round(Math.random() * 100);
};