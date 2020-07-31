// declare myRecords to get access within all functions
var myRecords = [];

// load all records immediately
window.onload = function() {
    CreateRecordTable();
  };

// adding new record
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

async function EditRecord (elem) {
    // bring up popup
    document.querySelector(".blocker").style.display = "flex";
    // get record_id of this row
    let selectedId = elem.closest("tr").firstElementChild.innerHTML;
    selectedId = parseInt(selectedId, 10)
    // access record data from myRecords
    let recordIdx = 0
    for (var i = 0; i < myRecords.length; i++) {
        if (myRecords[i]["record_id"] == selectedId){
            recordIdx = i
            break;
        }
    }
    let selectedRecord = myRecords[recordIdx]
    debugger;
}

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
    // refresh
    let response = await fetch("./records");
    myRecords = await response.json()

    // Provide col values and their headers; No need to generate since shouldn't change
    let col = ["record_id", "timestamp", "bp_upper", "bp_lower", "notes"];
    let colHeaders = ["record_id", "Time", "Upper", "Lower", "Notes", "Edit"]

    // CREATE DYNAMIC TABLE.
    let table = document.createElement("table");

    // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

    let tr = table.insertRow(-1);                   // TABLE ROW.

    // Create Headers
    for (let i = 0; i < colHeaders.length; i++) {
        let th = document.createElement("th");
        th.innerHTML = colHeaders[i];
        if (i == 0) {
            th.style = "display:none"
        }; // hide record_id and edit/delete headers
        tr.appendChild(th);
    }
    //  get edit/delete block from html
    let toolBox = document.querySelector(".toolBox");
    // ADD JSON DATA TO THE TABLE AS ROWS.
    for (let i = 0; i < myRecords.length; i++) {

        tr = table.insertRow(-1);

        for (let j = 0; j < colHeaders.length; j++) {
            let tabCell = tr.insertCell(-1);
            if (j < col.length) {
                tabCell.innerHTML = myRecords[i][col[j]];
                if (j == 0) {
                    tabCell.style = "display:none"
                }; // hide record_id
            } else {
                // add edit/delete image
                tabCell.innerHTML = toolBox.outerHTML;
            }
        }
    }
    // add edit and delete button

    // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
    let divContainer = document.getElementById("showData");
    divContainer.innerHTML = "";
    divContainer.id = "dataTable";
    divContainer.appendChild(table);
}
