# SAI-QTrack: Automotive Wiring Harness Defect & Scrap Tracking

> **Sistem Pemantauan Kualitas & Pelacakan Scrap Wiring Harness Shopfloor**  
> Disesuaikan untuk kebutuhan manufaktur **PT. Surabaya Autocomp Indonesia (SAI) - Yazaki Group**.

---

## 🎯 Latar Belakang & Masalah Riil yang Diselesaikan
PT. Surabaya Autocomp Indonesia adalah produsen utama *automotive wiring harness* (rangkaian kabel kelistrikan mobil) untuk OEM global (seperti Toyota Avanza/Veloz, Daihatsu Xenia/Ayla, dll).

Di lantai produksi (*shopfloor*), kendali mutu (*Zero Defect*) dan pengendalian kerugian material (*Scrap Control*) sangat krusial. Masalah yang sering terjadi:
1. **Pencatatan manual di kertas** lambat direkapitulasi, menyulitkan tim QC/Leader mengambil tindakan cepat saat terjadi cacat berulang pada lini *crimping* atau *assembly*.
2. **Ketiadaan database terpusat** membuat pelacakan (*traceability*) akar penyebab kecacatan per nomor part harness memakan waktu lama.

**SAI-QTrack** hadir untuk:
- Memberikan form input digital yang cepat dan ramah operator QC (*Fast-Entry*).
- Menghadirkan **Real-Time Quality Dashboard** ringkasan reject rate, total scrap hari ini, rasio *Scrap vs Rework*, dan analisis **Top 5 Defect (Pareto)** per lini dan shift.
- Membuka akses langsung ke **PostgreSQL** untuk tim analitik & Business Intelligence (**PowerBI**).

---

## 🛠️ Tech Stack & Arsitektur
- **Backend Framework**: Python 3.14 & Django 5.2
- **Database**: PostgreSQL 16 (Berjalan di container Docker)
- **Database Driver**: `psycopg` (v3 modern binary)
- **Frontend & UI**: Bootstrap 5 + Bootstrap Icons + Crispy Forms (Desain industri yang bersih dan ergonomis)
- **BI & Analytics Ready**: Skema relasional yang kompatibel dengan PowerBI / Metabase / Grafana

---

## 🚀 Panduan Menjalankan di Komputer Lokal

### 1. Jalankan PostgreSQL via Docker
Masuk ke folder `SAI-Qtrack` dan jalankan:
```bash
docker-compose up -d
```
Container database akan aktif di port `5433` (dipetakan ke port internal `5432` agar tidak bentrok dengan instalasi PostgreSQL lokal lain jika ada).

### 2. Aktifkan Virtual Environment & Jalankan Migrasi
Jika menggunakan PowerShell di Windows:
```powershell
.\venv\Scripts\Activate.ps1
python manage.py migrate
```

### 3. Load Data Master Awal (Seed Data)
Jalankan perintah ini untuk mengisi master data lini perakitan, part harness Toyota/Daihatsu, katalog defect standar pabrik, serta 25 sampel catatan QC:
```bash
python manage.py seed_data
```

### 4. Jalankan Web Server Django
```bash
python manage.py runserver
```
Buka browser di:
- **Live Quality Dashboard**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Form Fast-Entry Defect QC**: [http://127.0.0.1:8000/log/new/](http://127.0.0.1:8000/log/new/)
- **Data Logbook & Filter**: [http://127.0.0.1:8000/logs/](http://127.0.0.1:8000/logs/)
- **Django Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
  - **Username**: `admin`
  - **Password**: `admin123`

---

## 📊 Integrasi ke PowerBI (Nilai Plus saat Interview)
Aplikasi ini menggunakan PostgreSQL yang siap dihubungkan langsung ke **PowerBI Desktop**:

1. Buka **PowerBI Desktop** &rarr; Pilih **Get Data** &rarr; **PostgreSQL database**.
2. Masukkan parameter koneksi:
   - **Server**: `127.0.0.1:5433`
   - **Database**: `sai_qtrack_db`
   - **User**: `sai_user`
   - **Password**: `sai_secure_pwd`
3. Pilih view data `vw_powerbi_defects` (atau tabel `tracking_defectlog`, `tracking_line`, `tracking_harnesspart`, `tracking_defectcategory`).
4. Panduan lengkap koneksi, DAX measures, dan SQL view tersedia di:
   - 📄 [Panduan Lengkap PowerBI](docs/powerbi/POWERBI_INTEGRATION_GUIDE.md)
   - 🗄️ [Script SQL View Denormalisasi](docs/powerbi/create_powerbi_view.sql)

---

## 📁 Struktur Domain & Berkas
- [`GLOSSARY.md`](./GLOSSARY.md): Kamus istilah baku domain manufaktur wiring harness (*Line*, *Harness Part*, *Defect Category*, *Action Taken*).
- [`docs/adr/0001-postgresql-docker-for-powerbi-readiness.md`](./docs/adr/0001-postgresql-docker-for-powerbi-readiness.md): Catatan keputusan arsitektur database.
