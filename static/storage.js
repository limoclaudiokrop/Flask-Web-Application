var testUrl = "http://localhost:5000";
var liveUrl = "https://biblefaithchurchit.pythonanywhere.com";
var runUrl = testUrl;


function validaterenameFileForm(root){
	var error = document.getElementById("renameFileError");
	name = document.getElementById("renameFile").value;
	if(name == ""){
		error.textContent = "*** Enter filenname ***";
		error.style.display = "block";
		return;
	}
	path = root + "/" + name + ".pdf";
	var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
           if (xmlhttp.status == 200) {
                let txt = xmlhttp.responseText;
                if(txt == "false"){
                	error.textContent = "*** Filename already exists ***";
                	error.style.display = "block";
                	return;
                }else{
                	document.getElementById("renameFileForm").submit();
                }

            }
           
           
        }
    };

    xmlhttp.open("GET", runUrl + "/checkfilename?path=" + path, true);
    xmlhttp.send();
	
	
}


function validateAddInvoiceForm(){
	let elemError = document.getElementById("submitInvoiceError");
     var x = document.forms["addInvoiceForm"]["name"].value;
	  if (x == "") {
	    elemError.innerText = "*** " + "Enter company name" + " ***";
	    elemError.style.display = "block";
	    return false;
	  }
	  x = document.forms["addInvoiceForm"]["box"].value;
	  if (x == "") {
	    elemError.innerText = "*** " + "Enter company P.O Box address" + " ***";
	    elemError.style.display = "block";
	    return false;
	  }
	  x = document.forms["addInvoiceForm"]["city"].value;
	  if (x == "") {
	    elemError.innerText = "*** " +  "Enter company address city and region" + " ***";
	    elemError.style.display = "block";
	    return false;
	  }
	  x = document.forms["addInvoiceForm"]["postal"].value;
	  if (x == "") {
	    elemError.innerText = "*** " + "Enter Postal code" + " ***";
	    elemError.style.display = "block";
	    return false;
	  }
	  x = document.forms["addInvoiceForm"]["invoice_number"].value;
	  if (x == "") {
	    elemError.innerText = "*** " + "Enter Invoice number" + " ***";
	    elemError.style.display = "block";
	    return false;
	  }
	  x = document.forms["addInvoiceForm"]["issue_date"].value;
	  if (x == "") {
	    elemError.innerText = "*** " +  "Enter Invoice issue date" + " ***";
	    elemError.style.display = "block";
	    return false;
	  }
	  x = document.forms["addInvoiceForm"]["due_date"].value;
	  if (x == "") {
	    elemError.innerText = "*** " + "Enter Invoice due date" + " ***";
	    elemError.style.display = "block";
	    return false;
	  }

	  // x = document.forms["addInvoiceForm"]["tax"].value;
	  // if (x == "") {
	  //   elemError.innerText = "*** " +  + " ***";
	  //   elemError.style.display = "block";
	  //   alert("Enter tax percentage");
	  //   return false;
	  // }
	  // if(!isNumeric(x)){
	  //   elemError.innerText = "*** " +  + " ***";
	  //   elemError.style.display = "block";
	  //   alert("Value of tax is not a number");
	  //   return false
	  // }
	  // x = document.forms["addInvoiceForm"]["discount"].value;
	  // if (x == "") {
	  //   elemError.innerText = "*** " +  + " ***";
	  //   elemError.style.display = "block";
	  //   alert("Enter Discount");
	  //   return false;
	  // }
	  // if(!isNumeric(x)){
	  //   elemError.innerText = "*** " + "Value of discount is not a number" + " ***";
	  //   elemError.style.display = "block";
	  //   return false
	  // }

}


function isNumeric(value) {
    return /^-?\d+$/.test(value);
}

function addInvoiceItem(){
	let tax = document.getElementById('taxVal').value;

	var desc = document.getElementById("invoice_description").value;
    var amount = document.getElementById("invoice_amount").value;
    var table = document.getElementById("invoice_table");
    var len = document.getElementById("invoice_table").rows.length;
    var tot = table.rows[len-1].cells[1].innerHTML;
    if(tax == "tax"){
    	var row = table.insertRow(len-2);
    }else{
    	var row = table.insertRow(len-1);
    }

    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.innerHTML = desc;
    cell2.innerHTML = Number(amount).toLocaleString() + "/-";
    
    if(tax == "tax"){
    	let subtotelem = document.getElementById("subTot");
	    var subtot = Number(subtotelem.textContent.replace(/,/g, '')) + Number(amount);
	    subtotelem.textContent = subtot.toLocaleString();
	    var taxrate = Number(document.getElementById("span21").textContent);
	    var taxAmount = taxrate * subtot / 100;
	    document.getElementById("taxAmount").textContent = taxAmount.toLocaleString();
	    var total = taxAmount + subtot;
	    document.getElementById("total").textContent = total.toLocaleString(); 
	    
    }else{
    	var totElem = document.getElementById("total");
    	var total = Number(amount) + Number(totElem.textContent.replace(/,/g, ''));
    	totElem.textContent = total.toLocaleString();
    }
    document.getElementById("addItemCancelBtn").click();
}

