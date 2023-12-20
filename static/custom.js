var testUrl = "http://localhost:5000";
var liveUrl = "https://biblefaithchurchit.pythonanywhere.com";
var runUrl = testUrl;
var currentLocation = window.location;


function validateDepositForm(){
    if(document.getElementById("selectAreaOptAdd").value == ""){
        document.getElementById("depositError").textContent = "*** Enter all fields ***";
        document.getElementById("depositError").style.display = "block"; 
        return false;
    }

    if(document.getElementById("selectLocal").value == ""){
        document.getElementById("depositError").textContent = "*** Enter all fields ***";
        document.getElementById("depositError").style.display = "block"; 
        return false;
    }

    if(document.getElementById("depositDate").value == ""){
        document.getElementById("depositError").textContent = "*** Enter all fields ***";
        document.getElementById("depositError").style.display = "block"; 
        return false;
    }
    if(document.getElementById("depositAmount").value == ""){
        document.getElementById("depositError").textContent = "*** Enter all fields ***";
        document.getElementById("depositError").style.display = "block"; 
        return false;
    }
    if(document.getElementById("").value == ""){
        document.getElementById("depositError").textContent = "*** Enter all fields ***";
        document.getElementById("depositError").style.display = "block"; 
        return false;
    }
    if(document.getElementById("").value == ""){
        document.getElementById("depositError").textContent = "*** Enter all fields ***";
        document.getElementById("depositError").style.display = "block"; 
        return false;
    }
    if(document.getElementById("").value == ""){
        document.getElementById("depositError").textContent = "*** Enter all fields ***";
        document.getElementById("depositError").style.display = "block"; 
        return false;
    }


    return true;
}

function validateCreateEmployeeForm(){
    if(document.getElementById("firstname").value == ""){
        document.getElementById("newDirectorError").textContent = "*** Enter all fields ***";
        document.getElementById("newDirectorError").style.display = "block";
        
        return false;
    }
    if(document.getElementById("lastname").value == ""){

        document.getElementById("newDirectorError").textContent = "*** Enter all fields ***";
        document.getElementById("newDirectorError").style.display = "block";
        return false;
    }
    if(document.getElementById("directorEmail").value == ""){

        document.getElementById("newDirectorError").textContent = "*** Enter all fields ***";
        document.getElementById("newDirectorError").style.display = "block";
        return false;
    }
    return true;
}
function hideAddDirector(){
    document.getElementById("requirementDetails").style.display = "none";
    document.getElementById("addDirectorBtn").style.display = "block";

}

function showAddDirector(){
    document.getElementById("requirementDetails").style.display = "block";
    document.getElementById("addDirectorBtn").style.display = "none";
}

function editAccount(val){
    var idName = "editButton" + val;
    var aEl = document.getElementById(idName);
    var curr = aEl.textContent;
    if(curr == "edit"){
        aEl.innerHTML = "save";
        var el = document.getElementById("account"+val);
        var val1 = el.textContent;
        var valNum =  parseFloat(val1.replace(/,/g, ''))
        el.innerHTML = '<input id="editInput'+val+'" style="width: 80px; margin-right: 0px;" type="number" value=' + valNum + '>';

        el = document.getElementById("desc"+val);
        val1 = el.textContent;
        el.innerHTML = '<input id="descInput'+val+'" style="width: 160px; height: 25px; margin-right: 0px;" type="text" value=' + val1 + '>';

    }else{
        aEl.innerHTML = "edit";
        var desc = document.getElementById("descInput"+val).value;
        document.getElementById("desc"+val).innerHTML = desc;

        var currVal = document.getElementById("editInput"+val).value;
        var el = document.getElementById("account"+val);
        var preval = document.getElementById("tempAcc"+val).value;
        var accountId = document.getElementById("accountId" + val).value;
        var unsign = Number(currVal);
        if(unsign < 0){
            unsign = unsign * -1;
        }
        updateAccount(accountId, unsign, desc);
        var tot = document.getElementById("total");
        var wd = document.getElementById("wd" + val).innerHTML;
        //var diff = Number(currVal) - Number(preval);

        if(wd.trim() == "Withdraw"){
            unsign = unsign *-1;
        }
        el.innerHTML = Number(unsign).toLocaleString();
        var diff = Number(unsign) - parseFloat(preval.replace(/,/g, ''))
        document.getElementById("tempAcc"+val).value = unsign; 
        var totVal = tot.innerHTML;
         var totVal = Number(totVal.replace(/,/g, '')) + diff;
         tot.innerHTML = totVal.toLocaleString();
    }
     
}

