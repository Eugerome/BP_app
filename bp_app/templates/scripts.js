window.onload = function() {
    CreateRecordTable();
  };

document.getElementById("displayAddRecord").addEventListener("click", function(){
    document.querySelector(".blocker").style.display = "flex";
})

document.getElementById("closeAddRecord").addEventListener("click", function(){
    document.querySelector(".blocker").style.display = "none";
})
// add a close button later
document.querySelector(".close").addEventListener("click", function(){
    document.querySelector(".blocker").style.display = "none";
})

async function AddRecord () {
    // get input
    var bpUpper = document.getElementById("bpUpper").value;
    var bpLower = document.getElementById("bpLower").value;
    var timestamp = document.getElementById("timestamp").value;
    var notes = document.getElementById("notes").value;
    // validate that bp was given
    if (bpUpper === "", bpLower === "") {
        alert("Please fill in Blood Pressure Fields");
        return false;
    }
    var bpUpper = parseInt(bpUpper, 10)
    var bpLower = parseInt(bpLower, 10)
    // create payload
    var payload = {
        "bp_upper" : bpUpper,
        "bp_lower" : bpLower
    }
    // add timestamp and note if provided, otherwise don't include in payload
    if (typeof timestamp === 'string' && timestamp != "") {
        payload["timestamp"] = timestamp;
    }
    if (typeof notes === 'string' && notes != "") {
        payload["notes"] = notes;
    }
    // post payload
    let response = await fetch("./records", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
        body: JSON.stringify(payload)
    })
}

async function CreateRecordTable() {

    // Call Records Endpoint
    let response = await fetch("./records");


    let myRecords = await response.json()
    // EXTRACT VALUE FOR HTML HEADER.
    var col = [];
    for (var i = 0; i < myRecords.length; i++) {
        for (var key in myRecords[i]) {
            if (col.indexOf(key) === -1) {
                col.push(key);
            }
        }
    }

    // CREATE DYNAMIC TABLE.
    var table = document.createElement("table");

    // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

    var tr = table.insertRow(-1);                   // TABLE ROW.

    for (var i = 0; i < col.length; i++) {
        var th = document.createElement("th");      // TABLE HEADER.
        th.innerHTML = col[i];
        tr.appendChild(th);
    }

    // ADD JSON DATA TO THE TABLE AS ROWS.
    for (var i = 0; i < myRecords.length; i++) {

        tr = table.insertRow(-1);

        for (var j = 0; j < col.length; j++) {
            var tabCell = tr.insertCell(-1);
            tabCell.innerHTML = myRecords[i][col[j]];
        }
    }

    // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
    var divContainer = document.getElementById("showData");
    divContainer.innerHTML = "";
    divContainer.appendChild(table);
}
