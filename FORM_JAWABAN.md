# Jawaban siap salin · National Hackathon Project Submission Form

**Diperiksa 2 Oktober 2026.** Ini naskah untuk formulir resmi di <https://bit.ly/submit-hackathon>. Peserta mengisi dan mengirim formulir sendiri. Jawaban di bawah mengikuti kondisi proyek yang dapat dibuktikan; jangan menyatakan panggilan tool IBM Bob sudah berhasil.

## Halaman Informasi Tim dan Member 1

| Kolom | Isian |
|---|---|
| Informasi Tim | Individual |
| Team Member 1 — Full Name | Isi **nama lengkap sesuai pendaftaran dan sertifikat asli**. |
| Team Member 1 — Email | Isi email pendaftaran/akun yang benar. |
| Team Member 1 — University / Institution | Isi institusi sebenarnya. Walaupun kolom ini tidak bertanda wajib, halaman program menyebut peserta harus mahasiswa aktif D3–S3; pastikan data pendaftaran dan status Anda sesuai. |
| Team Member 1 — Phone Number | Isi nomor aktif yang benar. |
| Track — IBM SkillsBuild | Centang hanya track yang benar-benar diselesaikan. |
| Akun email IBM SkillsBuild | Isi email akun SkillsBuild yang sebenarnya. |
| Unggah Sertifikat IBM SkillsBuild | Unggah **sertifikat kelulusan kursus IBM SkillsBuild University Education yang asli** (maksimal 10 MB per file). Periksa berkas yang mungkin tersimpan dalam draf sebelum mengirim. |
| Daftar Nama Sertifikat | Centang hanya nama kursus yang sesuai sertifikat asli yang diunggah. |
| Project dikerjakan individu/tim | Individu |

**Dua sertifikat berbeda:** Formulir meminta bukti kelulusan *kursus IBM SkillsBuild University Education* saat submission. Pesan panitia menyatakan *Certificate of Participation Hackathon* diperoleh melalui submission. Jangan menunggu Certificate of Participation untuk mengirim, tetapi lampirkan sertifikat kursus asli yang diminta formulir.

## Halaman Project Overview

### Judul Project

PROOF2PAY AI — Evidence Readiness for Field-Service Billing

### Tema Project

Productivity & Smart Business

### Deskripsi Singkat Project (150–300 kata)

PROOF2PAY AI adalah prototipe untuk membantu tim layanan lapangan B2B memeriksa apakah pekerjaan yang dilaporkan selesai sudah memiliki bukti yang cukup sebelum diserahkan ke proses penagihan. Pengguna utamanya adalah koordinator operasional dan admin pada usaha servis, dimulai dari perawatan AC/HVAC. Saat ini catatan teknisi, foto, hasil ukur, persetujuan pelanggan, dan laporan akhir sering berada di tempat berbeda. Akibatnya, status “selesai” belum tentu berarti dokumen siap diperiksa oleh tim keuangan.

Pengguna membuka work order, melihat persyaratan penyelesaian, lalu membandingkannya dengan bukti yang tersedia. Prototipe menandai klaim yang belum didukung sebagai ambigu, menunjukkan bukti kritis yang hilang, dan memberi tindakan berikutnya. Status awal tetap terblokir; paket penyelesaian demo hanya dibuat setelah bukti kritis lengkap serta pengguna memberi persetujuan eksplisit. Empat flow Langflow menjalankan analisis, validasi, pembuatan paket, dan ringkasan kesiapan. Agent lokal dengan IBM Granite 3.3 2B memanggil tool review, sedangkan hasil akhirnya dijaga oleh aturan deterministik. Endpoint MCP dari Langflow sudah diuji langsung dan terhubung pada konfigurasi IBM Bob; pemanggilan tool melalui percakapan Bob belum terverifikasi.

