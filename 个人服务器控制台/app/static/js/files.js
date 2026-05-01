let currentPath = "/";
let parentPath = null;
let editPath = "";

const fileTableBody = document.getElementById("fileTableBody");
const currentPathEl = document.getElementById("currentPath");
const backBtn = document.getElementById("backBtn");
const refreshBtn = document.getElementById("refreshBtn");
const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");
const dropZone = document.getElementById("dropZone");
const newFolderBtn = document.getElementById("newFolderBtn");

const editorModalEl = document.getElementById("textEditorModal");
const previewModalEl = document.getElementById("previewModal");
const previewBody = document.getElementById("previewBody");
const editorFilePath = document.getElementById("editorFilePath");
const editorTextarea = document.getElementById("editorTextarea");
const saveTextBtn = document.getElementById("saveTextBtn");

const editorModal = new bootstrap.Modal(editorModalEl);
const previewModal = new bootstrap.Modal(previewModalEl);

function escapeHtml(text) {
  return String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

function fileActions(row) {
  if (row.is_dir) {
    return `<button class="btn btn-sm btn-outline-primary me-1 open-btn" data-path="${row.path}">打开</button>
      <button class="btn btn-sm btn-outline-secondary me-1 rename-btn" data-path="${row.path}" data-name="${escapeHtml(row.name)}">重命名</button>
      <button class="btn btn-sm btn-outline-danger delete-btn" data-path="${row.path}">删除</button>`;
  }

  let extra = "";
  if (row.type === "text") extra = `<button class="btn btn-sm btn-outline-success me-1 edit-btn" data-path="${row.path}">编辑</button>`;
  else if (row.type === "image") extra = `<button class="btn btn-sm btn-outline-success me-1 preview-btn" data-path="${row.path}">预览</button>`;

  return `<a class="btn btn-sm btn-outline-primary me-1" href="/api/files/download?path=${encodeURIComponent(row.path)}">下载</a>
      ${extra}
      <button class="btn btn-sm btn-outline-secondary me-1 rename-btn" data-path="${row.path}" data-name="${escapeHtml(row.name)}">重命名</button>
      <button class="btn btn-sm btn-outline-danger delete-btn" data-path="${row.path}">删除</button>`;
}

function renderTable(entries) {
  if (!entries.length) {
    fileTableBody.innerHTML = `<tr><td colspan="5" class="text-center text-secondary py-4">目录为空</td></tr>`;
    return;
  }

  fileTableBody.innerHTML = entries.map((row) => `<tr>
      <td>${row.is_dir ? "📁" : "📄"} ${escapeHtml(row.name)}</td>
      <td>${row.type}</td>
      <td>${row.is_dir ? "-" : fmtBytes(row.size)}</td>
      <td>${row.mtime}</td>
      <td>${fileActions(row)}</td>
    </tr>`).join("");
}

async function loadDir(path) {
  try {
    const data = await apiGet(`/api/files/list?path=${encodeURIComponent(path)}`);
    currentPath = data.current;
    parentPath = data.parent;
    currentPathEl.textContent = currentPath;
    renderTable(data.entries);
  } catch (err) { alert(err.message); }
}

async function uploadFiles(files) {
  if (!files || !files.length) return;
  const formData = new FormData();
  formData.append("path", currentPath);
  Array.from(files).forEach((f) => formData.append("files", f));

  const res = await fetch("/api/files/upload", { method: "POST", body: formData });
  const data = await res.json();
  if (!data.ok) { alert(data.message || "上传失败"); return; }
  loadDir(currentPath);
}

async function deletePath(path) {
  if (!window.confirm(`确认删除 ${path} ?`)) return;
  try { await apiPost("/api/files/delete", { path }); loadDir(currentPath); } catch (err) { alert(err.message); }
}

async function renamePath(path, oldName) {
  const name = window.prompt("请输入新名称", oldName);
  if (!name) return;
  try { await apiPost("/api/files/rename", { path, new_name: name }); loadDir(currentPath); } catch (err) { alert(err.message); }
}

async function createFolder() {
  const name = window.prompt("请输入新建文件夹名称");
  if (!name) return;
  try { await apiPost("/api/files/mkdir", { path: currentPath, name }); loadDir(currentPath); } catch (err) { alert(err.message); }
}

async function openTextEditor(path) {
  try {
    const data = await apiGet(`/api/files/read?path=${encodeURIComponent(path)}`);
    editPath = path;
    editorFilePath.textContent = path;
    editorTextarea.value = data.content || "";
    editorModal.show();
  } catch (err) { alert(err.message); }
}

async function saveText() {
  try { await apiPost("/api/files/write", { path: editPath, content: editorTextarea.value }); editorModal.hide(); loadDir(currentPath); }
  catch (err) { alert(err.message); }
}

function previewImage(path) {
  previewBody.innerHTML = `<img src="/api/files/raw?path=${encodeURIComponent(path)}" class="preview-image" alt="image preview">`;
  previewModal.show();
}

fileTableBody.addEventListener("click", (e) => {
  const target = e.target;
  if (target.classList.contains("open-btn")) loadDir(target.dataset.path);
  if (target.classList.contains("delete-btn")) deletePath(target.dataset.path);
  if (target.classList.contains("rename-btn")) renamePath(target.dataset.path, target.dataset.name);
  if (target.classList.contains("edit-btn")) openTextEditor(target.dataset.path);
  if (target.classList.contains("preview-btn")) previewImage(target.dataset.path);
});

backBtn.addEventListener("click", () => { if (parentPath) loadDir(parentPath); });
refreshBtn.addEventListener("click", () => loadDir(currentPath));
uploadBtn.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", () => uploadFiles(fileInput.files));
newFolderBtn.addEventListener("click", createFolder);
saveTextBtn.addEventListener("click", saveText);

dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.classList.add("dragover"); });
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));
dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  uploadFiles(e.dataTransfer.files);
});

loadDir("/");
