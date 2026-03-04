/* ============================
        DASHBOARD STATUS
============================ */

async function loadStatus() {
    try {
        const res = await fetch("/api/status");
        const data = await res.json();

        const engineCard = document.getElementById("engineStatus");
        const quarantineCard = document.getElementById("quarantineCount");

        if (engineCard) {
            engineCard.innerHTML = `
                <h3>⚙ Engine Status</h3>
                <p><b>Engine:</b> ${data.engine}</p>
                <p><b>Status:</b> 
                    <span class="${data.status === "Running" ? "green" : "red"}">
                        ${data.status}
                    </span>
                </p>
            `;
        }

        if (quarantineCard) {
            quarantineCard.innerHTML = `
                <h3>🗂 Quarantined Files</h3>
                <p class="big-number">${data.quarantined}</p>
            `;
        }

    } catch (err) {
        console.error("Status Load Error:", err);
    }
}

if (document.getElementById("engineStatus")) {
    loadStatus();
    setInterval(loadStatus, 5000); // auto refresh
}


/* ============================
        DARK MODE
============================ */

const darkToggle = document.getElementById("darkToggle");

if (darkToggle) {
    darkToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark");
        localStorage.setItem("darkMode",
            document.body.classList.contains("dark"));
    });

    // load saved preference
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark");
    }
}


/* ============================
        UPDATE SYSTEM
============================ */

const updateBtn = document.getElementById("updateBtn");

if (updateBtn) {
    updateBtn.addEventListener("click", async () => {
        updateBtn.innerText = "Updating...";
        updateBtn.disabled = true;

        try {
            await fetch("/api/update", { method: "POST" });
            alert("Signatures updated successfully!");
        } catch {
            alert("Update failed.");
        }

        updateBtn.innerText = "🔄 Check Updates";
        updateBtn.disabled = false;
    });
}


/* ============================
        FILE SCAN
============================ */

if (document.querySelector(".choose-btn")) {
    document.querySelector(".choose-btn").onclick = () => {
        document.getElementById("fileInput").click();
    };
}

if (document.getElementById("fileInput")) {
    document.getElementById("fileInput").onchange = function () {
        let file = this.files[0];
        document.getElementById("fileName").textContent =
            file ? file.name : "No file chosen";
    };
}

async function scanFile() {
    let fileInput = document.getElementById("fileInput");
    let output = document.getElementById("scanOutput");

    if (!fileInput || fileInput.files.length === 0) {
        alert("Please select a file first.");
        return;
    }

    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append("file", file);

    output.innerHTML = `
        <div class="loading-spinner"></div>
        <p>Scanning file...</p>
    `;

    try {
        const res = await fetch("/api/scan", {
            method: "POST",
            body: formData
        });

        const result = await res.json();

        if (result.status === "infected") {
            output.innerHTML = `
                <div class="result-card danger">
                    <h3>⚠ Threat Detected</h3>
                    <p><b>File:</b> ${file.name}</p>
                    <p><b>Threat:</b> ${result.threat}</p>
                </div>
            `;
        } else {
            output.innerHTML = `
                <div class="result-card safe">
                    <h3>✅ File Safe</h3>
                    <p>${file.name} is clean.</p>
                </div>
            `;
        }

        loadStatus(); // refresh dashboard

    } catch (err) {
        console.error("Scan Error:", err);
        output.innerHTML = `
            <div class="result-card danger">
                <h3>❌ Scan Failed</h3>
                <p>Check backend logs.</p>
            </div>
        `;
    }
}


/* ============================
        REAL-TIME PROCESS MONITOR
============================ */

async function loadProcesses() {
    try {
        const res = await fetch("/api/processes");
        const processes = await res.json();

        const table = document.getElementById("processTable");
        if (!table) return;

        table.innerHTML = "";

        processes.forEach(p => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${p.pid}</td>
                <td>${p.name}</td>
                <td>${p.cpu}%</td>
            `;
            table.appendChild(row);
        });

    } catch (err) {
        console.error("Process Monitor Error:", err);
    }
}

if (document.getElementById("processTable")) {
    loadProcesses();
    setInterval(loadProcesses, 3000);
}


/* ============================
        QUARANTINE
============================ */

async function loadQuarantine() {
    try {
        const res = await fetch("/api/quarantine");
        const items = await res.json();

        let ul = document.getElementById("quarantineList");
        if (!ul) return;

        ul.innerHTML = "";

        items.forEach(i => {
            let li = document.createElement("li");
            li.textContent = i;
            ul.appendChild(li);
        });

    } catch (err) {
        console.error("Quarantine Load Error:", err);
    }
}
if (document.getElementById("quarantineList")) loadQuarantine();


/* ============================
            LOGS
============================ */

async function loadLogs() {
    try {
        const res = await fetch("/api/logs");
        const logs = await res.json();

        let logDiv = document.getElementById("logData");
        if (!logDiv) return;

        logDiv.innerHTML = logs.map(l =>
            `<div class="log-entry">${l}</div>`
        ).join("");

    } catch (err) {
        console.error("Logs Error:", err);
    }
}
if (document.getElementById("logData")) loadLogs();

/* ============================
        CHECK UPDATES
============================ */
const updateBtn = document.getElementById("updateBtn");

if (updateBtn) {
    updateBtn.onclick = async () => {
        updateBtn.innerText = "Checking...";

        try {
            const res = await fetch("/api/update");
            const data = await res.json();

            if (data.status === "updated") {
                alert("Updated to version " + data.new_version);
            } else if (data.status === "already_latest") {
                alert("Already up to date!");
            } else {
                alert("Update failed.");
            }

        } catch (err) {
            alert("Update error.");
        }

        updateBtn.innerText = "🔄 Check Updates";
    };
}
