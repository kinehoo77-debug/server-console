(function () {
  const clock = document.getElementById("clock");
  if (!clock) return;
  const render = () => {
    const now = new Date();
    clock.textContent = now.toLocaleString("zh-CN", { hour12: false });
  };
  render();
  setInterval(render, 1000);
})();

function fmtBytes(size) {
  const units = ["B", "KB", "MB", "GB", "TB"];
  let value = Number(size || 0);
  let idx = 0;
  while (value >= 1024 && idx < units.length - 1) {
    value /= 1024;
    idx += 1;
  }
  return `${value.toFixed(1)} ${units[idx]}`;
}

async function apiGet(url) {
  const res = await fetch(url);
  const data = await res.json();
  if (!data.ok) throw new Error(data.message || "请求失败");
  return data;
}

async function apiPost(url, payload) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload || {}),
  });
  const data = await res.json();
  if (!data.ok) throw new Error(data.message || "请求失败");
  return data;
}
