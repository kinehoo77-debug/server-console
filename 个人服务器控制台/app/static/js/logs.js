const logContent = document.getElementById("logContent");
const logPath = document.getElementById("logPath");
const logSearch = document.getElementById("logSearch");
const logRefreshBtn = document.getElementById("logRefreshBtn");
const logClearBtn = document.getElementById("logClearBtn");

async function loadLogs() {
  const search = logSearch.value.trim();
  try {
    const data = await apiGet(`/api/logs?lines=500&search=${encodeURIComponent(search)}`);
    logPath.textContent = data.path || "-";
    logContent.textContent = data.content || "(无日志)";
    logContent.scrollTop = logContent.scrollHeight;
  } catch (err) {
    logContent.textContent = err.message;
  }
}

logRefreshBtn.addEventListener("click", loadLogs);
logClearBtn.addEventListener("click", () => { logContent.textContent = ""; });
logSearch.addEventListener("keydown", (e) => { if (e.key === "Enter") loadLogs(); });

loadLogs();
setInterval(loadLogs, 4000);
