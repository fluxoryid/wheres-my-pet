# Where’s My Pet? — FPS + GLB

Game Three.js berbahasa Indonesia, tanpa build step. Sajikan `dist/` melalui HTTP(S).

## Dunia dan kontrol

- Luas tepat 1.000 × 1.000 unit: X dan Z −500…500. Unit Three.js tidak otomatis berarti meter.
- First-person: kamera setinggi mata, WASD relatif arah pandang, Shift berlari, mouse via Pointer Lock; drag-look tersedia untuk sentuh/browser tanpa Pointer Lock. Esc membebaskan mouse. E atau klik bidikan untuk informasi objek; scroll/+− memberi zoom optik.
- Pemain menggerakkan karakter sendiri. Tidak ada orbit, teleport atau jalan otomatis. City Map hanya menandai tujuan.
- Enam tema dalam 50 level prosedural. Seed mengacak permutasi 50 profil hewan tanpa pengulangan profil, susunan distrik, tinggi gedung, rumah pemilik, rute, hadiah dan waktu.
- Kantor pencakar langit, perumahan, toko, pasar malam, kebun, taman, bunga, rumput, pedestrian, jalan, empat jembatan, sungai berarus. Dasar sungai Y −23, air Y −5.
- 110 kendaraan, 160 warga termasuk 24 pemancing. Waktu riil Asia/Jakarta (WIB), empat fase pencahayaan; langit menghasilkan environment map untuk material PBR.

## Model GLB

`dist/models/manifest.json` memuat 62 aset GLB standalone: 50 profil hewan, tiga manusia, sedan, gedung kantor, rumah, toko, bangku, bunga, lampu, air dan pohon.

Material PBR, geometri, tekstur yang tersedia dan animasi tersimpan dalam GLB. Runtime memakai GLTFLoader; instancing untuk bangunan/properti dan pembatasan jarak/jumlah untuk pohon dan warga. Manusia berjalan memakai animation clips GLB; hewan memiliki animasi sesuai anatomi.

Manusia dan hewan dibuat secara prosedural dengan bentuk lebih rinci, belum setara karakter fotorealistis hasil scan. Pohon memakai Tree Small 02 bertekstur dari Poly Haven (CC0), dengan optimasi geometri/tekstur. Lisensi/sumber: `dist/models/LICENSES.md`. Builder: `scripts/build-models.mjs`.

Galeri `models.html` memuat file yang sama, mendukung putar/zoom, animasi, dan unduh setiap GLB.

## Misi

PetNet fiktif, brosur pohon/rumah/tiang dan percakapan warga memberi potret render 3D, ciri khas, lokasi dan waktu laporan. Hewan berhenti lalu berpindah; laporan lama dapat kedaluwarsa. Digital map melacak lokasi aktual, anjing pelacak memperbarui jejak.

Ambil hewan dari jarak ≤15 unit dan antar ke pemilik ≤22 unit. Jika pencarian habis, hewan masuk truk. Pengait gratis membuka kandang dalam 18 detik; pemotong 3 detik; las 6 detik. Menjauh membatalkan pembukaan. Setelah bebas, tersedia 120 detik mengantar sebelum patroli menangkap pembawa hewan. Ada kondisi menang, gagal, ulang, reward acak, serta sembilan peralatan fungsional. Progres solo disimpan di localStorage.

## Multiplayer

Trystero v0.22.0 MQTT memakai relay publik untuk signaling terenkripsi dan WebRTC data channels untuk data permainan. Buat ruang dan bagikan seluruh kode kepada maksimal tujuh pemain yang sudah memiliki akses situs. Kode ruang tidak mengubah akses situs.

Host mengatur kapasitas delapan pemain, waktu, kepemilikan hewan, batas kecepatan/jarak, pembelian, cooldown dan reward; peer mengirim pose/intent, host mengirim snapshot 5 Hz. Host harus tetap online; putusnya host mengakhiri sesi. Tidak ada backend anticheat atau migrasi host.

Kolaborasi berbagi petunjuk dan hadiah. Merebut hewan dalam radius 15 unit mengubah pemain menjadi kompetitor dengan cooldown 12 detik. Pengantar kompetitif menerima reward penuh. Spawn awal acak; saldo multiplayer 250 koin per sesi, terpisah dari solo.

Koneksi bergantung pada WebRTC/STUN dan relay publik. Tidak ada TURN khusus, sehingga sebagian NAT/jaringan kantor dapat gagal terhubung. Uji delapan perangkat sekaligus belum dilakukan.

## ElevenLabs langsung

Audio runtime baru tidak menggunakan Runway, Krea, browser TTS atau suara sintetis pengganti. `scripts/generate-elevenlabs.py` memanggil API resmi `https://api.elevenlabs.io` langsung untuk SFX dan ucapan Indonesia.

Key dibaca dari environment `ELEVENLABS_API_KEY` atau file privat `.env.local` yang diabaikan Git, tidak masuk manifest/bundle dan tidak dicetak. Vault yang hanya menyimpan key belum otomatis menjadi binding environment. `.env.example` hanya berisi nama variabel kosong.

Manifest audio kosong berarti `requires_connection`: game menunjukkan audio belum tersedia. Setelah key terpasang, jalankan generator, verifikasi hasil MP3, lalu terbitkan ulang `dist/`. Generator sequential dan resumable; klip selesai tidak dibuat ulang. Paket/credit/izin ElevenLabs berlaku saat generasi.

Audio engine memakai listener FPS/HRTF untuk burung, angin, air, kendaraan, klakson, warga, hewan, langkah kaki dan alat sesuai aset yang tersedia. API key tidak diperlukan di browser atau situs publik.

## Verifikasi

`node --test tests/*.test.mjs` — 17 pemeriksaan aturan game, kapasitas, jarak/kecepatan, reward, kolaborasi/pengkhianatan, kandang/patroli, gerak hewan, arah FPS, struktur GLB/material/animasi dan kejujuran status audio.

Preview cloud mengalami relay timeout pada sesi pengembangan; gameplay FPS dan audio dalam browser belum terverifikasi. Render aset di Blender membantu pemeriksaan bentuk model, bukan pengganti uji browser.
