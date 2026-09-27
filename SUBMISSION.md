# Naskah submission · PROOF2PAY AI

**Status:** siap sebagai draf pengisian formulir, belum dikirim ke penyelenggara. Pemilik proyek mengonfirmasi bahwa peserta bekerja **sendiri**, tanpa tim. Nama lengkap peserta dan bukti persyaratan administrasi harus diisi dari data asli sebelum submit.

| Kolom | Isi |
|---|---|
| Nama proyek | PROOF2PAY AI |
| Nama peserta | **[Isi nama lengkap sesuai pendaftaran]** |
| Tim | Peserta individu / solo |
| Tema | Productivity & Smart Business |
| Tagline | Finish the job. Prove the job. Get paid. |
| Repository | [github.com/apiipp-co/proof2pay-ai](https://github.com/apiipp-co/proof2pay-ai) |
| Video demo | `demo/proof2pay-demo.mp4` (104 detik, tanpa narasi; URL publik bila formulir meminta tautan) |
| Demo lokal | `python3 -m http.server 8000`, lalu `http://localhost:8000/app/` |

## Deskripsi singkat

PROOF2PAY AI membantu tim layanan lapangan B2B memeriksa apakah pekerjaan yang diklaim selesai sudah didukung bukti yang diperlukan untuk menyiapkan penagihan. Sistem menunjukkan persyaratan, bukti terkait, alasan penghambat, dan langkah perbaikan. Paket penyelesaian demo hanya dapat dibuat setelah bukti kritis lengkap dan manusia menyetujui.

## Masalah dan pengguna

Teknisi dapat menyatakan pekerjaan selesai, sementara admin operasional dan keuangan masih perlu mencari hasil ukur, foto, pengakuan pelanggan, atau laporan akhir. Informasi tersebar dan klaim penyelesaian belum tentu sama dengan bukti. Pengguna awal yang dituju ialah koordinator operasional/admin pada UKM layanan lapangan B2B, dimulai dari perawatan AC/HVAC. Kebutuhan dan dampak komersial masih merupakan hipotesis yang perlu diuji melalui wawancara pengguna nyata.

## Solusi dan alur demo

Kasus sintetis `WO-1028` dimulai dari catatan teknisi dan dua foto. Browser prototype dan flow Langflow memeriksa empat persyaratan terhadap bukti. Catatan “cooling test performed” diperlakukan sebagai klaim, sehingga hasil ukur pendinginan tetap `AMBIGUOUS`. Pengakuan pelanggan dan laporan akhir juga belum ada; status awal `BLOCKED`. Setelah hasil ukur dan pengakuan sintetis ditambahkan, laporan tetap menjadi penghambat. Pengguna memberi persetujuan eksplisit dan nama pemberi persetujuan sebelum paket demo dihasilkan. Bukti yang bertentangan menghasilkan `HUMAN_REVIEW`.

Selain simulasi, flow Langflow menerima tiga ID work order **asli dari NYC Parks AMPS**: `2791739` (pemasangan AC), `2792582` (inspeksi pendingin/pemanas), dan `2792861` (perbaikan unit HVAC). Field sumber, waktu pengambilan, query API, serta checksum ada di [data publik](data/README.md). Misalnya, input `{"job_id":"2792861"}` mengembalikan deskripsi dan status `Completed` yang diterbitkan portal resmi. Validator tetap menghasilkan `INSUFFICIENT_EVIDENCE`, sebab catatan publik yang dipilih tidak menyediakan kontrak, dokumen penyelesaian, atau persetujuan pelanggan. Flow menolak pembuatan paket penagihan dari metadata tersebut.

## Implementasi yang dapat dibuktikan

- Browser prototype lokal dengan empat tes Node yang lulus.
- Empat flow Langflow 1.12 yang berjalan: `analyze_job_completion`, `validate_completion_evidence`, `generate_completion_pack`, dan `review_job_readiness`. Flow kelima, `agent_orchestration_requires_model`, memiliki node Agent, prompt, dan tiga tool yang terhubung tetapi memerlukan model sebelum bisa dijalankan. JSON ekspor, tangkapan layar, dan kode komponen tersedia.
- Tiga belas dari tiga belas skenario API Langflow lulus: delapan pada kasus sintetis, lima pada data publik asli dan pembatasan klaimnya.
- Endpoint MCP proyek Langflow menampilkan empat tool. Lima dari lima pemeriksaan MCP langsung lulus, termasuk review work order publik.
- `.bob/mcp.json` berisi konfigurasi koneksi lokal untuk IBM Bob; Bob Settings menampilkan server proyek berstatus **Connected**. **Panggilan tool melalui Bob belum terverifikasi**.
- Video layar 104 detik menunjukkan browser demo dan antarmuka Langflow; tanpa voiceover dan tanpa adegan Bob.

Artefak bukti: [status implementasi](IMPLEMENTATION_STATUS.md), [hasil evaluasi](evaluation/README.md), [ekspor Langflow](langflow/exports/), [laporan uji](langflow/runs/), [video](demo/proof2pay-demo.mp4), [pitch deck](docs/02-pitch-deck.pdf).

## Peran teknologi dan batas saat ini

Langflow menjalankan empat workflow berbasis komponen aturan deterministik untuk satu work order sintetis dan tiga catatan publik asli. Flow Agent native yang terpisah sudah terhubung ke tool analisis, validasi, dan pembuatan paket, tetapi belum dapat menjalankan inferensi karena model belum dipilih. MCP menyediakan empat tool yang bisa ditemukan dan dipanggil klien. IBM Bob telah terhubung sebagai klien MCP pada workspace, tetapi pemilihan dan pemanggilan tool melalui chat Bob belum terbukti. Versi yang berjalan saat ini tidak melakukan inferensi model AI, membaca data pelanggan privat, mengirim pesan, atau membuat invoice. Status `BILLING_READY_DEMO` hanya berlaku untuk simulasi, bukan otorisasi penagihan. Catatan NYC Parks bukan pilot pelanggan Indonesia dan tidak membuktikan dampak bisnis.

## Diferensiasi dan model bisnis

Fokus produk ialah celah antara “pekerjaan dilaporkan selesai” dan “bukti siap untuk handoff penagihan”. Nilai yang diuji: keputusan yang dapat ditelusuri dari persyaratan ke bukti, penghambat yang spesifik, dan langkah berikutnya yang jelas. Hipotesis model bisnis: perangkat lunak langganan untuk tim layanan lapangan, dengan harga dan kemasan produk ditentukan setelah validasi pelanggan. Tidak ada angka peningkatan produktivitas atau kesediaan membayar yang diklaim.

## Keamanan dan Responsible AI

Klaim teknisi tidak otomatis menjadi bukti. Persyaratan kritis yang hilang tetap memblokir paket; konflik meminta tinjauan manusia. Pembuatan paket sintetis membutuhkan persetujuan eksplisit dan identitas pemberi persetujuan. Sistem tidak mengesahkan tanda tangan, mengotorisasi invoice, mengirim komunikasi eksternal, atau memindahkan uang. Skenario browser `WO-1028` fiktif; tiga work order NYC Parks adalah metadata operasional asli dengan sumber yang dapat diperiksa. Tidak ada foto, tanda tangan, hasil ukur, atau hasil penagihan yang dikarang untuk ketiga work order asli tersebut. Lihat [ResponsibleAI.md](ResponsibleAI.md).

## Sebelum menekan Submit

1. Isi nama lengkap peserta di tabel atas sesuai pendaftaran.
2. Buka [repository publik](https://github.com/apiipp-co/proof2pay-ai) dan pastikan tautan dokumen, video, serta ekspor Langflow dapat diakses. Lihat [catatan publikasi](GITHUB_UPLOAD.md).
3. Bila form meminta URL video, unggah `demo/proof2pay-demo.mp4` ke tempat yang dapat diakses juri, lalu ganti path lokal di tabel.
4. Periksa syarat formulir resmi, termasuk sertifikat/kehadiran Hackathon Class dan batas waktu. Lampirkan hanya bukti asli.
5. Jika integrasi Bob merupakan syarat penilaian, jalankan pengujian Bob sungguhan dan tambahkan bukti panggilan tool. Jangan menggunakan laporan MCP langsung sebagai pengganti bukti Bob.

Dokumen ini adalah naskah siap salin yang jujur terhadap implementasi tanggal 28 September 2026; penerimaan akhir ditentukan penyelenggara.
