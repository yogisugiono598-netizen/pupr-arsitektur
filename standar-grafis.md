#!/usr/bin/env python3
"""
generate_sheet_list.py — Generator Daftar Gambar (sheet list) arsitektur sesuai urutan PUPR 2021.

Membaca references/sheet-sequence.json dan menghasilkan daftar lembar gambar dengan kode, judul,
skala, dan ukuran kertas default. Mendukung ekspansi per-lantai dan jumlah minimum (tampak/potongan).

Tidak butuh Revit. Pure Python 3 (stdlib saja). Output dapat dipakai untuk:
- Lampiran "Daftar Gambar" pada dokumen DED.
- Sumber data pembuatan ViewSheet di Revit (lihat pyrevit_create_sheets.py).

Contoh:
  # Daftar lengkap (semua, termasuk yang kondisional) -> Markdown
  python generate_sheet_list.py

  # Bangunan 3 lantai + ada basement (1 lantai) + ada lift -> CSV siap Revit
  python generate_sheet_list.py --lantai 3 --basement 1 --ada-lift --format csv -o sheets.csv

  # Hanya lembar WAJIB, tanpa yang kondisional
  python generate_sheet_list.py --hanya-wajib
"""
import argparse
import csv
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEQ = os.path.join(HERE, "..", "references", "sheet-sequence.json")


def load_seq(path=SEQ):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_rows(seq, lantai=1, basement=0, ada_lift=False, ada_ruang_khusus=False,
               tampak=4, potongan_bangunan=2, hanya_wajib=False, prefix=None):
    """Kembalikan list dict lembar gambar setelah ekspansi & filter."""
    rows = []
    for s in seq["sheets"]:
        sid = s["id"]

        # Filter kondisional
        if hanya_wajib and not s.get("wajib", False):
            continue
        if sid == "denah_basement" and basement <= 0:
            continue
        if sid == "detail_core_lift" and not ada_lift:
            continue
        if sid == "detail_ruang_khusus" and not ada_ruang_khusus and hanya_wajib:
            continue

        base_code = s["kode_default"]
        if prefix:
            # ganti prefix "AR" dengan prefix kustom
            num = base_code.split("-", 1)[1] if "-" in base_code else base_code
            base_code = "%s-%s" % (prefix, num)

        def add(suffix_label="", n=None):
            code = base_code if n is None else "%s%s" % (base_code, chr(96 + n))  # AR-04a, AR-04b...
            nama = s["nama"] + (" — " + suffix_label if suffix_label else "")
            rows.append({
                "kode": code,
                "nama": nama,
                "skala": s["skala_default"],
                "kertas": s["kertas_default"],
                "wajib": "WAJIB" if s.get("wajib") else "KONDISIONAL",
                "kondisi": s.get("kondisi", ""),
            })

        # Ekspansi
        if sid == "denah_bangunan" and lantai > 1:
            # Lantai dasar sudah punya lembar sendiri (denah_lantai_dasar). Sisanya lantai 2..N.
            for lt in range(2, lantai + 1):
                add("Lantai %d" % lt, n=lt - 1)
        elif sid == "denah_basement" and basement > 0:
            for b in range(1, basement + 1):
                add("Basement %d" % b, n=b)
        elif sid == "tampak_bangunan" and tampak > 1:
            for i, arah in enumerate(_arah(tampak), start=1):
                add("Tampak %s" % arah, n=i)
        elif sid == "tampak_tapak" and tampak > 1:
            for i, arah in enumerate(_arah(tampak), start=1):
                add("Tampak Tapak %s" % arah, n=i)
        elif sid == "potongan_bangunan" and potongan_bangunan > 1:
            labels = ["Melintang", "Memanjang"] + ["%d" % k for k in range(3, potongan_bangunan + 1)]
            for i, lab in enumerate(labels[:potongan_bangunan], start=1):
                add("Potongan %s" % lab, n=i)
        elif sid == "potongan_tapak":
            for i, lab in enumerate(["Memanjang", "Melintang"], start=1):
                add("Potongan Tapak %s" % lab, n=i)
        else:
            add()

    # Nomor lembar berurutan + jumlah halaman
    total = len(rows)
    for i, r in enumerate(rows, start=1):
        r["nomor_lembar"] = i
        r["jumlah_halaman"] = total
    return rows


def _arah(n):
    base = ["Depan", "Belakang", "Samping Kiri", "Samping Kanan"]
    if n <= 4:
        return base[:n]
    return base + ["Tambahan %d" % k for k in range(1, n - 3)]


def to_markdown(rows):
    out = io.StringIO()
    out.write("# Daftar Gambar Arsitektur (Urutan PUPR 2021)\n\n")
    out.write("Total lembar: **%d**\n\n" % len(rows))
    out.write("| No. Lembar | Kode | Judul Gambar | Skala | Kertas | Status |\n")
    out.write("|---|---|---|---|---|---|\n")
    for r in rows:
        out.write("| %d/%d | %s | %s | %s | %s | %s |\n" % (
            r["nomor_lembar"], r["jumlah_halaman"], r["kode"], r["nama"],
            r["skala"], r["kertas"], r["wajib"]))
    out.write("\n> Status KONDISIONAL = sertakan hanya bila relevan dengan proyek. "
              "Kode gambar mengikuti kebijakan unit kerja (default prefix AR = Arsitektur).\n")
    return out.getvalue()


def to_csv(rows):
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["nomor_lembar", "jumlah_halaman", "kode", "judul_gambar", "skala", "kertas", "status", "kondisi"])
    for r in rows:
        w.writerow([r["nomor_lembar"], r["jumlah_halaman"], r["kode"], r["nama"],
                    r["skala"], r["kertas"], r["wajib"], r["kondisi"]])
    return out.getvalue()


def main():
    ap = argparse.ArgumentParser(description="Generator daftar gambar arsitektur (urutan PUPR 2021)")
    ap.add_argument("--lantai", type=int, default=1, help="jumlah lantai di atas tanah (termasuk lantai dasar)")
    ap.add_argument("--basement", type=int, default=0, help="jumlah lantai basement")
    ap.add_argument("--ada-lift", action="store_true", help="proyek memiliki lift (sertakan Detail Core Lift)")
    ap.add_argument("--ada-ruang-khusus", action="store_true", help="ada ruang fungsi khusus (Detail Ruang Khusus)")
    ap.add_argument("--tampak", type=int, default=4, help="jumlah arah tampak (min 4)")
    ap.add_argument("--potongan-bangunan", type=int, default=2, help="jumlah potongan bangunan (min 2)")
    ap.add_argument("--hanya-wajib", action="store_true", help="hanya lembar berstatus WAJIB")
    ap.add_argument("--prefix", help="ganti prefix kode (default AR)")
    ap.add_argument("--format", choices=["md", "csv"], default="md")
    ap.add_argument("-o", "--output", help="tulis ke file (default stdout)")
    ap.add_argument("--seq", default=SEQ, help="path sheet-sequence.json")
    args = ap.parse_args()

    seq = load_seq(args.seq)
    rows = build_rows(seq, lantai=args.lantai, basement=args.basement, ada_lift=args.ada_lift,
                      ada_ruang_khusus=args.ada_ruang_khusus, tampak=args.tampak,
                      potongan_bangunan=args.potongan_bangunan, hanya_wajib=args.hanya_wajib,
                      prefix=args.prefix)

    text = to_csv(rows) if args.format == "csv" else to_markdown(rows)
    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        sys.stderr.write("Tertulis: %s (%d lembar)\n" % (args.output, len(rows)))
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
