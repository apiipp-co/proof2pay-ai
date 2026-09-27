# Naskah submission · PROOF2PAY AI

**Status:** siap sebagai draf pengisian formulir, belum dikirim ke penyelenggara. Pemilik proyek mengonfirmasi bahwa peserta bekerja **sendiri**, tanpa tim. Nama lengkap peserta, URL GitHub, dan bukti persyaratan administrasi harus diisi dari data asli sebelum submit.

| Kolom | Isi |
|---|---|
| Nama proyek | PROOF2PAY AI |
| Nama peserta | **[Isi nama lengkap sesuai pendaftaran]** |
| Tim | Peserta individu / solo |
| Tema | Productivity & Smart Business |
| Tagline | Finish the job. Prove the job. Get paid. |
| Repository | **[Isi URL GitHub setelah diunggah]** |
| Video demo | `demo/proof2pay-demo.mp4` (104 detik, tanpa narasi; URL publik bila formulir meminta tautan) |
| Demo lokal | `python3 -m http.server 8000`, lalu `http://localhost:8000/app/` |

## Deskripsi singkat

PROOF2PAY AI membantu tim layanan lapangan B2B memeriksa apakah pekerjaan yang diklaim selesai sudah didukung bukti yang diperlukan untuk menyiapkan penagihan. Sistem menunjukkan persyaratan, bukti terkait, alasan penghambat, dan langkah perbaikan. Paket penyelesaian demo hanya dapat dibuat setelah bukti kritis lengkap dan manusia menyetujui.

## Masalah dan pengguna

Teknisi dapat menyatakan pekerjaan selesai, sementara admin operasional dan keuangan masih perlu mencari hasil ukur, foto, pengakuan pelanggan, atau laporan akhir. Informasi tersebar dan klaim penyelesaian belum tentu sama dengan bukti. Pengguna awal yang dituju ialah koordinator operasional/admin pada UKM layanan lapangan B2B, dimulai dari perawatan AC/HVAC. Kebutuhan dan dampak komersial masih merupakan hipotesis yang perlu diuji melalui wawancara pengguna nyata.

## Solusi dan alur demo

Kasus sintetis `WO-1028` dimulai dari catatan teknisi dan dua foto. Browser prototype dan flow Langflow memeriksa empat persyaratan terhadap bukti. Catatan “cooling test performed” diperlakukan sebagai klaim, sehingga hasil ukur pendinginan tetap `AMBIGUOUS`. Pengakuan pelanggan dan laporan akhir juga belum ada; status awal `BLOCKED`. Setelah hasil ukur dan pengakuan sintetis ditambahkan, laporan tetap menjadi penghambat. Pengguna memberi persetujuan eksplisit dan nama pemberi persetujuan sebelum paket demo dihasilkan. Bukti yang bertentangan menghasilkan `HUMAN_REVIEW`.

## Implementasi yang dapat dibuktikan

- Browser prototype lokal dengan empat tes Node yang lulus.
- Tiga flow Langflow 1.12 asli: `analyze_job_completion`, `validate_completion_evidence`, dan `generate_completion_pack`; JSON ekspor, tangkapan layar, dan kode komponen tersedia.
- Tujuh dari tujuh skenario API Langflow lulus pada kasus sintetis.
- Endpoint MCP proyek Langflow menampilkan tiga tool. Tiga dari tiga pemeriksaan MCP langsung lulus, termasuk satu panggilan validasi dan gate persetujuan.
- `.bob/mcp.json` berisi konfigurasi koneksi lokal untuk IBM Bob; Bob Settings menampilkan server proyek berstatus **Connected**. **Panggilan tool melalui Bob belum terverifikasi**. Pengaturan akun yang diperiksa menampilkan masa trial berakhir.
- Video layar 104 detik menunjukkan browser demo dan antarmuka Langflow; tanpa voiceover dan tanpa adegan Bob.

Artefak bukti: [status implementasi](IMPLEMENTATION_STATUS.md), [hasil evaluasi](evaluation/README.md), [ekspor Langflow](langflow/exports/), [laporan uji](langflow/runs/), [video](demo/proof2pay-demo.mp4), [pitch deck](docs/02-pitch-deck.pdf).

## Peran teknologi dan batas saat ini

Langflow menjalankan tiga workflow berbasis komponen aturan deterministik untuk satu work order sintetis. MCP menyediakan permukaan tool yang bisa ditemukan dan dipanggil klien. IBM Bob telah terhubung sebagai klien MCP pada workspace, tetapi pemilihan dan pemanggilan tool melalui chat Bob belum terbukti. Versi saat ini tidak melakukan inferensi model AI, membaca data pelanggan nyata, mengirim pesan, atau membuat invoice. Status `BILLING_READY_DEMO` adalah hasil simulasi, bukan otorisasi penagihan.

## Diferensiasi dan model bisnis

Fokus produk ialah celah antara “pekerjaan dilaporkan selesai” dan “bukti siap untuk handoff penagihan”. Nilai yang diuji: keputusan yang dapat ditelusuri dari persyaratan ke bukti, penghambat yang spesifik, dan langkah berikutnya yang jelas. Hipotesis model bisnis: perangkat lunak langganan untuk tim layanan lapangan, dengan harga dan kemasan produk ditentukan setelah validasi pelanggan. Tidak ada angka peningkatan produktivitas atau kesediaan membayar yang diklaim.

## Keamanan dan Responsible AI

Klaim teknisi tidak otomatis menjadi bukti. Persyaratan kritis yang hilang tetap memblokir paket; konflik meminta tinjauan manusia. Pembuatan paket membutuhkan persetujuan eksplisit dan identitas pemberi persetujuan. Sistem tidak mengesahkan tanda tangan, mengotorisasi invoice, mengirim komunikasi eksternal, atau memindahkan uang. Data demo sepenuhnya fiktif. Lihat [ResponsibleAI.md](ResponsibleAI.md).

## Sebelum menekan Submit

1. Isi nama lengkap peserta dan URL repository di tabel atas.
2. Unggah folder ini ke GitHub sesuai [panduan upload](GITHUB_UPLOAD.md); pastikan file tersembunyi `.bob/` ikut masuk.
3. Bila form meminta URL video, unggah `demo/proof2pay-demo.mp4` ke tempat yang dapat diakses juri, lalu ganti path lokal di tabel.
4. Periksa syarat formulir resmi, termasuk sertifikat/kehadiran Hackathon Class dan batas waktu. Lampirkan hanya bukti asli.
5. Jika integrasi Bob merupakan syarat penilaian, jalankan pengujian Bob sungguhan dan tambahkan bukti panggilan tool. Jangan menggunakan laporan MCP langsung sebagai pengganti bukti Bob.

Dokumen ini adalah naskah siap salin yang jujur terhadap implementasi tanggal 28 September 2026; penerimaan akhir ditentukan penyelenggara.
