function addRule(){

	var text = '{"chain" : "'+document.getElementById("chain").value.trim()+'",'+
		'"Line_Number" : "'+document.getElementById("id").value.trim()+'",'+
		'"Source_IP" : "'+document.getElementById("source").value.trim()+'",'+
		'"Destination_IP" : "'+document.getElementById("destination").value.trim()+'",'+
		'"Protocol" : "'+document.getElementById("prot").value.trim()+'",'+
		'"Source_Port" : "'+document.getElementById("sport").value.trim()+'",'+
		'"Destination_Port" : "'+document.getElementById("dport").value.trim()+'",'+
		'"Interface_Input" : "'+document.getElementById("in").value.trim()+'",'+
		'"Interface_Output" : "'+document.getElementById("out").value.trim()+'",'+
		'"Target" : "'+document.getElementById("target").value.trim()+'"}';
	var xhr = new XMLHttpRequest();
	var url = "https://localhost:5000/v1/api/add-rule/";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
	    if (xhr.readyState === 4 && xhr.status === 200) {
		console.log(xhr.responseText);
		location.reload();
	    }
	};
	var data = JSON.stringify(JSON.parse(text));
	xhr.send(data);

}

function updateList(){

	fetch('https://localhost:5000/v1/api/list/')
 	.then(response => response.json())
	.then(data => {
		var numList = Object.keys(data).length;
		var i;
		for(i=0;i<numList;i++){
			var tbodyRef = document.getElementById('list').getElementsByTagName('tbody')[0];
			var newRow = tbodyRef.insertRow();
			var numEle = Object.keys(data[i]).length;
			var newCell = newRow.insertCell();
			var newText = document.createTextNode(data[i].chain);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newText = document.createTextNode(data[i].id);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newText = document.createTextNode(data[i].pkts);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newText = document.createTextNode(data[i].bytes);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newText = document.createTextNode(data[i].target);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newText = document.createTextNode(data[i].prot);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newText = document.createTextNode(data[i].opt);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newText = document.createTextNode(data[i].in);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newText = document.createTextNode(data[i].out);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newText = document.createTextNode(data[i].source);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newText = document.createTextNode(data[i].destination);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newText = document.createTextNode(data[i].spt);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newText = document.createTextNode(data[i].dpt);
			newCell.appendChild(newText);
			newCell = newRow.insertCell();
			newBtn = document.createElement("BUTTON");
			newBtn.innerHTML = "Delete";
			newBtn.value = data[i].chain+":"+data[i].id
			newBtn.addEventListener('click', function(){
				var str = this.value.split(":");
				del(str[0], str[1]);
			}, false);
			newCell.appendChild(newBtn);
		}
	});

}
function del( chain, id){

	var xhr = new XMLHttpRequest();
	var url = "https://localhost:5000/v1/api/delete-rule/";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
	    if (xhr.readyState === 4 && xhr.status === 200) {
		console.log(xhr.responseText);
		location.reload();
	    }
	};
	var data = JSON.stringify(JSON.parse('{ "chain" : "'+chain+'", "Line_Number" : "'+id+'"}'));
	xhr.send(data);

}