Demo browser publik memakai work order sintetis agar dapat dicoba tanpa data pelanggan. Tiga work order publik NYC Parks juga diuji: meskipun berstatus “Completed”, sistem menolak menyebutnya siap tagih karena bukti kontrak, serah terima, dan persetujuan pelanggan tidak tersedia. Manfaat yang dituju ialah pemeriksaan yang lebih jelas, dapat ditelusuri, dan mengurangi bolak-balik pencarian bukti. Dampak waktu serta hasil bisnis masih perlu divalidasi dengan pengguna nyata.

### Problem Statement

Pada layanan lapangan, pekerjaan bisa ditandai selesai sebelum dokumen pendukung siap untuk pemeriksaan admin dan handoff penagihan. Catatan teknisi, foto, hasil ukur, laporan akhir, dan pengakuan pelanggan tersebar; klaim di catatan sering belum setara dengan bukti. Koordinator harus menelusuri kekurangan secara manual, dan tim keuangan belum memiliki alasan yang konsisten untuk menerima atau menunda paket pekerjaan. PROOF2PAY menargetkan celah antara status operasional “selesai” dan kesiapan bukti, tanpa mengklaim telah mengukur frekuensi atau biaya masalah pada pelanggan nyata.

### Target User

Pengguna utama: koordinator operasional dan admin pada UKM layanan lapangan B2B, terutama tim servis AC/HVAC. Pengguna terkait: teknisi yang melengkapi bukti dan admin keuangan yang menerima paket penyelesaian. Segmen ini adalah target validasi awal, belum pilot pelanggan.

### Mengapa Solusi Ini Dibutuhkan?

Pemeriksaan manual mudah kehilangan konteks saat bukti tersebar. Prototipe menghubungkan setiap persyaratan dengan bukti yang ditemukan, menyebut alasan penghambat, dan mengusulkan langkah perbaikan. Klaim teknisi tidak otomatis diterima; konflik dikirim ke tinjauan manusia. Pendekatan ini membuat keputusan demo dapat ditelusuri dan mencegah paket dibuat dari metadata “Completed” saja. Nilai produktivitasnya masih hipotesis yang akan diukur melalui pilot.

### Fitur Utama Project

1. **Evidence checklist** — memperlihatkan persyaratan penyelesaian dan status bukti per work order.
2. **Readiness review** — empat flow Langflow mengidentifikasi bukti yang hilang, ambigu, atau bertentangan dan memberi alasan serta tindakan berikutnya.
3. **Guarded AI Agent** — IBM Granite lokal memanggil tool review; output guard mempertahankan hasil terstruktur berbasis aturan ketika ringkasan model tidak didukung bukti.
4. **Human approval gate** — paket penyelesaian demo hanya dibuat setelah bukti kritis lengkap dan pemberi persetujuan dicatat.
5. **MCP tool interface** — empat tool Langflow ditemukan dan diuji langsung; konfigurasi IBM Bob menunjukkan koneksi MCP, sedangkan panggilan tool dari chat Bob masih menunggu verifikasi.

### Alur Penggunaan Project

Koordinator membuka work order → melihat catatan dan bukti → flow Langflow menganalisis klaim serta memvalidasi persyaratan → review menghasilkan status `BLOCKED`, `HUMAN_REVIEW`, atau kesiapan demo dengan alasan dan langkah berikutnya → pengguna melengkapi bukti yang kurang → manusia memberi persetujuan eksplisit → flow membuat paket penyelesaian demo. Pada rencana integrasi Bob, pengguna akan meminta ringkasan melalui Bob; Bob memanggil tool Langflow melalui MCP dan menampilkan hasil review untuk tindakan pengguna. Saat ini panggilan MCP telah diuji langsung, tetapi langkah chat Bob ke tool belum terverifikasi.

### Penggunaan IBM Langflow

