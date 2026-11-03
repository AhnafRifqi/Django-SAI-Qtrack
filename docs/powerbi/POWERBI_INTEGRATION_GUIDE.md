# Panduan Integrasi PostgreSQL Docker ke Microsoft PowerBI Desktop

Dokumen ini menjelaskan langkah demi langkah cara menghubungkan database PostgreSQL yang berjalan di dalam Docker container (`sai_postgres`) langsung ke **PowerBI Desktop** untuk kebutuhan pelaporan eksekutif, analisis *scrap rate*, dan analisis *Pareto defect*.

---

## 1. Parameter Koneksi Database

Pastikan container PostgreSQL sedang berjalan (`docker-compose up -d`). Gunakan kredensial berikut:

| Parameter | Nilai Konfigurasi | Keterangan |
| :--- | :--- | :--- |
| **Server** | `127.0.0.1:5433` | Host lokal dengan port forward `5433` |
| **Database** | `sai_qtrack_db` | Nama database operasional |
| **Data Connectivity Mode** | **Import** (atau DirectQuery) | Direkomendasikan *Import* untuk performa cepat |
| **User Name** | `sai_user` | Akun database |
| **Password** | `sai_secure_pwd` | Password default `.env` |

> 💡 **Catatan Port**: Container memetakan port `5433` di host ke port `5432` di dalam container. Karena itu di PowerBI Anda wajib memasukkan `127.0.0.1:5433`.

---

## 2. Langkah-Langkah di PowerBI Desktop

1. Buka aplikasi **PowerBI Desktop**.
2. Pada tab **Home**, klik icon **Get Data** &rarr; pilih **More...**.
3. Di kotak pencarian, ketik **PostgreSQL database** &rarr; klik **Connect**.
4. Isi jendela konfigurasi koneksi:
   - **Server**: `127.0.0.1:5433`
   - **Database**: `sai_qtrack_db`
   - **Data Connectivity mode**: Pilih **Import**.
5. Klik **OK**.
6. Pada dialog autentikasi kredensial:
   - Pilih tab **Database** (di sebelah kiri).
   - Masukkan **User name**: `sai_user`
   - Masukkan **Password**: `sai_secure_pwd`
   - Klik **Connect**.
   *(Jika muncul peringatan enkripsi/SSL Support, klik **OK** / **Continue**).*
7. Pada jendela **Navigator**, Anda dapat memilih:
   - **Opsi A (Rekomendasi - Denormalized View)**: Pilih `vw_powerbi_defects` (dibuat via script `create_powerbi_view.sql`). View ini sudah menggabungkan nama lini, part mobil, kategori cacat, dan klasifikasi scrap dalam satu tabel siap olah.
   - **Opsi B (Relational Tables)**: Centang tabel:
     - `tracking_defectlog` (Fact Table)
     - `tracking_line` (Dimension)
     - `tracking_harnesspart` (Dimension)
     - `tracking_defectcategory` (Dimension)
8. Klik **Load**. Data siap divisualisasikan!

---

## 3. Eksekusi Script SQL View (Opsional namun Bernilai Plus)

Untuk mengaktifkan SQL View `vw_powerbi_defects` di container PostgreSQL, jalankan perintah ini dari terminal:

```bash
# Melalui Docker Exec langsung
docker exec -i sai_postgres psql -U sai_user -d sai_qtrack_db < docs/powerbi/create_powerbi_view.sql
```

Atau buka tool GUI database (seperti DBeaver / pgAdmin / DataGrip) yang terhubung ke `127.0.0.1:5433`, lalu paste isi dari `docs/powerbi/create_powerbi_view.sql` dan eksekusi.

---

## 4. Rekomendasi DAX Measures untuk Dashboard Mutu

Buat measure berikut di PowerBI untuk kalkulasi otomatis KPI:

### 1. Total Defect Quantity
```dax
Total Defect Qty = SUM(vw_powerbi_defects[quantity])
```

### 2. Total Scrap Quantity
```dax
Total Scrap Qty = CALCULATE(
    SUM(vw_powerbi_defects[quantity]),
    vw_powerbi_defects[disposition] = "SCRAP"
)
```

### 3. Total Rework Quantity
```dax
Total Rework Qty = CALCULATE(
    SUM(vw_powerbi_defects[quantity]),
    vw_powerbi_defects[disposition] = "REWORK"
)
```

### 4. Scrap Rate Percentage
```dax
Scrap Rate % = DIVIDE([Total Scrap Qty], [Total Defect Qty], 0)
```

---

## 5. Rekomendasi Visualisasi Dashboard PowerBI

1. **KPI Cards (Top Bar)**:
   - Card 1: `Total Defect Qty`
   - Card 2: `Total Scrap Qty` (Warna Merah)
   - Card 3: `Scrap Rate %`
   - Card 4: `Critical Severity Qty`
2. **Visual Pareto (Bar & Line Chart)**:
   - X-Axis: `defect_name`
   - Column Y-Axis: `Total Defect Qty`
   - Urutkan menurun (*Descending*) untuk melihat 20% jenis defect yang menyumbang 80% reject.
3. **Donut Chart**:
   - Legend: `disposition` (Scrap vs Rework)
   - Values: `quantity`
4. **Matrix Table (Shopfloor Traceability)**:
   - Rows: `car_model` &rarr; `part_number` &rarr; `line_code`
   - Columns: `shift_name`
   - Values: `Total Defect Qty`