function updateAccount(accountId, newVal, desc){
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
           if (xmlhttp.status == 200) {
                let txt = xmlhttp.responseText;
           }
           
           
        }
    };

    xmlhttp.open("GET", runUrl + "/setAccount?id=" + accountId + "&val="+newVal+"&desc="+desc, true);
    xmlhttp.send();
}

function editMembers(val){
    var idName = "editButton" + val;
    var aEl = document.getElementById(idName);
    var curr = aEl.textContent;
    if(curr == "edit"){
        aEl.innerHTML = "save";
        let statusDiv = "statusVal" + val;
        let selectDiv = "statusSelect" + val;
        document.getElementById(statusDiv).style.display = "none";
        document.getElementById(selectDiv).style.display = "block";
       
    }else{
        aEl.innerHTML = "edit";
        let statusDiv = document.getElementById("statusVal" + val);
        let selectDiv = document.getElementById("statusSelect" + val);
        var churchId = document.getElementById("churchId" + val).value;
        var currVal = selectDiv.value;
        var dict = ["invalid", "Ongoing", "Pending", "Completed", "Archive"];
        if(currVal != "0"){
            statusDiv.innerHTML = dict[Number(currVal)];
        }
        selectDiv.style.display ="none";
        statusDiv.style.display = "block";

        if(currVal != "0"){
            updateMembers(churchId, currVal);
        }
    }
     
}

function updateMembers(churchId, newVal){
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
           if (xmlhttp.status == 200) {
                let txt = xmlhttp.responseText;
           }
           
           
        }
    };

    xmlhttp.open("GET", runUrl+"/setMembers?id=" + churchId + "&val="+newVal, true);
    xmlhttp.send();
}

