#!/usr/bin/env python3
"""
generate_checklist.py — Generator checklist kelengkapan gambar arsitektur PUPR 2021.

Membaca data kanonik (references/kelengkapan-gambar.json) dan menghasilkan
checklist Konten / Skala / Notasi (+ presentasi per skala) yang siap dicetak
atau dipakai sebagai dasar QC.

Tidak butuh Revit. Pure Python 3 (stdlib saja).

Contoh:
  # Semua jenis gambar -> Markdown ke stdout
  python generate_checklist.py

  # Hanya jenis tertentu -> file Markdown
  python generate_checklist.py --jenis denah_bangunan potongan_bangunan -o checklist.md

  # Satu kelompok (denah/tampak/potongan/rencana/detail/tapak_kawasan/perspektif) -> CSV
  python generate_checklist.py --kelompok denah --format csv -o denah.csv

  # Tampilkan daftar id jenis gambar yang tersedia
  python generate_checklist.py --list
"""
import argparse
import csv
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "references", "kelengkapan-gambar.json")


def load_data(path=DATA):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def select(data, jenis=None, kelompok=None):
    items = data["jenis_gambar"]
    if jenis:
        wanted = set(jenis)
        items = [j for j in items if j["id"] in wanted]
        missing = wanted - {j["id"] for j in items}
        if missing:
            sys.stderr.write("PERINGATAN: id tidak ditemukan: %s\n" % ", ".join(sorted(missing)))
    if kelompok:
        items = [j for j in items if j["kelompok"] == kelompok]
    return items


def to_markdown(data, items):
    meta = data["meta"]
    out = io.StringIO()
    out.write("# Checklist Kelengkapan Gambar Arsitektur (PUPR 2021)\n\n")
    out.write("> Sumber: %s\n>\n> Acuan normatif: %s\n>\n" % (meta["sumber"], meta["acuan_normatif"]))
    out.write("> Konten/Skala/Notasi = persyaratan **minimal**. Centang `[ ]` -> `[x]` saat terpenuhi.\n\n")
    for j in items:
        out.write("## %s\n\n" % j["nama"])
        out.write("*Kelompok: %s — Modul hlm. %s*\n\n" % (data["kelompok"].get(j["kelompok"], j["kelompok"]), j.get("halaman", "-")))

        out.write("**Skala yang diperbolehkan:** %s\n\n" % ", ".join(j.get("skala", []) or ["-"]))

        out.write("**Konten (wajib):**\n\n")
        for c in j.get("konten", []):
            out.write("- [ ] %s\n" % c)
        out.write("\n")

        out.write("**Notasi minimal (wajib):**\n\n")
        for n in j.get("notasi", []):
            out.write("- [ ] %s\n" % n)
        out.write("\n")

        pres = j.get("presentasi")
        if pres:
            out.write("**Penyajian per skala:**\n\n")
            for skala, rules in pres.items():
                out.write("- *Skala %s:*\n" % skala)
                for r in rules:
                    out.write("    - [ ] %s\n" % r)
            out.write("\n")

        if j.get("catatan"):
            out.write("> Catatan: %s\n\n" % j["catatan"])
        out.write("---\n\n")
    return out.getvalue()


def to_csv(data, items):
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["id_jenis", "nama_gambar", "kelompok", "halaman", "kategori", "skala", "item", "status"])
    for j in items:
        gid, nama, kel, hal = j["id"], j["nama"], j["kelompok"], j.get("halaman", "")
        skala_str = "; ".join(j.get("skala", []))
        for c in j.get("konten", []):
            w.writerow([gid, nama, kel, hal, "KONTEN", skala_str, c, "BELUM"])
        for n in j.get("notasi", []):
            w.writerow([gid, nama, kel, hal, "NOTASI", skala_str, n, "BELUM"])
        for skala, rules in (j.get("presentasi") or {}).items():
            for r in rules:
                w.writerow([gid, nama, kel, hal, "PRESENTASI", skala, r, "BELUM"])
    return out.getvalue()


def main():
    ap = argparse.ArgumentParser(description="Generator checklist kelengkapan gambar PUPR 2021")
    ap.add_argument("--jenis", nargs="+", help="id jenis gambar (lihat --list)")
    ap.add_argument("--kelompok", help="filter kelompok: tapak_kawasan|denah|tampak|potongan|rencana|detail|perspektif")
    ap.add_argument("--format", choices=["md", "csv"], default="md")
    ap.add_argument("-o", "--output", help="tulis ke file (default: stdout)")
    ap.add_argument("--data", default=DATA, help="path kelengkapan-gambar.json")
    ap.add_argument("--list", action="store_true", help="tampilkan id jenis gambar lalu keluar")
    args = ap.parse_args()

    data = load_data(args.data)

    if args.list:
        for j in data["jenis_gambar"]:
            print("%-26s %s" % (j["id"], j["nama"]))
        return

    items = select(data, jenis=args.jenis, kelompok=args.kelompok)
    if not items:
        sys.stderr.write("Tidak ada jenis gambar terpilih.\n")
        sys.exit(1)

    text = to_csv(data, items) if args.format == "csv" else to_markdown(data, items)

    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        sys.stderr.write("Tertulis: %s (%d jenis gambar)\n" % (args.output, len(items)))
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
