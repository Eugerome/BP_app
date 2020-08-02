// declare myRecords to get access within all functions
var myRecords = [];

// load all records immediately
window.onload = function() {
    CreateRecordTable();
  };

// clickaway from edit popup to close
document.querySelector("#addBlocker").addEventListener("click", function(event){
    let isClickInside = document.querySelector("#popup").contains(event.target);
    if (!isClickInside) {
        document.querySelector("#addBlocker").style.display = "none";
    }
})

// clickaway from delete popup to close
document.querySelector("#deleteBlocker").addEventListener("click", function(event){
    let isClickInside = document.querySelector("#deletePopup").contains(event.target);
    if (!isClickInside) {
        document.querySelector("#deleteBlocker").style.display = "none";
    }
})

// display dates at user browser time
function UserTimezone (timestamp) {

}

// get record_id for item
function GetSelectedId (elem) {
    var selectedId = elem.closest("tr").firstElementChild.innerHTML;
    return parseInt(selectedId, 10);
}

// triggers when Add Record button is clicked
async function AddRecord () {
    // bring up popup
    document.getElementById("closeAddRecord").setAttribute("onclick", "PushRecord()");
    document.querySelector("#addBlocker").style.display = "flex";
}

// triggers when delete record butoon is clicked
async function ConfirmDeleteRecord (elem) {
    // get record_id of this row
    let selectedId = GetSelectedId(elem)
    // raise popup
    document.querySelector("#deleteBlocker").style.display = "flex";
    // pass record_id to DeleteRecord function
    let newButtonFunc = "DeleteRecord(" + selectedId.toString() + ")"
    document.getElementById("deleteTrue").setAttribute("onclick", newButtonFunc);
    }

// triggers if delete action not confirmed
async function NoDeleteRecord() {
    document.querySelector("#deleteBlocker").style.display = "none";
}

// triggers if delete action is confirmed
async function DeleteRecord(record_id) {
    let response = await fetch("./records/" + record_id.toString(), {
        method: "DELETE",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    // close popup
    NoDeleteRecord();
    // refresh table automatically
    CreateRecordTable();
}

async function EditRecord (elem) {
    // get record_id of this row
    let selectedId = GetSelectedId(elem)
    // access record data from myRecords
    let recordIdx = 0
    for (var i = 0; i < myRecords.length; i++) {
        if (myRecords[i]["record_id"] == selectedId){
            recordIdx = i
            break;
        }
    }
    let selectedRecord = myRecords[recordIdx]
    // add record id to save record button
    let newButtonFunc = "PushRecord(" + selectedRecord["record_id"] + ")"
    document.getElementById("closeAddRecord").setAttribute("onclick", newButtonFunc);
    // bring up popup
    let popupEdit = document.getElementById("popup")
    document.querySelector("#addBlocker").style.display = "flex";
    // populate with selectedRecord values
    Object.keys(selectedRecord).forEach( function(key) {
        if (key != "record_id") {
            popupEdit.querySelector("#" + key).value = selectedRecord[key]
        }
    })
}

async function PushRecord ( record_id=null) {
    // get input
    var bp_upper = document.getElementById("bp_upper").value;
    var bp_lower = document.getElementById("bp_lower").value;
    var timestamp = document.getElementById("timestamp").value;
    var notes = document.getElementById("notes").value;
    // validate that bp was given
    if (bp_upper === "", bp_lower === "") {
        alert("Please fill in Blood Pressure Fields");
        return false;
    }
    var bp_upper = parseInt(bp_upper, 10)
    var bp_lower = parseInt(bp_lower, 10)
    // create payload
    var payload = {
        "bp_upper" : bp_upper,
        "bp_lower" : bp_lower
    }
    // add timestamp and note if provided, otherwise don't include in payload
    if (typeof timestamp === 'string' && timestamp != "") {
        timestamp = new Date(timestamp)
        timestamp = timestamp.toISOString()
        payload["timestamp"] = timestamp;
    }
    if (typeof notes === 'string' && notes != "") {
        payload["notes"] = notes;
    }
    // if record_id is null - create new record, otherwise edit existing one
    if (record_id == null) {
        // post payload
        let response = await fetch("./records", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
            body: JSON.stringify(payload)
        })
    } else {
        let response = await fetch("./records/" + record_id.toString(), {
            method: "PUT",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
            body: JSON.stringify(payload)
        })
    }
    // reset popup
    document.getElementById("popup").reset();
    // make popup invisible
    document.querySelector("#addBlocker").style.display = "none";
    // refresh table automatically
    CreateRecordTable();
}


async function CreateRecordTable() {
    // refresh
    let response = await fetch("./records");
    myRecords = await response.json()

    // Provide col values and their headers; No need to generate since shouldn't change
    let col = ["record_id", "timestamp", "bp_upper", "bp_lower", "notes"];
    let colHeaders = ["record_id", "Time", "Upper", "Lower", "Notes", "Edit"];

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
    let divContainer = document.getElementById("dataTable");
    divContainer.innerHTML = "";
    divContainer.appendChild(table);
}