function filterBillings(){
    area = document.getElementById("searchAreaSelectBillings").value;
    local = document.getElementById("searchLocalSelect").value;
    date = document.getElementById("searchDateSelect").value;
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
           if (xmlhttp.status == 200) {
                let txt = xmlhttp.responseText;
                const obj = JSON.parse(txt);
                var table = document.getElementById('billingsTable');
                while(table.rows.length > 2) {
                  table.deleteRow(table.rows.length-1);
                }
                var dict = {"1":"Offerings", "2":"Mavuno", "3":"Tithes","4":"Fund-Raising"};
                var dict2 = {"1":"MPESA","2":"Cash"};
                var clearance = document.getElementById("clearanceStatus").value;
                var total = 0;
                for(var i =0; i < obj.length; i++){
                    var arr = obj[i];
                    var row = table.insertRow(table.rows.length);
                    var cell1 = row.insertCell(0);
                    var cell2 = row.insertCell(1);
                    var cell3 = row.insertCell(2);
                    var cell4 = row.insertCell(3);
                    var cell5 = row.insertCell(4);
                    var cellP = row.insertCell(5);
                    
                    var cell6 = row.insertCell(6);
                    
                    var index = i + 1;
                    var hiddenId = "accountId" + index;
                    
                    cell1.innerHTML = arr[3]+ '<input id="' + hiddenId + '" type="hidden" + value="'+arr[0]+'" >';
                    cell2.innerHTML = arr[6] + '<input id="tempAcc' + index + '" type="hidden" + value="'+arr[4]+'" >';
                    cell3.innerHTML = arr[7];
                    
                    cell4.innerHTML = arr[1];
                    cell5.innerHTML = dict2[arr[2]];;
                    cell6.innerHTML = arr[4];
                    cell6.id = "account" + index;
                    
                    var element = document.createElement("a");
                    cellP.innerHTML = arr[8]
                    cellP.id = "wd" + index;
                    if(arr[8] == "Deposit"){
                        total = total + Number(arr[4])
                    }else{
                        total = total - Number(arr[4])
                    }
                    if(clearance == "2"){
                        var cell7 = row.insertCell(7);
                        
                        var aId = "editButton" + index;
                        cell7.innerHTML = '<a id="'+aId+'" onclick="editAccount('+index +')" class="tagLink font-italic " style="color: blue; margin-right: 15px;">edit</a>';
                    
                        
                    }
                }
                
                var row = table.insertRow(table.rows.length);
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                cell1.innerHTML = "Total";
                cell1.colSpan = "6";
                cell2.innerHTML = total
                cell2.id = "total";
                
           }
           
           
        }
    };
    var url = runUrl+"/filterbillings?area=" + area + "&date=" + date;
    if(local != ""){
        url = runUrl+"/filterbillingslocal?area=" + area + "&local="+local + "&date=" + date;
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function filterChurches(){
    area = document.getElementById("searchAreaSelectChurches").value;
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
           if (xmlhttp.status == 200) {
                let txt = xmlhttp.responseText;
                const obj = JSON.parse(txt);
                var table = document.getElementById('churchesTable');
                while(table.rows.length > 2) {
                  table.deleteRow(table.rows.length-1);
                }
                for(var i =0; i < obj.length; i++){
                    var arr = obj[i];
                    var row = table.insertRow(table.rows.length);
                    var cell1 = row.insertCell(0);
                    var cell2 = row.insertCell(1);
                    var cell3 = row.insertCell(2);
                    var cell4 = row.insertCell(3);
                    var cell5 = row.insertCell(4);
                    var index = i + 1;
                    var hiddenId = "churchId" + index;
                    cell1.innerHTML = i+1 + '<input id="' + hiddenId + '" type="hidden" + value="'+arr[0]+'" >';
                    cell2.innerHTML = arr[1]
                    cell3.innerHTML = arr[2];
                    cell4.innerHTML = arr[4];
                    
                    cell4.id = "members" + index;
                    var aId = "editButton" + index;
                    cell5.innerHTML = '<a id="'+aId+'" onclick="editMembers('+index +')" class="tagLink font-italic " style="color: blue; margin-right: 15px;">edit</a>';
                    
                }
           }
           
           
        }
    };

    xmlhttp.open("GET", runUrl+"/filterchurches?area=" + area, true);
    xmlhttp.send();
}

if(currentLocation == runUrl+"/dashboard"){
    document.getElementById("searchAreaSelect").addEventListener("change", populateLocalSelect);

    function populateLocalSelect(){
        selEl = document.getElementById("searchLocalSelect");
        var i,L = selEl.options.length-1;
        for(i = L; i >= 1; i--){
            selEl.remove(i);
        }
        val = document.getElementById("searchAreaSelect").value;
        if (val != ""){
             var xmlhttp = new XMLHttpRequest();

                xmlhttp.onreadystatechange = function() {
                    if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
                       if (xmlhttp.status == 200) {
                            let txt = xmlhttp.responseText;
                            const arr = txt.split(",");
                            var select = document.getElementById("searchLocalSelect");
                            for (var i =0; i < arr.length-1; i++){
                                var opt = arr[i];
                                var el = document.createElement("option");
                                el.textContent = opt;
                                el.value = opt;
                                select.appendChild(el);
                            }
                       }
                       
                       
                    }
                };

                xmlhttp.open("GET", runUrl+"/findLocals?area=" + val, true);
                xmlhttp.send();
            
        }
        
    }


}
if(currentLocation == runUrl+"/billing"){
    document.getElementById("searchAreaSelectBillings").addEventListener("change", populateLocalSelectBilling);

    function populateLocalSelectBilling(){
        selEl = document.getElementById("searchLocalSelect");
        var i,L = selEl.options.length-1;
        for(i = L; i >= 1; i--){
            selEl.remove(i);
        }
        val = document.getElementById("searchAreaSelectBillings").value;
        if (val != ""){
             var xmlhttp = new XMLHttpRequest();

                xmlhttp.onreadystatechange = function() {
                    if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
                       if (xmlhttp.status == 200) {
                            let txt = xmlhttp.responseText;
                            const arr = txt.split(",");
                            var select = document.getElementById("searchLocalSelect");
                            for (var i =0; i < arr.length-1; i++){
                                var opt = arr[i];
                                var el = document.createElement("option");
                                el.textContent = opt;
                                el.value = opt;
                                select.appendChild(el);
                            }
                       }
                       
                       
                    }
                };

                xmlhttp.open("GET", runUrl+"/findLocals?area=" + val, true);
                xmlhttp.send();
            
        }
        
    }


}

