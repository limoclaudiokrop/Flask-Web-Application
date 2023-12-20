function renderChart(arr){
    var ctx = document.getElementById('lineChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Ksh',
                data: arr,
                backgroundColor: [
                    'rgba(85,85,85, 1)'

                ],
                borderColor: 'rgb(41, 155, 99)',

                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });
}

function loadXMLDoc() {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
           if (xmlhttp.status == 200) {
                let txt = xmlhttp.responseText;
                const obj = JSON.parse(txt);
                
                months = obj["months"];

                arr = []
                for(const key in months){
                    arr.push(months[key]);
                }
                let arr1 = arr.slice(0,3);
                let arr2 = arr.slice(3,3+arr.length);
                var result = arr2.concat(arr1);
                const d = new Date();
                var month = d.getMonth() + 1;
                var end = Number(obj['end']);
                
                if(end < month){
                    month = end
                }
                var final = result.slice(0,month);
                
                renderChart(final);

                const objCont = obj["categories"];
                arr = []
                for(const key in objCont){
                    arr.push(objCont[key]);
                }
                renderChart1(arr);
                document.getElementById("totalContributions").textContent = "KES " + Number(obj["total"]).toLocaleString();

                
               
           }
           else if (xmlhttp.status == 400) {
              alert('There was an error 400');
           }
           else {
               alert('something else other than 200 was returned');
           }
        }
    };

    xmlhttp.open("GET", "http://localhost:5000/getData", true);
    xmlhttp.send();
}

loadXMLDoc();


