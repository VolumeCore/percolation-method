const serverUrl = 'http://127.0.0.1:4567'

function fetchData(size, concentration) {
    return fetch(serverUrl + `/generateMatrix/${size}/${concentration}`)
        .then((res) => res.json())
        .then((data) => data);
}

function validateData(data) {
    let result = Array.isArray(data);
    if(result) return isSquareMatrix(data);
    else return false;
}

function isSquareMatrix(matrix) {
    for (var i = 0; i < matrix.length; i++) {
        rows = matrix.length;
        columns = matrix[i].length;
        if(rows != columns) {
          return false;
        }
    }
    return true;
}

function generateTable(data) {
    let percolationTable = document.getElementById('percolation-table');
    percolationTable.innerHTML = "";
    for (let row of data) {
        let tableRow = percolationTable.insertRow();
        for (let col of row) {
            let cell = tableRow.insertCell();
            !!col && cell.classList.add('_blue');
        }
    }
    let containerElem = document.querySelector('.percolation-method');
    containerElem.insertBefore(percolationTable, containerElem.firstChild);
}

function showMessageInsideTable(message){
    let percolationTable = document.getElementById('percolation-table');
    percolationTable.innerHTML = "";
    let tableRow = percolationTable.insertRow(0);
    let cell = tableRow.insertCell();
    cell.classList.add('_darkgray');
    cell.innerHTML = message;
}

async function main() {
    let data = await fetchData(5, 75);
    let result = validateData(data);
    if (!result) {
        let message = 'Incorrect data came from the server. Try again';
        showMessageInsideTable(message);
    }
    else generateTable(data);
}

async function onButtonClick() {
    const size = document.getElementById('size-input').value;
    const concentration = document.getElementById('concentration-input').value;
    let data = await fetchData(size, concentration);
    let result = validateData(data);
    if (!result) {
        let message = 'Incorrect data came from the server. Try again';
        showMessageInsideTable(message);
    }
    else generateTable(data);
}

(() => {
    main();
})()
