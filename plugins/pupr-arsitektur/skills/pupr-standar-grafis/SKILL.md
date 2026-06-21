---
name: pupr-standar-grafis
description: >
  Standar grafis & notasi gambar arsitektur menurut Modul Standar Kelengkapan Gambar Arsitektur PUPR
  2021: kop gambar (13 field wajib), judul & skala, orientasi/arah Utara, ketebalan garis
  (0,18/0,25/0,35/0,4 mm), jenis garis, leader, garis potong, garis dimensi, teks (ukuran 18pt/14pt &
  tinggi 3mm/5-6mm), dimensi, legenda, ukuran kertas (A3/A2/A1), serta 4 kategori notasi & token
  simbolnya. Gunakan saat user bertanya "standar grafis PUPR", "kop gambar", "ketebalan/jenis garis
  gambar", "ukuran teks/font gambar teknik", "ukuran kertas gambar", "notasi/simbol gambar
  arsitektur", atau saat menyiapkan setup grafis (text type/line) di Revit agar sesuai PUPR. JANGAN
  pakai untuk standar material/struktur SNI — itu skill revit-sni-*.
metadata:
  version: "1.0.0"
  sumber: "Modul Standar Kelengkapan Gambar Arsitektur, Edisi 1 (Sept 2021), Ditjen Cipta Karya PUPR"
---

# PUPR — Standar Grafis & Notasi

Aturan grafis lintas-gambar (berlaku untuk semua jenis gambar). Untuk persyaratan isi **per jenis
gambar** (denah/tampak/potongan/detail/dll), gunakan skill `pupr-kelengkapan-checklist`.

## Sumber data
- `references/standar-grafis.md` — 12 komponen standar grafis (kop, judul & skala, orientasi,
  ketebalan garis, jenis garis, leader, garis potong, garis dimensi, teks, dimensi, legenda, kertas).
- `references/notasi.md` — 4 kategori notasi + daftar token simbol baku.

**Baca file rujukan terkait sebelum menjawab** — jangan mengarang nilai/standar dari ingatan.

## Angka kunci yang sering ditanya (ringkas)

| Aspek | Nilai baku PUPR 2021 |
|---|---|
| Ketebalan garis | 0,18 / 0,25 / 0,35 / 0,4 mm |
| Teks judul | 18 pt (A0–A2) · 14 pt (A3–A4) |
| Tinggi teks dimensi/notasi | 3 mm |
| Tinggi teks subjudul/judul | 5–6 mm |
| Ukuran kertas | A3 (297×420) · A2 (420×594) · A1 (594×841) mm |
| Jarak objek ↔ garis dimensi | ± 10 mm |
| Kop gambar | 13 field minimal (lihat referensi) |
| Skala | wajib **skala angka + skala batang** (batang selalu dilampirkan) |
| Orientasi | arah Utara di atas (denah); wajib simbol arah Utara sebenarnya bila menyimpang |

Teks selalu **kapital + sans-serif**, judul tanpa singkatan.

## Alur kerja

### Menjawab pertanyaan standar
Ambil nilai dari `references/standar-grafis.md` / `references/notasi.md`, jawab BLUF + tabel,
sebutkan dasar (nama komponen / halaman modul) bila perlu.

### Menyiapkan setup grafis di Revit (opsional, via pyRevit MCP)
Jika user ingin menerapkan standar ke model Revit melalui MCP pyRevit, hasilkan **kode Python Revit
API** lalu kirim ke Revit lewat MCP. Contoh template membuat Text Note Type sesuai ukuran teks PUPR
(adaptasi nama base type/family sesuai template user):

```python
# pyRevit / Revit API — buat Text Note Type ukuran PUPR (3mm, 5mm, 6mm).
# Jalankan via MCP "execute python in Revit". Ukuran tinggi teks Revit dalam feet.
from Autodesk.Revit.DB import (FilteredElementCollector, TextNoteType,
                               ElementType, BuiltInParameter, Transaction)

doc = __revit__.ActiveUIDocument.Document
MM_TO_FT = 1.0 / 304.8
SIZES_MM = {"PUPR_Notasi_3mm": 3.0, "PUPR_Subjudul_5mm": 5.0, "PUPR_Judul_6mm": 6.0}

base = FilteredElementCollector(doc).OfClass(TextNoteType).FirstElement()
t = Transaction(doc, "PUPR text types"); t.Start()
for name, mm in SIZES_MM.items():
    nt = base.Duplicate(name)
    p = nt.get_Parameter(BuiltInParameter.TEXT_SIZE)
    if p: p.Set(mm * MM_TO_FT)
    # set font ke sans-serif (mis. Arial) bila parameter tersedia di environment-mu
t.Commit()
print("Text types dibuat:", list(SIZES_MM.keys()))
```

Catatan:
- **Ketebalan garis** di Revit diatur lewat *Manage → Object Styles* (nomor pena 1–16) dan tabel
  *Line Weights* (mm per skala) — bukan langsung dari nilai mm di objek. Petakan nomor pena ke nilai
  0,18/0,25/0,35/0,4 mm pada skala yang dipakai. Sampaikan ini bila user minta otomatisasi penuh.
- Untuk membuat **kop gambar** (title block) & **daftar gambar** sesuai PUPR, gunakan skill
  `pupr-deliverable-setup`.

## Aturan
- Nilai-nilai ini adalah **standar minimal/baku** modul PUPR 2021; sebutkan bila ada hal yang
  diserahkan ke kebijakan unit kerja (mis. kode gambar, kolom tanda tangan).
- Jangan mencampur standar ini dengan standar struktur/material SNI.