function validateUploadFileForm(){
	if( document.getElementById("uploadFile").files.length == 0 ){
    	return false;
	}
	return true;
}

function populateRenameModal(filename, path, root, cat){
	
	document.getElementById("renameFile").value = filename.split(".pdf")[0];
	
	document.getElementById("renamePath").value = path;
	document.getElementById("renameRoot").value = root;
	document.getElementById("renameCat").value = cat;
	document.getElementById("prevname").value = filename;
}

function validatenewFolderForm(){
	let name = document.getElementById("newFolder").value;
	let error = document.getElementById("newFolderError");
	if(document.getElementById("newFolder").value == ""){
		error.style.display = "block";
		error.innerText = "*** Enter folder name ***";

		return false;
	}
	let elements = document.getElementsByClassName("dirs");

	let valid = true;
	Array.from(elements).forEach(function (element) {
	  if(element.innerText.trim() === name.trim()){
	  	valid = false;
	  }
	});

	if(!valid){
		error.style.display = "block";
		error.innerText = "*** Folder already exists ***";
		return false;
	}
	

}

function validatenewApplicationForm(){
	let name = document.getElementById("newApplication").value;
	let error = document.getElementById("newAppError");
	if(document.getElementById("newApplication").value == ""){
		error.style.display = "block";
		error.innerText = "*** Enter Application name ***";

		return false;
	}
	let elements = document.getElementsByClassName("dirs");

	let valid = true;
	Array.from(elements).forEach(function (element) {
	  if(element.innerText.trim() === name.trim()){
	  	valid = false;
	  }
	});

	if(!valid){
		error.style.display = "block";
		error.innerText = "*** Application already exists ***";
		return false;
	}
}

function getData(root, position){
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) { // XMLHttpRequest.DONE == 4
           if (xmlhttp.status == 200) {
                let txt = xmlhttp.responseText;
                const obj = JSON.parse(txt);
                let root = obj['root'];
                let arrDirs = obj['dirs'];
                for (var i=0; i < arrDirs.length; i++){
                	var curr = arrDirs[i];
                	choraFolder(root + "/" + curr, curr, position);
                }
                let arrFiles = obj['files'];
                for (var i=0; i < arrFiles.length; i++){
                	var curr = arrFiles[i];
                	choraFile(root + "/" + curr, curr, position);
                }

           }
           
           
        }
    };

    xmlhttp.open("GET", runUrl + "/getFiles?doc=" + root, true);
    xmlhttp.send();
}

function choraFolder(root, folderName, position){
	let outerdiv = document.createElement('div');
	outerdiv.className = "border mr-5 mb-5";
	outerdiv.setAttribute("onclick", "loadSelections('" + root + "', '1','oz','" + position + "')");

	let img = document.createElement('img');
    img.src = "static/folder.jpg";
    img.height = "250";
    img.width = "250"
    outerdiv.appendChild(img);

    let innerDiv = document.createElement('div');
    let span = document.createElement('span');
    span.className = "ml-3";
    span.innerText = folderName;
    innerDiv.style.backgroundColor = "#f2f2f2";
    
    innerDiv.appendChild(span);
    outerdiv.appendChild(innerDiv);

    document.getElementById('fileCollector').appendChild(outerdiv);
}


function choraFile(root, filename, position){
	outerdiv = document.createElement('div');
	outerdiv.className = "border mr-5 mb-5";
	
	img = document.createElement('embed');
    img.src = root;
    img.height = "250";
    img.width = "250"
    outerdiv.appendChild(img);

    innerDiv = document.createElement('div');
    innerDiv.setAttribute("onclick", "loadSelections('" + root + "', '2','"+filename+"', '"+position+"')");

    span = document.createElement('span');
    span.className = "ml-3";
    span.innerText = filename
    innerDiv.style.backgroundColor = "#f2f2f2";
    
    innerDiv.appendChild(span);
    outerdiv.appendChild(innerDiv);
    document.getElementById('fileCollector').appendChild(outerdiv);
}

function submitFileSelection(path, fileroot,filename,position){

	var xhr = new XMLHttpRequest();
	xhr.open("POST", runUrl + "/selectfile", true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.onreadystatechange = function () {
	  if (xhr.readyState === 4) {
	    window.location.href = runUrl + "/storage?doc="+ xhr.responseText;
	  }};
	xhr.send(JSON.stringify({
	    'path': path,
	    'file': fileroot,
	    'filename': filename,
	    'position': position
	}));
} 
function loadSelections(root, mode,filename, position){
	if(mode == "1"){
		document.getElementById('fileCollector').innerHTML = '';
		getData(root, position);  

	}else{
		let path = document.getElementById("currentDirectory").value;
		let fileroot = root;
		submitFileSelection(path, fileroot,filename,position);
	}
	
    
}

