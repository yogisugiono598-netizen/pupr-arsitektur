---
name: pupr-deliverable-setup
description: >
  Menyusun struktur deliverable gambar arsitektur sesuai urutan PUPR 2021: daftar gambar / sheet list
  (kode, judul, skala, ukuran kertas), penomoran lembar, dan pembuatan ViewSheet di Revit via pyRevit
  MCP. Gunakan saat user minta "susun daftar gambar", "buat sheet list / daftar lembar", "scaffold
  gambar kerja DED", "urutan gambar arsitektur PUPR", "berapa lembar gambar untuk bangunan X lantai",
  "buatkan sheet di Revit", atau menyiapkan kop + nomor lembar untuk satu set gambar. Mendukung
  ekspansi otomatis per-lantai, basement, tampak (min 4 arah), dan potongan (min 2). JANGAN gunakan
  untuk isi/QC per gambar (pakai pupr-kelengkapan-checklist) atau standar grafis kop detail (pakai
  pupr-standar-grafis).
metadata:
  version: "1.0.0"
  sumber: "Modul Standar Kelengkapan Gambar Arsitektur, Edisi 1 (Sept 2021), Ditjen Cipta Karya PUPR"
---

# PUPR — Deliverable Setup (Daftar Gambar & Sheet Revit)

Men-scaffold *set* gambar arsitektur: urutan lembar, kode/nomor, skala & kertas default, lalu
(opsional) membuat ViewSheet di Revit lewat MCP pyRevit. Untuk isi tiap gambar gunakan
`pupr-kelengkapan-checklist`; untuk standar grafis kop/garis/teks gunakan `pupr-standar-grafis`.

## Sumber data
- `references/sheet-sequence.json` — 24 lembar baku berurut (id, judul, kode default `AR-xx`, skala
  default, kertas default, status wajib/kondisional, dan flag ekspansi `per_lantai` / `min_lembar`).

> **Kode & nomor lembar fleksibel.** Modul PUPR menyerahkan kode gambar & nomor lembar ke peraturan
> administratif tiap unit kerja. Prefix `AR` (Arsitektur) hanyalah default yang bisa diganti
> (`--prefix`). Kertas default A3; tapak/kawasan berskala besar pakai A2/A1.

## Alur kerja

### 1) Susun daftar gambar (sheet list)
Gunakan generator agar urutan & penomoran konsisten:

```bash
# Daftar penuh (semua lembar, termasuk kondisional) -> Markdown
python scripts/generate_sheet_list.py

# Proyek nyata: 3 lantai + 1 basement + ada lift -> CSV (siap dipakai membuat sheet di Revit)
python scripts/generate_sheet_list.py --lantai 3 --basement 1 --ada-lift --format csv -o sheets.csv

# Hanya lembar WAJIB (tanpa kondisional)
python scripts/generate_sheet_list.py --hanya-wajib

# Ganti prefix kode (mis. 'A') & jumlah tampak/potongan
python scripts/generate_sheet_list.py --prefix A --tampak 4 --potongan-bangunan 2
```

Parameter ekspansi: `--lantai N` (Denah Bangunan per lantai 2..N), `--basement N`, `--ada-lift`
(Detail Core Lift), `--ada-ruang-khusus`, `--tampak N` (default 4), `--potongan-bangunan N` (default 2).
Generator otomatis mengisi **No. Lembar berurutan** dan **Jumlah Halaman** (field kop PUPR).

### 2) Buat ViewSheet di Revit (via pyRevit MCP)
Template: `scripts/pyrevit_create_sheets.py`. Langkah:
1. Hasilkan `sheets.csv` (langkah 1) atau tempel daftar ke list `SHEETS` di template.
2. Set `TITLE_BLOCK_NAME` ke nama family kop di proyek user (kosongkan untuk pakai title block pertama).
3. Kirim isi script ke Revit melalui MCP pyRevit (eksekusi Python di Revit). Script membuat setiap
   `ViewSheet` dengan `SheetNumber` = kode dan `Name` = judul (uppercase), serta melewati nomor yang
   sudah ada agar idempoten.

Penjelasan untuk user:
- Script **membuat lembar + nomor + judul**. Penempatan view ke tiap lembar tidak diotomasi (pemetaan
  view spesifik proyek) — lakukan manual atau langkah lanjutan.
- Kop sesuai PUPR butuh 13 field (lihat `pupr-standar-grafis`). Jika family kop user punya parameter
  kustom (Nama Proyek, Kode, Jumlah Halaman, dsb.), tambahkan pengisian parameter pada bagian loop di
  template.

### 3) Validasi kelengkapan set
Setelah sheet dibuat / set gambar tersusun, gunakan subagent `pupr-reviewer` untuk mengaudit apakah
set sudah memenuhi kelengkapan PUPR (jenis gambar wajib ada, jumlah minimum tampak/potongan terpenuhi,
skala sesuai), dengan membandingkan sheet/view di Revit terhadap daftar baku.

## Aturan
- Tandai lembar **KONDISIONAL** dengan jelas (basement, core lift, ruang khusus, finishing dinding,
  titik lampu/sanitasi bila ditangani MEP) — sertakan hanya bila relevan.
- Pastikan jumlah minimum: **Tampak ≥ 4 arah**, **Potongan Bangunan ≥ 1 melintang + 1 memanjang**
  (salah satu memotong tangga), **Potongan Tapak ≥ 2**.
- **Potongan Prinsip skala harus lebih besar** dari Potongan Bangunan.
- Jangan menilai/QC isi tiap gambar di sini — itu tugas `pupr-kelengkapan-checklist` / `pupr-reviewer`.
