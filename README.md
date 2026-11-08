# Where’s My Pet? — kota 1.000 × 1.000

Game Three.js berbahasa Indonesia, tanpa build step. Sajikan direktori `dist/` melalui HTTP(S).

## Dunia dan permainan

- Batas dunia X/Z −500…500: tepat 1.000 × 1.000 unit Three.js. Satuan ini tidak otomatis berarti meter.
- 50 level dengan enam tema. Seed adventure mengacak permutasi 50 profil hewan tanpa pengulangan profil antarlevel. Distrik, tinggi gedung, rute, rumah pemilik, hadiah dan waktu berbeda secara prosedural.
- Gedung hingga sekitar 210 unit, perumahan, toko, kios, kebun, taman, bunga, rumput, pedestrian, jalan dan empat jembatan sungai. Dasar sungai Y −23, air Y −5, kedalaman sekitar 18 unit.
- Instancing menggabungkan puluhan ribu bagian statis menjadi sedikit draw call; 110 kendaraan, 160 warga (termasuk 24 pemancing), arus sungai dan foliage beranimasi.
- Klik objek memberi nama, pemilik dan detail serta zoom. Semua bagian instanced memiliki metadata objek. Objek bergerak memperbarui posisi metadata.
- PetNet fiktif, brosur pohon/rumah/tiang dan dialog warga memberi potret render 3D, ciri dan lokasi bertimestamp. Hewan berpindah dengan interval yang makin singkat di level lanjut.
- City Map permanen dan peta besar berisi distrik, sungai, pemain, rumah pemilik, truk dan jejak. Lokasi hewan aktual hanya dengan digital map. Klik peta untuk menandai tujuan; navigasi BFS mengikuti jalan aman.
- WASD/panah, Shift, tombol sentuh; E untuk objek terdekat. Ambil hewan ≤15 unit, antar ke pemilik ≤22 unit. Tidak ada tombol teleport penyelesaian.
- Waktu pencarian, penangkapan satwa, pembukaan kandang nyata selama 3/6/18 detik, patroli, gagal, ulang, pembagian hadiah dan sembilan peralatan fungsional.
- Waktu riil Asia/Jakarta (WIB), empat fase pencahayaan. Web Audio memberi musik, klakson dan celoteh. SpeechSynthesis membaca dialog jika suara perangkat tersedia.

## Multiplayer WebRTC

Buka Multiplayer, isi nama, buat ruang. Bagikan seluruh kode ke maksimal tujuh pemain dengan akses situs. Pengaturan akses situs tidak diubah. Ruang tidak membuka akses situs kepada pengunjung baru.

Trystero v0.22.0 MQTT memanfaatkan broker publik untuk signaling terenkripsi dan WebRTC data channels untuk data permainan. Tidak ada backend game terpusat. Host menjalankan GameEngine dan memutuskan batas 8 pemain, waktu, kepemilikan hewan, pembelian, jarak aksi, kecepatan posisi, cooldown dan hadiah. Peer mengirim pose/intent, host mengirim snapshot 5 Hz. Host harus tetap membuka game; host terputus mengakhiri sesi, bukan migrasi host otomatis. Peer non-host tidak dapat mengganti level.

Koneksi bergantung pada WebRTC/STUN dan ketersediaan relay publik. Tidak ada TURN khusus; beberapa NAT/jaringan kantor dapat memblokir koneksi. Tidak tersedia jaminan konektivitas semua jaringan. Ini multiplayer kasual dengan host tepercaya, bukan sistem kompetitif dengan anticheat server.

Pemain berkolaborasi berbagi petunjuk dan hadiah. Merebut dari radius 15 unit mengubah pemain menjadi kompetitor dengan cooldown 12 detik. Kompetitor yang mengantar mendapat reward penuh. Spawn awal acak; saldo per sesi 250 koin, terpisah dari progres solo. Progres solo memakai localStorage, tidak lintas perangkat.

## Pemeriksaan

`node --test tests/engine.test.mjs`

Uji mencakup 50 level, batas kota, determinisme, kapasitas 8, batas kecepatan, jarak aksi, idempotensi reward, kolaborasi, pengkhianatan, kandang, patroli, peralatan, pergerakan hewan dan peluit. Browser QA dicatat terpisah; lulus unit test bukan bukti konektivitas antarperangkat.

## Aset dan batas visual

Three.js r170 dan Trystero v0.22.0 di-vendor secara lokal (MIT dan dependensi berlisensi dalam bundle). Tidak ada foto hewan eksternal atau internet langsung. Potret 3D dan model hewan bersifat stilisasi; katalog 50 profil bukan seluruh spesies dunia. Layout berbagi grid jalan, dengan variasi distrik prosedural. Audio dialog memakai suara sistem, bukan rekaman warga individu.