Empat flow berbasis aturan berjalan di Langflow 1.12: `analyze_job_completion` menerima ID/catatan work order dan menandai klaim; `validate_completion_evidence` membandingkan bukti dengan persyaratan; `generate_completion_pack` menerapkan gerbang bukti serta persetujuan; `review_job_readiness` menyusun status, alasan, dan tindakan. Flow memakai komponen kustom Python, Prompt Template, serta input/output terstruktur. Flow Agent `agent_orchestration_local_granite` menjalankan IBM Granite 3.3 2B lokal melalui Ollama, memanggil tool review, lalu output guard memeriksa kembali hasilnya. Empat tool tersedia melalui endpoint MCP Langflow. Uji langsung: 13/13 skenario API, 5/5 MCP, dan 5/5 hasil akhir Agent lulus pada 2 Oktober 2026. Ini belum menguji akurasi AI membaca foto atau dokumen lapangan asli.

### Penggunaan IBM Bob

IBM Bob disiapkan sebagai antarmuka asisten bagi koordinator untuk meminta review work order dan memahami penghambat. Konfigurasi `.bob/mcp.json` mengarahkan Bob ke endpoint MCP Langflow lokal, dan layar Settings Bob menunjukkan server proyek berstatus `Connected`. Tool yang direncanakan untuk dipanggil ialah analisis, validasi, review, dan pembuatan paket demo. Output yang dituju adalah status kesiapan, alasan berbasis bukti, dan langkah perbaikan. **Batas implementasi saat submission:** pemanggilan tool dan jawaban melalui chat Bob belum berhasil diverifikasi; paket ini menunjukkan konsep integrasi serta koneksi MCP, bukan demo end-to-end Bob. Pengujian Bob akan dilanjutkan sebelum tahap final/mentoring sesuai pesan panitia.

### Bagaimana IBM Langflow dan IBM Bob Terintegrasi?

Hubungan teknisnya memakai MCP: Langflow mengekspor empat flow sebagai tool pada endpoint lokal; IBM Bob dikonfigurasi sebagai klien MCP melalui `.bob/mcp.json`. Bob akan menerima permintaan pengguna dan mengirim parameter work order ke tool review Langflow. Langflow mengembalikan status terstruktur, bukti, penghambat, dan tindakan berikutnya untuk ditampilkan Bob; pembuatan paket tetap dikunci oleh kelengkapan bukti serta persetujuan manusia. **Yang sudah terbukti:** endpoint MCP dapat menemukan dan menjalankan tool, serta server tampil `Connected` di Bob Settings. **Yang belum terbukti:** pemanggilan tool dari percakapan Bob dan responsnya. Karena itu integrasi end-to-end dinyatakan sebagai langkah berikutnya, bukan fitur yang sudah selesai.

### Project File / Link

https://github.com/apiipp-co/proof2pay-ai

Repository publik berisi README, kode prototipe, flow Langflow, dokumentasi, diagram, pitch deck, video, screenshot, dan laporan uji. Demo interaktif: <https://apiipp-co.github.io/proof2pay-ai/app/>. Video demo final (76 detik): <https://apiipp-co.github.io/proof2pay-ai/demo/proof2pay-demo-stage1-final.mp4>.

### Pitching Deck

Unggah berkas [`docs/02-pitch-deck-stage1-final.pdf`](docs/02-pitch-deck-stage1-final.pdf) (PDF, sekitar 585 KB). Salinan dengan nama sederhana tersedia di folder `FORM_UPLOADS_PROOF2PAY/`. Jangan tempel URL saja karena kolom ini meminta unggahan satu file.

### Project / Prototype Screenshot

Unggah 5 file pilihan pada folder `FORM_UPLOADS_PROOF2PAY/` di sebelah repository pada komputer peserta. Urutannya mencakup tampilan terblokir, flow review, empat MCP tools terkini, koneksi Bob, dan konfirmasi paket setelah persetujuan. Screenshot Bob hanya membuktikan status koneksi, bukan panggilan tool.

### Dampak yang Dihasilkan

