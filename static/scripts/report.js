let variable=4;

function submit_section1(){
    var form = document.getElementById("section1_form")
    form.submit()
}

function add_medicine(){
    // event.preventDefault();
    let medicines= document.getElementById("medicines");
    let new_medicine=`
        <div class="space">
            <label for="m${variable}">${variable}.</label><input type="text" id="m${variable}">
            <input type="checkbox" id="m${variable} MORNING" unchecked="'True"><label for="m${variable} MORNING">MORNING</label>
            <input type="checkbox" id="m${variable} AFTERNOON" unchecked="'True"><label for="m${variable} AFTERNOON">AFTERNOON</label>
            <input type="checkbox" id="m${variable} NIGHT" unchecked="'True"><label for="m${variable} NIGHT">NIGHT</label>
        </div>
    `;
    medicines.innerHTML += new_medicine;
    variable=variable+1;
}


function submit_section4() {
    // Gather and handle the data
    // Example: you can iterate through the dynamically added medicine entries and collect the information

    // For illustration purposes, let's log the data to the console
    let medicinesData = [];
    document.querySelectorAll('.space').forEach(function (medicineEntry) {
        let medicineInfo = {
            label: medicineEntry.querySelector('label').textContent,
            input: medicineEntry.querySelector('input[type="text"]').value,
            morning: medicineEntry.querySelector('input[id$="MORNING"]').checked,
            afternoon: medicineEntry.querySelector('input[id$="AFTERNOON"]').checked,
            night: medicineEntry.querySelector('input[id$="NIGHT"]').checked
        };
        medicinesData.push(medicineInfo);
    });

    console.log("Medicines Data:", medicinesData);
}