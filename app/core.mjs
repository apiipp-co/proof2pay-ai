// Deterministic, local demo rules. This module makes no AI or external-service claims.
export function assess(caseData, evidence, approved = false) {
  const has = (label) => evidence.some((item) => item.label === label);
  const rows = caseData.requirements.map((requirement) => {
    let status = "MISSING";
    let matched = [];
    let next = "Tambahkan bukti sesuai persyaratan.";
    if (requirement.id === "REQ-BEFORE-AFTER") {
      matched = evidence.filter((item) => ["before_photo", "after_photo"].includes(item.label));
      status = has("before_photo") && has("after_photo") ? "READY" : matched.length ? "INCOMPLETE" : "MISSING";
      next = "Unggah foto sebelum dan sesudah pekerjaan.";
    } else if (requirement.id === "REQ-COOLING-TEST") {
      matched = evidence.filter((item) => item.label === "cooling_reading" || item.label === "completion_note");
      const reading = evidence.find((item) => item.label === "cooling_reading");
      status = reading?.conflict ? "HUMAN_REVIEW" : reading && Number.isFinite(reading.value) && reading.unit ? "READY" : has("completion_note") ? "AMBIGUOUS" : "MISSING";
      next = status === "HUMAN_REVIEW" ? "Supervisor perlu meninjau pembacaan yang bertentangan." : "Tambahkan hasil ukur pascaservis beserta satuannya.";
    } else if (requirement.id === "REQ-CUSTOMER-ACK") {
      matched = evidence.filter((item) => item.label === "customer_ack");
      status = matched.some((item) => item.confirmed === true) ? "READY" : matched.length ? "HUMAN_REVIEW" : "MISSING";
      next = "Minta konfirmasi pelanggan dan catat sumbernya.";
    } else if (requirement.id === "REQ-SERVICE-REPORT") {
      matched = evidence.filter((item) => item.label === "service_report");
      status = matched.length ? "READY" : "MISSING";
      next = "Setujui pembuatan laporan final dari fakta terverifikasi.";
    }
    return { ...requirement, status, evidence_ids: matched.map((item) => item.id), next };
  });
  const unresolved = rows.filter((row) => row.critical && row.status !== "READY");
  const review = unresolved.some((row) => row.status === "HUMAN_REVIEW");
  const state = review ? "HUMAN_REVIEW" : unresolved.length ? "BLOCKED" : approved ? "BILLING_READY" : "AWAITING_APPROVAL";
  return { job_id: caseData.job.job_id, state, rows, blockers: unresolved.map((row) => row.id), approved, synthetic: true };
}

export function finalize(caseData, evidence, approver) {
  if (typeof approver !== "string" || !approver.trim()) throw new Error("Nama pemberi persetujuan wajib diisi.");
  const before = assess(caseData, evidence);
  const nonReportBlockers = before.rows.filter((row) => row.critical && row.id !== "REQ-SERVICE-REPORT" && row.status !== "READY");
  if (nonReportBlockers.length) throw new Error("Bukti kritis belum lengkap; paket tidak dapat difinalisasi.");
  const report = {
    id: "EV-REPORT-DEMO",
    type: "report",
    label: "service_report",
    synthetic: true,
    approved_by: approver.trim(),
  };
  const nextEvidence = evidence.some((item) => item.label === "service_report") ? evidence : [...evidence, report];
  const result = assess(caseData, nextEvidence, true);
  if (result.state !== "BILLING_READY") throw new Error("Pemeriksaan akhir gagal.");
  return {
    result,
    evidence: nextEvidence,
    pack: {
      demo_only: true,
      job_id: caseData.job.job_id,
      customer: caseData.job.customer,
      service_type: caseData.job.service_type,
      technician_claim_unverified: caseData.technician_note,
      evidence_ids: nextEvidence.map((item) => item.id),
      requirement_results: result.rows.map(({ id, status, source_ref, evidence_ids }) => ({ id, status, source_ref, evidence_ids })),
      approved_by: approver.trim(),
      status: "BILLING_READY_DEMO",
      disclaimer: "Data sintetis untuk demonstrasi. Tidak mengirim invoice atau dokumen ke pelanggan.",
    },
  };
}