Dampak yang diharapkan: koordinator lebih cepat menemukan bukti yang kurang, mengurangi bolak-balik antara teknisi dan admin, serta menyerahkan paket dengan alasan yang dapat ditelusuri. Metrik pilot yang akan diukur adalah waktu dari klaim selesai hingga berkas siap ditinjau, jumlah permintaan ulang bukti per work order, dan proporsi paket yang lolos pemeriksaan pertama. Saat ini belum ada pengukuran pada pelanggan. Bukti teknis yang tersedia: 13/13 skenario API Langflow, 5/5 MCP langsung, 5/5 keluaran akhir Agent terjaga, serta 4/4 tes browser pada 2 Oktober 2026; angka ini menunjukkan perilaku demo, bukan dampak bisnis.

### Potensi Pengembangan & Skalabilitas

Langkah berikutnya: verifikasi panggilan IBM Bob end-to-end; uji bersama koordinator layanan lapangan; dukung unggahan foto/dokumen dengan persetujuan dan evaluasi ekstraksi AI yang terpisah; tambah persyaratan per jenis pekerjaan; lalu sambungkan sistem work order yang sudah dipakai organisasi. Aturan dan jejak bukti perlu dijaga saat diperluas ke HVAC, perawatan fasilitas, instalasi, atau layanan lain. Hosting, keamanan data pelanggan, dan pengukuran dampak harus diselesaikan sebelum penggunaan produksi.

### Apa yang Membuat Project Ini Berbeda?

1. Fokus pada jeda antara “pekerjaan dilaporkan selesai” dan “bukti siap untuk handoff penagihan”, bukan sekadar daftar tugas.
2. Keputusan demo selalu memetakan persyaratan ke sumber bukti, alasan penghambat, serta langkah berikutnya; metadata `Completed` saja tidak cukup.
3. AI Agent ditempatkan di belakang validasi deterministik dan persetujuan manusia, sehingga ringkasan model yang keliru tidak membuka gerbang paket.

Ini diferensiasi rancangan yang dapat didemonstrasikan, bukan klaim bahwa semua produk pasar tidak memiliki fitur serupa.

### Kemampuan AI Agent

Flow Agent Langflow menggunakan IBM Granite 3.3 2B lokal untuk menerima permintaan review dan memanggil tool `review_job_readiness`. Dalam uji, panggilan tool terjadi dan hasil akhir terstruktur lolos 5/5 pemeriksaan. Agent membantu menyajikan status, penghambat, dan tindakan pada work order sintetis atau metadata publik. Output guard berbasis aturan mengabaikan ringkasan bebas model yang tidak didukung sumber; karena itu keputusan akhir tetap berasal dari validasi deterministik. Agent belum terbukti menilai foto/dokumen lapangan yang tidak terstruktur secara andal, dan tidak mengotorisasi invoice.

## Pemeriksaan sebelum Anda klik Kirim

1. Ganti semua identitas draf dengan data pendaftaran yang benar; periksa email, telepon, track, dan nama kursus.
2. Unggah sertifikat kelulusan kursus IBM SkillsBuild **asli**, pitch deck PDF, serta lima screenshot pilihan. Formulir menyebut batas 10 MB per file.
3. Pastikan tautan repository dan demo terbuka, serta pernyataan Bob tetap sesuai bukti.
4. Simpan bukti konfirmasi setelah formulir benar-benar dikirim. Beri tahu panitia status submit jika diperlukan.

**Pesan status singkat untuk panitia, bila Anda ingin membalas:** “Halo Kak, terima kasih atas pengingatnya. Project saya, PROOF2PAY AI, sudah siap untuk submission tahap ini dengan prototipe, dokumentasi, deck, dan flow Langflow. Integrasi Bob melalui MCP sudah terkoneksi tetapi panggilan tool lewat chat Bob masih saya lanjutkan untuk tahap berikutnya. Saya akan menyelesaikan pengisian formulir dan mengabari setelah terkirim.” Kirim hanya setelah sesuai keadaan sebenarnya.
