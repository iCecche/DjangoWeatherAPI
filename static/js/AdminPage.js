const form = document.getElementById("apiForm");
const csrftoken = getCookie('csrftoken');
const tableContainer = document.getElementById('table-container');
const jsonView = document.getElementById('json-view');
let currentView = 'table';
let data = {};

const methodSelect = form.querySelector('select[name="method"]');
const idInput = document.getElementById('resource_id');

methodSelect.addEventListener("change", () => {
    const method = methodSelect.value.toUpperCase();
    if (["PUT", "PATCH", "DELETE"].includes(method)) {
        idInput.disabled = false;
    } else {
        idInput.disabled = true;
        idInput.value = "";
    }
});

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const method = form.method.value;
    const endpoint = form.endpoint.value;
    const resourceId = form.querySelector('[name="resource_id"]').value;
    const url = endpoint.startsWith("/")
        ? window.location.origin + endpoint + (resourceId ? `${resourceId}/` : "")
        : endpoint;
    const payload = form.payload.value;

    const options = {
        method: method,
        credentials: "same-origin", // ✅ invia i cookie della sessione Django!
        headers: {}
    };

    if (method !== "GET") {
        options.headers["Content-Type"] = "application/json";
        options.headers["X-CSRFToken"] = csrftoken;
    }
    if(payload && method !== "GET" && method !== "DELETE") {
        try {
            options.body = JSON.stringify(JSON.parse(payload));
        } catch (err) {
            return;
        }
    }
    try {
        const res = await fetch(url, options);
        data = await res.json();
        renderView();
    } catch (err) {

    }
});

function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : null;
}

function jsonToTable(json) {
    if (!json || (Array.isArray(json) && json.length === 0)) return "<p>No data available</p>";

    const dataArray = Array.isArray(json) ? json : [json];
    const headers = Object.keys(dataArray[0]);
    let table = '<table><thead><tr>' + headers.map(h => `<th>${h}</th>`).join('') + '</tr></thead><tbody>';
    table += dataArray.map(row => `<tr>${headers.map(h => `<td>${row[h]}</td>`).join('')}</tr>`).join('');
    table += '</tbody></table>';
    return table;
}

function renderView() {
    if (currentView === 'table') {
        tableContainer.innerHTML = jsonToTable(data);
        tableContainer.style.display = 'block';
        jsonView.style.display = 'none';
    } else {
        jsonView.textContent = JSON.stringify(data, null, 2);
        jsonView.style.display = 'block';
        tableContainer.style.display = 'none';
    }
}

function toggleView() {
    currentView = currentView === 'table' ? 'json' : 'table';
    renderView();
}

renderView();
