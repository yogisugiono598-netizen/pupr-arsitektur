# PUPR Arsitektur — Claude Code Marketplace

Marketplace plugin Claude Code yang memuat **`pupr-arsitektur`**: standar **kelengkapan & grafis
gambar arsitektur** menurut *Modul Standar Kelengkapan Gambar Arsitektur* Kementerian PUPR, Ditjen
Cipta Karya (Edisi 1, September 2021).

Isi plugin: **3 skills + 1 agent QA**, mencakup 24 jenis gambar dari Block Plan sampai Perspektif 3D.
Detail lengkap ada di [README plugin](plugins/pupr-arsitektur/README.md).

## Struktur

```
.claude-plugin/marketplace.json
LICENSE
README.md
plugins/
└── pupr-arsitektur/
    ├── .claude-plugin/plugin.json
    ├── README.md
    ├── agents/pupr-reviewer.md
    └── skills/
        ├── pupr-standar-grafis/
        ├── pupr-kelengkapan-checklist/
        └── pupr-deliverable-setup/
```

## Instalasi

Di Claude Code, tambahkan marketplace ini lalu install plugin-nya:

```
/plugin marketplace add yogisugiono598-netizen/pupr-arsitektur
/plugin install pupr-arsitektur
```

Skills & agent otomatis terdaftar (skill tampil sebagai `pupr-arsitektur:<nama-skill>`).

## Lisensi

[MIT](LICENSE) © 2026 goyy16