function filter(){
    reset = document.getElementById("adminCheck").value;
    area = document.getElementById("searchAreaSelect").value;
    if(area == "" && reset == "fresh"){
        return;
    }
    if(area == ""  && reset == "rotten"){
        document.getElementById("adminCheck").value = "fresh";
        var oldcanv = document.getElementById('lineChart');
        oldcanv.remove();
        var canv = document.createElement('canvas');
        canv.id = 'lineChart';
        document.getElementById("lineChartDiv").appendChild(canv);
        
        oldcanv = document.getElementById('doughnut');
        oldcanv.remove();
        canv = document.createElement('canvas');
        canv.id = 'doughnut';
        document.getElementById("doughnutDiv").appendChild(canv);
        
        document.getElementById("branchesNum").textContent = document.getElementById("hiddenBranches").value;
        //document.getElementById("members").textContent = document.getElementById("hiddenMembers").value
        document.getElementById("totalContributions").textContent = document.getElementById("hiddenContributions").value
        
        loadXMLDoc();
        //loadXMLDoc1();
        return;
    }
    if(area != "" && reset == "fresh"){
        document.getElementById("adminCheck").value = "rotten";
        document.getElementById("hiddenBranches").value = document.getElementById("branchesNum").textContent;
        //document.getElementById("hiddenMembers").value = document.getElementById("members").textContent;
        document.getElementById("hiddenContributions").value = document.getElementById("totalContributions").textContent;
        
    }
    
    local = document.getElementById("searchLocalSelect").value;

    document.getElementById("searchButton").style.display = "none";
    document.getElementById("searchLoader").style.display = "block";

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
       if (xmlhttp.status == 200) {
            let txt = xmlhttp.responseText;
            const obj = JSON.parse(txt);
            document.getElementById("branchesNum").textContent = obj["branches"];
            //document.getElementById("members").textContent = obj["members"];
            document.getElementById("totalContributions").textContent = "Ksh " + Number(obj["total"]).toLocaleString();
            
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
            
            var oldcanv = document.getElementById('lineChart');
            oldcanv.remove();
            var canv = document.createElement('canvas');
            canv.id = 'lineChart';
            document.getElementById("lineChartDiv").appendChild(canv);
            renderChart(final);

            const objCont = obj["categories"];
            arr = []
            for(const key in objCont){
                arr.push(objCont[key]);
            }
            oldcanv = document.getElementById('doughnut');
            oldcanv.remove();
            canv = document.createElement('canvas');
            canv.id = 'doughnut';
            document.getElementById("doughnutDiv").appendChild(canv);
            
            renderChart1(arr);

            document.getElementById("searchButton").style.display = "block";
            document.getElementById("searchLoader").style.display = "none";
    
            
       }
       
       
    }
};
var url = runUrl+"/sortarea?area=" + val;
if(local != ""){
    url = runUrl+"/sortlocal?area=" + val + "&local=" + local;
}
xmlhttp.open("GET", url, true);
xmlhttp.send();
}


