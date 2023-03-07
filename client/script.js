const serverUrl = 'http://127.0.0.1:4567'

function fetchData(size, concentration) {
    return fetch(serverUrl + `/generateMatrix/${size}/${concentration}`)
        .then((res) => res.json())
        .then((data) => data);
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

async function main() {
    let data = await fetchData(5, 75);
    generateTable(data);
}

async function onButtonClick() {
    const size = document.getElementById('size-input').value;
    const concentration = document.getElementById('concentration-input').value;
    let data = await fetchData(size, concentration);
    generateTable(data);
}

(() => {
    main();
})()
