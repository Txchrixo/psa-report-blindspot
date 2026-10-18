"""Prepare the photos of the printed reports for the repository and the models.

Run from the root of the repository:
    python photos/prepare_photos.py

What it does
1. Phone photos: photos/phone_original/{light,shade}/R001_light.jpg ...
   Some were taken at 200 megapixels, which is far too heavy for git.
   I save a copy with the long side at 4080 px (the size of my 12 MP photos),
   with no camera data, in photos/phone/{light,shade}/.
   The originals stay on my computer and are not committed.
2. WhatsApp photos: photos/whatsapp/{light,shade}/R001_light_wa.jpeg
   These are the real files downloaded from WhatsApp. I don't touch them,
   I only check that they carry no camera data.
3. It writes photos/photos.csv with one line per photo.
"""

from pathlib import Path
import csv
import re

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parent
ORIGINALS = ROOT / "phone_original"
PHONE = ROOT / "phone"
WHATSAPP = ROOT / "whatsapp"
LONG_EDGE = 4080
NAME = re.compile(r"^(R\d{3})_(light|shade)(_wa)?$")


def has_camera_data(path):
    with Image.open(path) as im:
        exif = im.getexif()
        return len(exif) > 0 and any(k not in (0x0112,) for k in exif.keys()), (0x8825 in exif)


def save_phone_copy(src, dst):
    im = Image.open(src)
    im.draft("RGB", (LONG_EDGE, LONG_EDGE))
    im.load()
    im = ImageOps.exif_transpose(im).convert("RGB")
    if max(im.size) > LONG_EDGE:
        im.thumbnail((LONG_EDGE, LONG_EDGE), Image.Resampling.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, format="JPEG", quality=92)  # a new file, without any EXIF or GPS


def main():
    rows, problems = [], []

    for src in sorted(ORIGINALS.rglob("*.jpg")):
        m = NAME.match(src.stem)
        if not m:
            problems.append(f"name not understood: {src}")
            continue
        dst = PHONE / src.parent.name / src.name
        if not dst.exists():
            save_phone_copy(src, dst)
        rows.append((dst, m.group(1), m.group(2), 0))

    for src in sorted(list(WHATSAPP.rglob("*.jpeg")) + list(WHATSAPP.rglob("*.jpg"))):
        m = NAME.match(src.stem)
        if not m or not m.group(3):
            problems.append(f"name not understood: {src}")
            continue
        rows.append((src, m.group(1), m.group(2), 1))

    out = []
    for path, report_id, light, whatsapp in rows:
        exif_left, gps_left = has_camera_data(path)
        if gps_left:
            problems.append(f"GPS data found in {path}")
        with Image.open(path) as im:
            w, h = im.size
        out.append({
            "photo_id": path.stem,
            "report_id": report_id,
            "light": light,
            "whatsapp": whatsapp,
            "file": path.relative_to(ROOT.parent).as_posix(),
            "width": w,
            "height": h,
            "camera_data": int(exif_left),
        })

    out.sort(key=lambda r: (r["report_id"], r["light"], r["whatsapp"]))
    with open(ROOT / "photos.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        writer.writeheader()
        writer.writerows(out)

    print(f"{len(out)} photos in photos/photos.csv")
    for kind in ((0, "light"), (0, "shade"), (1, "light"), (1, "shade")):
        n = sum(1 for r in out if (r["whatsapp"], r["light"]) == kind)
        print(f"  {'whatsapp' if kind[0] else 'phone':8} {kind[1]:5} {n}")
    dup = {}
    for r in out:
        dup.setdefault((r["report_id"], r["light"], r["whatsapp"]), []).append(r["file"])
    for k, v in dup.items():
        if len(v) > 1:
            problems.append(f"two photos for {k}: {v}")
    print("problems:" if problems else "no problem found")
    for p in problems:
        print("  ", p)


if __name__ == "__main__":
    main()
