---
name: pupr-kelengkapan-checklist
description: >
  Persyaratan kelengkapan minimal (Konten, Skala, Notasi, penyajian per skala) untuk
  setiap jenis gambar arsitektur menurut Modul Standar Kelengkapan Gambar Arsitektur PUPR 2021.
  Gunakan skill ini saat user bertanya "apa saja yang harus ada di gambar denah/tampak/potongan/
  detail/rencana/site plan/block plan/perspektif", "kelengkapan gambar arsitektur", "skala gambar
  PUPR", "notasi minimal gambar", "buat checklist kelengkapan gambar", atau saat perlu mengecek satu
  gambar terhadap standar PUPR. Mencakup 24 jenis gambar dari Block Plan sampai Perspektif 3D.
  JANGAN gunakan untuk mutu material/struktur SNI (beton, tulangan, baja, gempa) — itu ranah skill
  revit-sni-*. Skill ini khusus kelengkapan & penyajian gambar deliverable arsitektur.
metadata:
  version: "1.0.0"
  sumber: "Modul Standar Kelengkapan Gambar Arsitektur, Edisi 1 (Sept 2021), Ditjen Cipta Karya PUPR"
---

# PUPR — Kelengkapan Gambar Arsitektur

Acuan persyaratan **minimal** isi gambar per jenis, sesuai Modul Standar Kelengkapan Gambar
Arsitektur PUPR (Edisi 1, September 2021). Untuk aturan grafis lintas-gambar (kop, ketebalan garis,
teks, ukuran kertas, simbol notasi) lihat skill `pupr-standar-grafis`.

## Sumber data kanonik

Semua persyaratan tersimpan terstruktur di:

```
references/kelengkapan-gambar.json
```

Tiap jenis gambar punya: `konten` (elemen wajib), `skala` (opsi skala yang diizinkan), `notasi`
(notasi minimal wajib), dan `presentasi` (aturan penyajian grafis per skala). **Selalu baca file ini
sebagai sumber kebenaran** — jangan mengarang persyaratan dari ingatan.

24 jenis gambar (id JSON): `block_plan`, `site_plan`, `denah_lantai_dasar`, `denah_bangunan`,
`denah_basement`, `tampak_tapak`, `tampak_bangunan`, `potongan_tapak`, `potongan_bangunan`,
`potongan_prinsip`, `rencana_finishing_dinding`, `rencana_pintu_jendela`, `rencana_lantai`,
`rencana_atap`, `rencana_plafond`, `rencana_titik_lampu`, `rencana_sanitasi`, `detail_pintu_jendela`,
`detail_toilet`, `detail_ruang_khusus`, `detail_tangga_ramp`, `detail_core_lift`, `detail_lainnya`,
`perspektif`.

## Alur kerja

### 1) Menjawab "apa saja yang harus ada di gambar X?"
- Baca `references/kelengkapan-gambar.json`, ambil objek dengan `id` yang cocok.
- Sajikan `konten`, `skala`, `notasi`, dan `presentasi` (per skala) sesuai gaya jawaban user
  (BLUF + bullet/tabel). Tegaskan ini persyaratan **minimal**.

### 2) Membuat checklist (cetak / dasar QC)
Gunakan generator agar konsisten:

```bash
# Daftar id jenis gambar
python scripts/generate_checklist.py --list

# Checklist Markdown untuk jenis tertentu
python scripts/generate_checklist.py --jenis denah_bangunan potongan_bangunan -o checklist.md

# Checklist seluruh satu kelompok ke CSV (mis. semua "detail")
python scripts/generate_checklist.py --kelompok detail --format csv -o detail.csv

# Seluruh 24 jenis gambar (Markdown ke stdout)
python scripts/generate_checklist.py
```

Output Markdown memakai kotak centang `[ ]` siap diisi; CSV cocok untuk spreadsheet/Issue tracking.

### 3) QC cepat satu gambar (inline)
- Tanyakan / tentukan jenis gambar dan skalanya.
- Ambil persyaratan dari JSON, lalu periksa gambar (mis. gambar yang di-paste, atau hasil
  rasterisasi PDF) item demi item.
- Laporkan **ADA / TIDAK ADA / TIDAK JELAS** per item, plus rekomendasi perbaikan ringkas.
- Untuk QC satu **set besar** (banyak lembar), serahkan ke subagent `pupr-reviewer`.

## Aturan penting (jangan dilanggar)

- **Persyaratan ini MINIMAL**, bukan maksimal. Jangan menyatakan gambar "tidak sesuai" hanya karena
  ada elemen tambahan di luar daftar.
- **Skala wajib dari daftar yang diizinkan** untuk jenis itu. Contoh: Potongan Prinsip harus
  1:50 / 1:20 / 1:10 dan **harus lebih besar** dari skala Potongan biasa.
- **Aturan penyajian berbeda per skala** (mis. di denah 1:200/1:100 dinding terpotong diblok hitam;
  di 1:50 beroutline tebal + arsir material). Pakai blok `presentasi` sesuai skala gambar.
- Sebutkan dasar halaman modul (field `halaman`) bila user butuh rujukan.
- Jika informasi yang diberikan user tidak cukup untuk menilai (mis. skala tidak diketahui),
  katakan "Insufficient data" dan minta yang kurang — jangan menebak.

## Catatan integrasi (opsional)
Skill ini tool-agnostic. Untuk men-scaffold daftar gambar/sheet & kop sesuai urutan PUPR (dan
membuat sheet di Revit via pyRevit MCP), gunakan skill `pupr-deliverable-setup`.
