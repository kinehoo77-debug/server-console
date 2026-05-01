const cpuValueEl = document.getElementById("cpuValue");
const memValueEl = document.getElementById("memValue");
const diskValueEl = document.getElementById("diskValue");
const netValueEl = document.getElementById("netValue");

const cpuLineChart = echarts.init(document.getElementById("cpuLineChart"));
const memoryPieChart = echarts.init(document.getElementById("memoryPieChart"));
const diskPieChart = echarts.init(document.getElementById("diskPieChart"));

const cpuPoints = [];
const timePoints = [];
let prevNet = null;
let prevTs = null;

function renderCpuChart() {
  cpuLineChart.setOption({
    grid: { left: 34, right: 14, top: 20, bottom: 30 },
    xAxis: { type: "category", boundaryGap: false, data: timePoints, axisLabel: { color: "#726e98" } },
    yAxis: { type: "value", max: 100, axisLabel: { color: "#726e98", formatter: "{value}%" } },
    series: [{ data: cpuPoints, type: "line", smooth: true, showSymbol: false, lineStyle: { width: 3, color: "#7a63e6" }, areaStyle: { color: "rgba(122,99,230,0.15)" } }],
    tooltip: { trigger: "axis" },
  });
}

function renderPie(chart, usedPercent, title) {
  chart.setOption({
    title: { text: `${usedPercent}%`, left: "center", top: "44%", textStyle: { color: "#4d4770", fontSize: 24 } },
    tooltip: { trigger: "item" },
    series: [{ name: title, type: "pie", radius: ["62%", "82%"], label: { show: false }, data: [
      { value: usedPercent, name: "已用", itemStyle: { color: "#7a63e6" } },
      { value: Math.max(0, 100 - usedPercent), name: "剩余", itemStyle: { color: "#ede8ff" } },
    ] }],
  });
}

async function loadSystemInfo() {
  try {
    const data = await apiGet("/api/system/info");
    const info = data.info;
    document.getElementById("infoIp").textContent = info.ip;
    document.getElementById("infoOs").textContent = `${info.os} (${info.version})`;
    document.getElementById("infoUptime").textContent = info.uptime;
    document.getElementById("infoLoad").textContent = info.load;
  } catch (err) {
    console.error(err);
  }
}

async function loadMetrics() {
  try {
    const data = await apiGet("/api/system/metrics");
    const m = data.metrics;

    cpuValueEl.textContent = `${m.cpu_percent}%`;
    memValueEl.textContent = `${m.memory_percent}%`;
    diskValueEl.textContent = `${m.disk_percent}%`;

    const label = new Date().toLocaleTimeString("zh-CN", { hour12: false });
    timePoints.push(label);
    cpuPoints.push(m.cpu_percent);
    if (timePoints.length > 20) {
      timePoints.shift();
      cpuPoints.shift();
    }

    renderCpuChart();
    renderPie(memoryPieChart, m.memory_percent, "内存");
    renderPie(diskPieChart, m.disk_percent, "磁盘");

    if (prevNet !== null && prevTs !== null) {
      const intervalSec = Math.max((m.timestamp - prevTs) / 1000, 1);
      const deltaRecv = m.net_recv - prevNet.recv;
      const deltaSent = m.net_sent - prevNet.sent;
      const speed = (Math.max(0, deltaRecv) + Math.max(0, deltaSent)) / intervalSec;
      netValueEl.textContent = `${fmtBytes(speed)}/s`;
    }

    prevNet = { recv: m.net_recv, sent: m.net_sent };
    prevTs = m.timestamp;
  } catch (err) {
    console.error(err);
  }
}

window.addEventListener("resize", () => {
  cpuLineChart.resize();
  memoryPieChart.resize();
  diskPieChart.resize();
});

loadSystemInfo();
loadMetrics();
setInterval(loadSystemInfo, 15000);
setInterval(loadMetrics, 2500);
