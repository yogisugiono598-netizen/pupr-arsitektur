# -*- coding: utf-8 -*-
"""
pyrevit_create_sheets.py — TEMPLATE pembuatan ViewSheet di Revit sesuai Daftar Gambar PUPR 2021.

CARA PAKAI (via MCP pyRevit "execute python in Revit"):
  1. Hasilkan daftar lembar dengan generate_sheet_list.py (CSV) ATAU isi list SHEETS di bawah manual.
  2. Sesuaikan TITLE_BLOCK_NAME dengan nama family title block (kop) di proyekmu.
  3. Kirim isi file ini ke Revit lewat MCP. Script akan membuat ViewSheet ber-nomor & ber-judul.

CATATAN PENTING:
  - Ini TEMPLATE — wajib disesuaikan dengan environment (nama family kop, set parameter kop kustom).
  - Penempatan view ke sheet TIDAK dilakukan otomatis di sini (perlu pemetaan view per lembar yang
    spesifik proyek). Script fokus membuat sheet + nomor + nama (+ opsi set skala kop bila ada param).
  - Kompatibel pyRevit (IronPython / CPython). Bila pakai Revit Python lain, sesuaikan akses `__revit__`.
"""
from Autodesk.Revit.DB import (
    FilteredElementCollector, BuiltInCategory, FamilySymbol,
    ViewSheet, Transaction, ElementId
)

doc = __revit__.ActiveUIDocument.Document  # noqa: F821  (disediakan oleh pyRevit)

# ---------------------------------------------------------------------------
# KONFIGURASI — sesuaikan dengan proyekmu
# ---------------------------------------------------------------------------
# Nama family title block (kop). Kosongkan ("") untuk pakai title block pertama yang ditemukan.
TITLE_BLOCK_NAME = ""  # contoh: "Kop PUPR A3"

# Daftar lembar: (kode/nomor, judul). Tempel hasil dari generate_sheet_list.py atau isi manual.
# Tip: kolom 'kode' -> SHEET_NUMBER, kolom 'judul_gambar' -> SHEET_NAME.
SHEETS = [
    ("AR-01", "RENCANA MASSA BANGUNAN (BLOCK PLAN)"),
    ("AR-02", "RENCANA TAPAK (SITE PLAN)"),
    ("AR-03", "DENAH LANTAI DASAR"),
    # ... tambahkan sesuai daftar gambar ...
]
# ---------------------------------------------------------------------------


def load_sheets_from_csv(path):
    """Opsional: muat SHEETS dari CSV hasil generate_sheet_list.py (kolom: kode, judul_gambar)."""
    import csv
    rows = []
    with open(path, "r") as f:
        for r in csv.DictReader(f):
            rows.append((r["kode"], r["judul_gambar"].upper()))
    return rows


def get_title_block_symbol(doc, name=""):
    """Kembalikan FamilySymbol title block (kop). Pilih by-name bila diisi, else yang pertama."""
    collector = (FilteredElementCollector(doc)
                 .OfCategory(BuiltInCategory.OST_TitleBlocks)
                 .OfClass(FamilySymbol))
    symbols = list(collector)
    if not symbols:
        raise Exception("Tidak ada family Title Block (kop) di proyek. Muat dulu family kop.")
    if name:
        for s in symbols:
            try:
                sym_name = s.Family.Name + " : " + s.get_Parameter(
                    __import__("Autodesk.Revit.DB", fromlist=["BuiltInParameter"]).BuiltInParameter.SYMBOL_NAME_PARAM
                ).AsString()
            except Exception:
                sym_name = s.Family.Name
            if name.lower() in sym_name.lower() or name.lower() in s.Family.Name.lower():
                return s
    return symbols[0]


def existing_sheet_numbers(doc):
    nums = set()
    for vs in FilteredElementCollector(doc).OfClass(ViewSheet):
        try:
            nums.add(vs.SheetNumber)
        except Exception:
            pass
    return nums


def main():
    tb = get_title_block_symbol(doc, TITLE_BLOCK_NAME)
    if not tb.IsActive:
        # Aktifkan symbol bila belum aktif (perlu transaction tersendiri di sebagian versi)
        t0 = Transaction(doc, "Activate title block"); t0.Start()
        tb.Activate(); doc.Regenerate(); t0.Commit()

    existing = existing_sheet_numbers(doc)
    created, skipped = [], []

    t = Transaction(doc, "PUPR — buat ViewSheet"); t.Start()
    try:
        for number, name in SHEETS:
            if number in existing:
                skipped.append(number)
                continue
            sheet = ViewSheet.Create(doc, tb.Id)
            sheet.SheetNumber = number
            sheet.Name = name
            created.append(number)
        t.Commit()
    except Exception as e:
        t.RollBack()
        raise

    print("Sheet dibuat (%d): %s" % (len(created), ", ".join(created) if created else "-"))
    if skipped:
        print("Dilewati karena nomor sudah ada (%d): %s" % (len(skipped), ", ".join(skipped)))
    print("Selesai. Tempatkan view ke masing-masing sheet secara manual / via langkah lanjutan.")


if __name__ == "__main__":
    main()
