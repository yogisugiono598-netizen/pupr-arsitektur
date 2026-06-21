# PUPR Arsitektur — Claude Code Plugin

Standar **Kelengkapan & Grafis Gambar Arsitektur** menurut *Modul Standar Kelengkapan Gambar
Arsitektur* Kementerian PUPR, Ditjen Cipta Karya (Edisi 1, September 2021), dikemas sebagai plugin
Claude Code: **3 skills + 1 agent**.

Lingkup ketat: **kelengkapan deliverable gambar + standar grafis**. Tidak mencakup standar
material/struktur SNI (gunakan skill `revit-sni-*` terpisah), pembuatan elemen Revit umum, atau
kritik desain.

## Isi

| Komponen | Tipe | Fungsi |
|---|---|---|
| `pupr-standar-grafis` | skill | Kop gambar (13 field), ketebalan/jenis garis, teks (18pt/14pt, 3mm/5-6mm), ukuran kertas (A3/A2/A1), dimensi, legenda, orientasi, 4 kategori notasi. Plus snippet pyRevit untuk text type. |
| `pupr-kelengkapan-checklist` | skill | Persyaratan minimal **Konten / Skala / Notasi / penyajian per skala** untuk **24 jenis gambar**. Generator checklist Markdown/CSV. |
| `pupr-deliverable-setup` | skill | Daftar gambar / sheet list (kode, judul, skala, kertas) berurutan PUPR, ekspansi per-lantai/basement/tampak/potongan, + template pyRevit pembuat ViewSheet. |
| `pupr-reviewer` | agent | Auditor QA: cek kelengkapan satu gambar atau satu set lengkap (juga bisa introspeksi Revit via MCP) → laporan temuan ber-severity. |

24 jenis gambar: Block Plan, Site Plan, Denah Lantai Dasar, Denah Bangunan, Denah Basement, Tampak
Tapak, Tampak Bangunan, Potongan Tapak, Potongan Bangunan, Potongan Prinsip, Rencana (Finishing
Dinding, Pintu & Jendela, Lantai, Atap, Plafond, Titik Lampu, Sanitasi), Detail (Pintu & Jendela,
Toilet, Ruang Khusus, Tangga/Ramp, Core Lift, Lainnya), Perspektif 3D.

## Struktur
```
pupr-arsitektur/
├── .claude-plugin/plugin.json
├── agents/
│   └── pupr-reviewer.md
└── skills/
    ├── pupr-standar-grafis/
    │   ├── SKILL.md
    │   └── references/{standar-grafis.md, notasi.md}
    ├── pupr-kelengkapan-checklist/
    │   ├── SKILL.md
    │   ├── references/kelengkapan-gambar.json
    │   └── scripts/generate_checklist.py
    └── pupr-deliverable-setup/
        ├── SKILL.md
        ├── references/sheet-sequence.json
        └── scripts/{generate_sheet_list.py, pyrevit_create_sheets.py}
```

## Instalasi

### Opsi A — sebagai plugin (disarankan untuk distribusi)
1. Letakkan folder `pupr-arsitektur/` di repo marketplace plugin Anda (atau repo Git).
2. Di Claude Code, tambahkan marketplace lalu install plugin `pupr-arsitektur`:
   ```
   /plugin marketplace add <url-atau-path-repo>
   /plugin install pupr-arsitektur
   ```
3. Skills & agent otomatis terdaftar (skill tampil sebagai `pupr-arsitektur:<nama-skill>`).

### Opsi B — manual ke `.claude/` (paling sederhana)
Salin isi `skills/` dan `agents/` ke direktori Claude Code:
- Per-proyek: `<proyek>/.claude/skills/` dan `<proyek>/.claude/agents/`
- Global: `~/.claude/skills/` dan `~/.claude/agents/`

```bash
mkdir -p ~/.claude/skills ~/.claude/agents
cp -r pupr-arsitektur/skills/* ~/.claude/skills/
cp -r pupr-arsitektur/agents/* ~/.claude/agents/
```

## Dependensi
- **Skills referensi & generator**: hanya **Python 3** (stdlib) — jalan di mana saja.
- **Fitur eksekusi ke Revit** (`pyrevit_create_sheets.py`, snippet text type, introspeksi sheet oleh
  `pupr-reviewer`): butuh **MCP pyRevit** Anda yang dapat mengeksekusi Python ke Revit. Template
  ditulis dengan Revit API standar (`__revit__`, `Transaction`, `FilteredElementCollector`,
  `ViewSheet.Create`) dan **wajib disesuaikan** dengan nama family kop / parameter proyek.

## Contoh pemakaian
```bash
# Checklist denah & potongan bangunan
python skills/pupr-kelengkapan-checklist/scripts/generate_checklist.py \
  --jenis denah_bangunan potongan_bangunan -o checklist.md

# Daftar gambar: 3 lantai + 1 basement + ada lift
python skills/pupr-deliverable-setup/scripts/generate_sheet_list.py \
  --lantai 3 --basement 1 --ada-lift --format csv -o sheets.csv
```
Dalam percakapan: *"buat checklist kelengkapan denah bangunan"*, *"susun daftar gambar untuk bangunan
4 lantai"*, *"audit set DED ini terhadap PUPR"* (memicu `pupr-reviewer`).

## Sumber & acuan
- Modul Standar Kelengkapan Gambar Arsitektur, Edisi 1 (Sept 2021), Direktorat BTPP, Ditjen Cipta Karya, PUPR.
- Acuan normatif: PP No.16/2021 (pelaksanaan UU No.28/2002 tentang Bangunan Gedung).
- Standar grafis: Standar Informasi Dalam Gambar Manual (Indraprastha & Faisal, ITB, 2015).

Persyaratan dalam plugin ini bersifat **minimal**; kode/nomor gambar & kolom tanda tangan menyesuaikan
peraturan administratif unit kerja masing-masing.
