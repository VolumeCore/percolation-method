const serverUrl = 'http://127.0.0.1:4567'
let currentMatrix;
let selected1 = {};
let selected2 = {};
let dijkstraBtn = document.getElementById('dijkstra-btn');
let infoText = document.getElementById('info-text');

function fetchData(size, concentration) {
    return fetch(serverUrl + `/generateMatrix/${size}/${concentration}`)
        .then((res) => res.json())
        .then((data) => {
            return data;
        });
}

function validateData(data) {
    let result = Array.isArray(data);
    if (result) {
        return isSquareMatrix(data)
    } else {
        return false;
    }
}

function isSquareMatrix(matrix) {
    let rows = matrix.length;

    for (let i = 0; i < matrix.length; i++) {
        let columns = matrix[i].length;
        if (rows !== columns) {
            return false;
        }
    }
    return true;
}

function generateTable(data) {
    infoText.innerHTML = "";
    let percolationTable = document.getElementById('percolation-table');
    percolationTable.innerHTML = "";
    dijkstraBtn.setAttribute('disabled', 'true');
    for (let i = 0; i < data.length; i++) {
        let tableRow = percolationTable.insertRow();
        for (let j = 0; j < data[i].length; j++) {
            let cell = tableRow.insertCell();
            if (!!data[i][j]) {
                cell.classList.add('_blue');
            }
            if (i === 0 || i === data.length - 1) { // всё в фигурных скобках - алгоритм дейкстры
                cell.classList.add('_clickable');
                cell.addEventListener('click', () => {
                    if (cell.classList.contains('_selected')) {
                        cell.classList.remove('_selected');
                        if (i === 0) {
                            selected1 = {};
                        }
                        if (i === data.length - 1) {
                            selected2 = {};
                        }
                        dijkstraBtn.setAttribute('disabled', 'true');
                        return;
                    }
                    if (i === 0) {
                        selected1 = {x: i, y: j};
                        for (let cell of percolationTable.firstChild.firstChild.childNodes) {
                            cell.classList.remove('_selected')
                        }
                    } else {
                        selected2 = {x: i, y: j};
                        for (let cell of percolationTable.firstChild.lastChild.childNodes) {
                            cell.classList.remove('_selected')
                        }
                    }
                    cell.classList.add('_selected');

                    if (!!Object.keys(selected1).length && !!Object.keys(selected2).length) {
                        dijkstraBtn.removeAttribute('disabled');
                    } else {
                        dijkstraBtn.setAttribute('disabled', 'true');
                    }
                })
            }
            if (data[i][j] === 2) { // для алгоритма дейкстры
                cell.classList.add('_darkgray');
            }
            if (data[i][j] === 3) { // для алгоритма дейкстры
                cell.classList.add('_red');
            }
        }
    }
    let containerElem = document.querySelector('.percolation-method');
    containerElem.insertBefore(percolationTable, containerElem.lastChild);
}

function dijkstra() {
    fetch(serverUrl + '/dijkstra', {
        method: "POST",
        body: JSON.stringify({
            x1: selected1.x,
            y1: selected1.y,
            x2: selected2.x,
            y2: selected2.y,
            matrix: currentMatrix
        })
    })
        .then((json) => json.json())
        .then((data) => {
            selected1 = {};
            selected2 = {};
            generateTable(currentMatrix);
            if (!data.length) {
                infoText.innerHTML = "Нет такого пути";
                return;
            } else {
                infoText.innerHTML = "";
            }
            let matrixWithHighlights = [];
            for (let item of currentMatrix) {
                matrixWithHighlights.push([...item]);
            }
            for (let item of data) {
                matrixWithHighlights[item[0]][item[1]] = matrixWithHighlights[item[0]][item[1]] === 1 ? 2 : 3;
            }
            generateTable(matrixWithHighlights);
        })
}

function showMessageInsideTable(message) {
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
    } else {
        currentMatrix = data;
        generateTable(data);
    }
}

async function onButtonClick() {
    const size = document.getElementById('size-input').value;
    const concentration = document.getElementById('concentration-input').value;
    let data = await fetchData(size, concentration);
    let result = validateData(data);
    if (!result) {
        let message = 'Incorrect data came from the server. Try again';
        showMessageInsideTable(message);
    } else {
        currentMatrix = data;
        generateTable(data);
    }
}

(() => {
    main();
})()
