
function selectLogo(){
	let log = document.getElementById("selectLogo").value;
	if(log != ""){
		document.getElementById("imgInvoiceLogo").src = logos[log];
		
	}
	document.getElementById("selectLogo").style.display = "none";
}
function displaySelectLogo(){
	document.getElementById("selectLogo").style.display = "block";
}

function changeLogo(){
	var link = document.getElementById("invoiceLogoUrl").value;
	if(link == ""){
		return;
	}
	document.getElementById("imgInvoiceLogo").src =link;
	document.getElementById("invoiceLogoCancel").click(); 
}
function checkFilename(){

	var filename = document.getElementById("invoiceFilename").value;
	
	if(filename == ""){
		var error = document.getElementById("invoiceFilenameError");
		error.textContent = "*** Enter filename ***";
		error.style.display = "block";
		return;
	}

	var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) { 
           if (xmlhttp.status == 200) {
                let txt = xmlhttp.responseText;
                if (txt == 'True'){
                	document.getElementById("invoiceDownloadBtn").style.display = "none";
                	document.getElementById("invoiceLoader").style.display = "block";
                	
                	downloadInvoice(filename);
                	return;
                }else{
                	var error = document.getElementById("invoiceFilenameError");
					error.textContent = "*** Filename already exists ***";
					error.style.display = "block";
					return;
                }
           }
           
           
        }
    };

    xmlhttp.open("GET", runUrl + "/invoicefilename?name=" + filename, true);
    xmlhttp.send();
}


function downloadInvoice(filename){
	var Data = { 
	    sender : [],
	    receiver : [],
	    invoice : [],
	    stats : [],
	    items : [],
	    bank : [],
	    logo : document.getElementById("imgInvoiceLogo").src,
	    filename: filename

	};
	var span = "span";
	for(let i=0; i < 6; i++){
		var curr = span + i;
		Data.sender.push(document.getElementById(curr).textContent);
	}
	span = "span";
	for(let i=8; i < 11; i++){
		var curr = span + i;
		Data.invoice.push(document.getElementById(curr).textContent);
	}
	span = "span1";
	for(let i=1; i < 7; i++){
		var curr = span + i;
		Data.receiver.push(document.getElementById(curr).textContent);
	}
	span = "span4";
	for(let i=1; i < 5; i++){
		var curr = span + i;
		Data.bank.push(document.getElementById(curr).textContent);
	}

	let tax = document.getElementById('taxVal').value;
	if(tax == "tax"){
    	Data.stats.push(document.getElementById("subTot").textContent + "/-");
		Data.stats.push(document.getElementById("span21").textContent + "%");
		Data.stats.push(document.getElementById("taxAmount").textContent + "/-");
		Data.stats.push(document.getElementById("total").textContent + "/-");

    }else{
		Data.stats.push(document.getElementById("total").textContent + "/-");    	
    }
	
	var table = document.getElementById("invoice_table");
	var len = document.getElementById("invoice_table").rows.length;
	var end = len-1;
	if(tax == "tax"){end = len-2;}
	for(let i=1; i < end; i++){
		var row = table.rows[i];
		var tempArr = [];
		tempArr.push(row.cells[0].textContent);
		tempArr.push(row.cells[1].textContent);
		Data.items.push(tempArr);
	}
	var xhr = new XMLHttpRequest();
	xhr.open("POST", runUrl + "/postinvoice", true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.onreadystatechange = function () {
	  if (xhr.readyState === 4) {
	    window.location.href = runUrl + "/storage?doc=static/documents/Invoices";
	    // window.location.href = runUrl + "/renderinvoice";
	  }};
	xhr.send(JSON.stringify(Data));
}


function ona(id){
	document.getElementById("edit" + id).style.display = "inline";
	document.getElementById("p" + id).style.display = "none";	
}

function ficha(id){
	document.getElementById("edit" + id).style.display = "none";
	document.getElementById("p" + id).style.display = "block";
	document.getElementById("span" + id).textContent = document.getElementById("inp" + id).value;	
}

function toa(){
	var len = document.getElementById("invoice_table").rows.length;
	document.getElementById("invoice_table").deleteRow(len-2);
	document.getElementById("taxVal").value = "noTax";

}