# pupr-arsitektur — Claude Code Marketplace

Repo ini adalah **marketplace Claude Code** (`voxel-labs`) yang memuat satu plugin:
**`pupr-arsitektur`** — Standar Kelengkapan & Grafis Gambar Arsitektur PUPR 2021.

> **PENTING:** Plugin Claude Code **bergantung pada struktur folder**. Jangan upload file lepasan
> (flat) ke root repo — skill tidak akan terdeteksi dan 3 berkas `SKILL.md` akan saling menimpa.
> Gunakan **git** agar struktur folder (termasuk `.claude-plugin/`) terjaga.

## Struktur yang benar
```
pupr-arsitektur/                              <- root repo = MARKETPLACE
├── .claude-plugin/
│   └── marketplace.json                      <- katalog marketplace (wajib)
├── LICENSE
├── README.md                                 <- berkas ini
└── plugins/
    └── pupr-arsitektur/                       <- PLUGIN
        ├── .claude-plugin/
        │   └── plugin.json                    <- manifest plugin (wajib)
        ├── README.md
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
Setiap `SKILL.md` **harus** berada di subfolder skill-nya sendiri (nama folder = nama skill).

## Instalasi (untuk pengguna)
```text
/plugin marketplace add yogisugiono598-netizen/pupr-arsitektur
/plugin install pupr-arsitektur@voxel-labs
```
Format install: `<nama-plugin>@<nama-marketplace>` (nama marketplace = field `name` di
`marketplace.json`, yaitu `voxel-labs`).

Memperbarui setelah ada perubahan: `/plugin marketplace update voxel-labs`.

### Alternatif tanpa marketplace (pakai sendiri)
Salin isi `plugins/pupr-arsitektur/skills/*` dan `plugins/pupr-arsitektur/agents/*` ke
`~/.claude/skills/` dan `~/.claude/agents/`.

## Plugin: pupr-arsitektur
Detail lengkap ada di `plugins/pupr-arsitektur/README.md`. Ringkas: 3 skills
(`pupr-standar-grafis`, `pupr-kelengkapan-checklist`, `pupr-deliverable-setup`) + 1 agent
(`pupr-reviewer`) mencakup 24 jenis gambar dari Block Plan sampai Perspektif 3D, dengan integrasi
opsional ke Revit via MCP pyRevit.

## Sumber
Modul Standar Kelengkapan Gambar Arsitektur, Edisi 1 (Sept 2021), Direktorat BTPP, Ditjen Cipta
Karya, Kementerian PUPR. Acuan normatif: PP No.16/2021 (pelaksanaan UU No.28/2002 Bangunan Gedung).
