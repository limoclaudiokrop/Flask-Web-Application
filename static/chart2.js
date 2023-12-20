function renderChart1(arr){
    var ctx2 = document.getElementById('doughnut').getContext('2d');
var myChart2 = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: ['Ongoing', 'Pending', 'Completed', 'Archives'],

        datasets: [{
            label: 'Projects',
            data: arr,
            backgroundColor: [
                'rgba(41, 155, 99, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(255, 77, 77, 1)'

            ],
            borderColor: [
                'rgba(41, 155, 99, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(255, 77, 77, 1)'

            ],
            borderWidth: 1
        }]

    },
    options: {
        responsive: true
    }
});
}

function loadXMLDoc1() {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
           if (xmlhttp.status == 200) {
                let txt = xmlhttp.responseText;
                const arr = txt.split(",");
                let n = arr.length;
                var numArr = [];
                for(var i =0; i < n; i++){
                    numArr.push(parseInt(arr[i]));
                }
                
                renderChart1(numArr);
               
           }
           else if (xmlhttp.status == 400) {
              alert('There was an error 400');
           }
           else {
               alert('something else other than 200 was returned');
           }
        }
    };

    xmlhttp.open("GET", "http://localhost:5000/getSummary", true);
    xmlhttp.send();
}

//loadXMLDoc1();
