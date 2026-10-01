import { assess, finalize } from "./core.mjs";

const $ = (id) => document.getElementById(id);
let caseData;
let evidence;
let approved = false;
let pack;

const stateCopy = {
  BLOCKED: ["Belum siap ditagihkan", "Bukti kritis masih perlu dilengkapi."],
  HUMAN_REVIEW: ["Perlu tinjauan manusia", "Ada bukti yang bertentangan atau perlu dikonfirmasi."],
  AWAITING_APPROVAL: ["Menunggu persetujuan", "Bukti lengkap; keputusan final menunggu koordinator."],
  BILLING_READY: ["Siap untuk billing (demo)", "Paket demo sudah disetujui dan dibuat."],
};

function render() {
  const result = assess(caseData, evidence, approved);
  const [name, explanation] = stateCopy[result.state];
  $("state-name").textContent = name;
  $("state-explain").textContent = explanation;
  $("ready-count").textContent = result.rows.filter((row) => row.status === "READY").length;
  $("blocker-count").textContent = result.blockers.length;
  $("requirement-summary").textContent = `${result.rows.length} PERSYARATAN`;
  $("requirements").replaceChildren(...result.rows.map((row, index) => {
    const item = document.createElement("article");
    item.className = "requirement";
    const rail = document.createElement("div");
    rail.className = `rail rail-${row.status.toLowerCase().replaceAll("_", "-")}`;
    const circle = document.createElement("span");
    circle.className = "rail-circle";
    circle.textContent = row.status === "READY" ? "✓" : String(index + 1);
    const stem = document.createElement("span");
    stem.className = "rail-stem";
    rail.append(circle, stem);
    const body = document.createElement("div");
    const title = document.createElement("h3"); title.className = "req-title"; title.textContent = row.description;
    const source = document.createElement("span"); source.className = "req-source"; source.textContent = `SUMBER: ${row.source_ref} · ${row.critical ? "KRITIS" : "PENDUKUNG"}`;
    const proof = document.createElement("p"); proof.className = "req-proof"; proof.textContent = row.evidence_ids.length ? `Bukti terkait: ${row.evidence_ids.join(", ")}` : "Belum ada bukti terkait.";
    const next = document.createElement("p"); next.className = "req-next"; next.textContent = row.status === "READY" ? "Persyaratan didukung bukti terstruktur." : row.next;
    body.append(title, source, proof, next);
    const status = document.createElement("span"); status.className = `status ${row.status.toLowerCase().replaceAll("_", "-")}`; status.textContent = row.status.replaceAll("_", " ");
    item.append(rail, body, status);
    return item;
  }));
  $("add-reading").disabled = evidence.some((item) => item.label === "cooling_reading") || approved;
  $("add-ack").disabled = evidence.some((item) => item.label === "customer_ack") || approved;
  const prerequisite = result.rows.every((row) => row.id === "REQ-SERVICE-REPORT" || !row.critical || row.status === "READY");
  $("finalize").disabled = !prerequisite || approved;
  $("finalize").title = prerequisite ? "" : "Lengkapi bukti kritis sebelum finalisasi";
  $("download").hidden = !pack;
}

async function init() {
  try {
    const response = await fetch(new URL("../demo/golden-case-WO-1028.json", import.meta.url));
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    caseData = await response.json();
    evidence = [...caseData.evidence];
    render();
  } catch (error) {
    $("state-name").textContent = "Data gagal dimuat";
    $("state-explain").textContent = "Jalankan dari root repositori: python3 -m http.server 8000, lalu buka /app/.";
    $("action-feedback").textContent = String(error);
  }
}

$("add-reading").addEventListener("click", () => {
  evidence.push({ id: "EV-004", type: "reading", label: "cooling_reading", value: 22, unit: "°C", synthetic: true });
  $("action-feedback").textContent = "Hasil ukur sintetis ditambahkan. Pemeriksaan diperbarui.";
  render();
});
$("add-ack").addEventListener("click", () => {
  evidence.push({ id: "EV-005", type: "acknowledgement", label: "customer_ack", confirmed: true, synthetic: true });
  $("action-feedback").textContent = "Konfirmasi pelanggan sintetis dicatat. Pemeriksaan diperbarui.";
  render();
});
$("finalize").addEventListener("click", () => {
  if (!$("confirm").checked) { $("approval-feedback").textContent = "Centang persetujuan setelah meninjau bukti."; return; }
  try {
    const output = finalize(caseData, evidence, $("approver").value);
    evidence = output.evidence; pack = output.pack; approved = true;
    $("approval-feedback").textContent = "Paket demo berhasil dibuat. Tidak ada data yang dikirim keluar.";
    render();
  } catch (error) { $("approval-feedback").textContent = error.message; }
});
$("download").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(pack, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a"); link.href = url; link.download = "proof2pay-WO-1028-demo-pack.json"; link.click();
  URL.revokeObjectURL(url);
});
init();