if(currentLocation == runUrl+"/addProject" ){
    document.getElementById("selectAreaOpt").addEventListener("change", openNewArea);
    function openNewArea(){
        val = document.getElementById("selectAreaOpt").value;
        if (val == "Other"){

            document.getElementById("newAreaDiv").style.display = "block";
        }else{
            document.getElementById("newAreaDiv").style.display = "none";
        }
        
    }    
}

if(currentLocation == runUrl+"/deposit" || currentLocation == runUrl+"/withdraw"
    || currentLocation == runUrl+"/addAccount"){
    document.getElementById("selectAreaOptAdd").addEventListener("change", openSelectLocal);

    function openSelectLocal(){
        selEl = document.getElementById("selectLocal");
        var i,L = selEl.options.length-1;
        for(i = L; i >= 1; i--){
            selEl.remove(i);
        }
        val = document.getElementById("selectAreaOptAdd").value;
        if (val != ""){
             var xmlhttp = new XMLHttpRequest();

                xmlhttp.onreadystatechange = function() {
                    if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
                       if (xmlhttp.status == 200) {
                            let txt = xmlhttp.responseText;
                            const arr = txt.split(",");
                            var select = document.getElementById("selectLocal");
                            var options = ["Agape", "Town", "Inheritance"];
                            for (var i =0; i < arr.length-1; i++){
                                var opt = arr[i];
                                var el = document.createElement("option");
                                el.textContent = opt;
                                el.value = opt;
                                select.appendChild(el);
                            }
                            document.getElementById("selectLocalDiv").style.display = "block";
                       }
                       
                       
                    }
                };

                xmlhttp.open("GET", runUrl+"/findLocals?area=" + val, true);
                xmlhttp.send();
            
        }else{
            document.getElementById("selectLocalDiv").style.display = "none";
        }
        
    }


}

// if(currentLocation == runUrl+"/withdraw" || currentLocation == runUrl+"/deposit"){
//     document.getElementById("selectLocal").addEventListener("change", openSelectAccount);

//     function openSelectAccount(){
//         val = document.getElementById("selectAreaOptAdd").value;
//         local = document.getElementById("selectLocal").value;
//         selEl = document.getElementById("selectAccount");
//         var i,L = selEl.options.length-1;
//         for(i = L; i >= 1; i--){
//             selEl.remove(i);
//         }
//              var xmlhttp = new XMLHttpRequest();

//                 xmlhttp.onreadystatechange = function() {
//                     if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
//                        if (xmlhttp.status == 200) {
//                             let txt = xmlhttp.responseText;

//                             const arr = txt.split(",");
//                             var select = document.getElementById("selectAccount");
                            
//                             for (var i =0; i < arr.length-1; i++){
//                                 var sels = arr[i].split("-");
                                
//                                 var el = document.createElement("option");
//                                 el.textContent = arr[i];
//                                 el.value = sels[0].trim();
//                                 select.appendChild(el);
//                             }
//                        }
                       
                       
//                     }
//                 };
//                 xmlhttp.open("GET", runUrl+"/findAccounts?area=" + val + "&local=" + local, true);
//                 xmlhttp.send();
            
        
        
//     }


// }


function forgot_password(){
    email = document.getElementById("email").value;
    document.getElementById("loader").style.display = "block"
    document.getElementById("loaderDiv").style.display = "none"
        
    if(email == ""){
        document.getElementById("loginError").textContent = "Enter your email";
        return;
    }
    document.getElementById("loaderDiv").style.display = "block"
    
   var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
           if (xmlhttp.status == 200) {
                let txt = xmlhttp.responseText;
                document.getElementById("loaderDiv").style.display = "none"
    
                if(txt == "not found"){
                    document.getElementById("loginError").textContent = "Account with this email does not exist";
                
                }
                if(txt == "success"){
                    document.getElementById("loginError").textContent = "Your new password has been sent to your email";
                    
                }
                
           }
           
        }
    };

    xmlhttp.open("GET", runUrl+"/forgot?email=" + email, true);
    xmlhttp.send();

}
