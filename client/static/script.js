const serverUrl = 'http://127.0.0.1:4567'

let currentMatrix;
let selected1 = {};
let selected2 = {};
let dijkstraBtn = document.getElementById('dijkstra-btn');
let infoText = document.getElementById('info-text');

socket = io.connect('http://' + document.domain + ':' + location.port + '/app');

socket.on('hoshen_kopelman', function(data) {
    if (!data) {
        let message = 'Incorrect data came from the server. Try again';
        showMessageInsideTable(message);
    } else {
        generateTable(data.matrix);
    }
});

socket.on('dijkstra', function(data) {
    generateMatrixWithHighlights(data);
});

function fetchData(type, size, concentration) {
    return fetch(serverUrl + `/${type}/${size}/${concentration}`)
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

function generateColor(value) {
    return '#' + (((value*470892)+148276)%999999)
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
                cell.style.backgroundColor = generateColor(data[i][j])
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

function findShortestWay() {
    fetch(serverUrl + '/shortest', {
        method: "POST",
        body: JSON.stringify({
            matrix: currentMatrix
        })
    })
        .then((json) => json.json())
        .then((res) => {
            generateMatrixWithHighlights(res);
        })
}

function onButtonDijkstraClick(x1, y1, x2, y2) {
    socket.emit('dijkstra', {
        x1,
        y1,
        x2,
        y2,
        matrix: JSON.stringify(currentMatrix)
    });
}

function generateMatrixWithHighlights(res) {
    let data = res["path"];
    selected1 = {};
    selected2 = {};
    generateTable(currentMatrix);
    let matrixWithHighlights = [];
    for (let item of currentMatrix) {
        matrixWithHighlights.push([...item]);
    }
    let redCounter = 0;
    let blackCounter = 0;
    let currentRedClusterLength = 0;
    let redLengths = [];

    for (let i = 0; i < data.length; i++) {
        if (matrixWithHighlights[data[i][0]][data[i][1]] === 1) {
            matrixWithHighlights[data[i][0]][data[i][1]] = 2;
            if (currentRedClusterLength > 0) {
                redLengths.push(currentRedClusterLength);
                currentRedClusterLength = 0;
            }
            blackCounter++;
        } else {
            currentRedClusterLength === 0 && (currentRedClusterLength = 1);
            if (i > 0 && matrixWithHighlights[data[i - 1][0]][data[i - 1][1]] === 3) {
                currentRedClusterLength++;
            }
            matrixWithHighlights[data[i][0]][data[i][1]] = 3;
            redCounter++;
        }
    }
    if (currentRedClusterLength > 0) {
        redLengths.push(currentRedClusterLength);
    }
    generateTable(matrixWithHighlights);
    infoText.innerHTML = `Черных: ${blackCounter}; Красных: ${redCounter}; Средняя длина красного кластера: ${(redLengths.reduce((sum, value) => sum + value, 0) / redLengths.length).toFixed(2)}; Стоимость пути: ${res["cost"]}`
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
    let data = await fetchData('generateMatrix', 15, 75);
    let result = validateData(data);
    if (!result) {
        let message = 'Incorrect data came from the server. Try again';
        showMessageInsideTable(message);
    } else {
        currentMatrix = data;
        generateTable(data);
    }
}

async function onButtonClick(type) {
    const size = document.getElementById('size-input').value;
    const concentration = document.getElementById('concentration-input').value;
    let data = await fetchData(type , size, concentration);
    let result = validateData(data);
    if (!result) {
        let message = 'Incorrect data came from the server. Try again';
        showMessageInsideTable(message);
    } else {
        currentMatrix = data;
        generateTable(data);
    }
}

async function onButtonHoshenKopelmanClick() {
    socket.emit('hoshen_kopelman', {matrix: JSON.stringify(currentMatrix)});
}

(() => {
    main();
})()
