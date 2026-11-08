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

`dist/models/manifest.json` memuat 64 aset GLB standalone: 50 profil hewan, tiga manusia, sedan, truk satwa, air mancur, gedung kantor, rumah, toko, bangku, bunga, lampu, air dan pohon.

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

Paket runtime sudah berisi **61 klip lokal dari 22 kategori audio**, dibuat melalui konektor ElevenLabs langsung: burung, angin, sungai, lalu lintas, klakson, keramaian, langkah kaki, alat, las, tujuh keluarga suara/pergerakan hewan, efek keberhasilan dan penjemputan, tiga dialog Indonesia, dan musik instrumental. Beberapa variasi awal terkena batas antrean; klip yang diterima telah selesai dan tidak dibuat ulang.

`dist/audio/manifest.json` menyimpan kategori, model, generation ID, durasi dan nama file lokal. Tidak menyimpan signed download URLs atau API key. Model SFX: eleven_text_to_sound_v2; dialog: eleven_multilingual_v2; musik: eleven_music_v2. Suara dialog dipilih dari daftar suara Indonesia yang tersedia pada konektor.

Audio engine memakai listener FPS/HRTF untuk sumber di dunia 3D dan memilih variasi klakson/dialog bergantian. Angin dan musik menjadi lapisan latar; langkah kaki aktif saat berjalan; suara alat mengikuti alat pembuka kandang yang dipakai. Tombol Masuk ke kota mengaktifkan audio melalui gesture pengguna, dan ♫ mematikan seluruh loop. Audio yang gagal dimuat tidak menghalangi klip lainnya.

API key tidak diperlukan oleh browser maupun situs yang diterbitkan. `scripts/import-elevenlabs-assets.py` mengimpor hasil konektor dari metadata unduhan temporer privat, mengonversi ke MP3 dan menormalkan level audio. Signed URLs tidak diterbitkan. `scripts/generate-elevenlabs.py` tetap tersedia sebagai jalur API resmi alternatif bila environment kelak memiliki key, tetapi tidak dipakai untuk paket ini. File privat `.env.local` diabaikan Git dan tidak masuk paket situs.

## Verifikasi

`node --test tests/*.test.mjs` — 20 pemeriksaan aturan game, kapasitas, jarak/kecepatan, reward, kolaborasi/pengkhianatan, kandang/patroli, gerak hewan, arah FPS, struktur GLB/material/animasi dan kelengkapan aset, pergantian variasi klakson dan penghentian semua loop saat mute.

Preview cloud mengalami relay timeout pada sesi pengembangan; gameplay FPS dan audio spasial dalam browser belum terverifikasi. Semua 61 MP3 berhasil didekode dan diverifikasi tidak senyap dengan FFmpeg. Render aset di Blender membantu pemeriksaan bentuk model, bukan pengganti uji browser.

## Peningkatan karakter dan pencahayaan

Karakter manusia memakai pivot lutut, jarak kaki lebih sempit, langkah ke depan/belakang dan ayunan tangan berlawanan. Pemain multiplayer berputar mengikuti perpindahan dan kembali ke pose diam ketika berhenti. Builder khusus manusia: `node scripts/build-models.mjs --humans-only`.

Lampu jalan kini tersebar di jalan kota. Lampu jalan, pintu gedung, mobil dan truk memakai spotlight dengan peluruhan kuadrat, arah sorot dan warna yang sesuai. Material lensa dan jendela menyala saat sore/malam. Untuk membatasi biaya GPU, hanya 12 sumber terdekat mendapat slot cahaya aktif, termasuk dua dengan bayangan lokal. Jendela memakai emisi dan cahaya pintu sebagai representasi penerangan gedung; belum ada simulasi interior pada setiap jendela. Model motor belum tersedia dalam paket ini.

Material mendapat detail normal/roughness untuk keluarga beton, batu, kayu, kain, aspal dan atap. Lingkungan pantulan PMREM mengikuti fase WIB. Ini peningkatan PBR atas model prosedural yang tersedia, belum fotorealisme penuh atau pantulan dinamis ray tracing.

Panduan penggunaan ulang lintas proyek: [proses karakter dan environment](docs/threejs-realistic-environment.md). Tambahan tes mencakup artikulasi lutut, pose diam, arah/gerakan sorot lampu, pergantian siang–malam dan batas jumlah lampu. Uji render terisolasi di Chromium berhasil; performa gameplay kota penuh tetap perlu diuji pada GPU perangkat sasaran.
