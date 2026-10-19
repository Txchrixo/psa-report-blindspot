"""Builds results/scoring/annotate.html, the page I use to score in the browser.

Run from the repo root: python scoring/make_annotator.py
Same answers, ids and order as to_score.xlsx. The export gives back the same xlsx.
The page opens with the scores already in to_score.xlsx. What I change in the
browser is kept there and wins over the sheet.
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_sheet import (AGE_LIMITS, AUTO, CHOICES, FILE_COLUMNS, OUT, PHOTO_COLUMNS,
                        PHOTO_REPORTS, ROOT, RULES, build, limit_text, load_answers, report_text)

TEMPLATE = Path(__file__).resolve().parent / "annotate_template.html"


def limit_fr(r):
    if r.printed_range == "":
        return "aucune limite imprimée"
    if r.printed_range.startswith("age table"):
        age = int(r.age)
        lo, hi, lim = next(row for row in AGE_LIMITS if row[0] <= age <= row[1])
        return f"tableau par âge, sa ligne est {lo}-{hi} ans : < {str(lim).replace('.', ',')}"
    return r.printed_range


def facts(r):
    en = [("Age", f"{r.age} y"), ("PSA", f"{r.psa_printed} {r.unit}"), ("Limit", limit_text(r).replace("limit ", ""))]
    fr = [("Âge", f"{r.age} ans"), ("PSA", f"{r.psa_printed} {r.unit}"), ("Limite", limit_fr(r))]
    if r.free_ratio_pct:
        en.append(("Free PSA", f"{r.free_ratio_pct} %"))
        fr.append(("PSA libre", f"{r.free_ratio_pct} %"))
    if r.clinical_note:
        en.append(("Note", r.clinical_note))
        fr.append(("Note", r.clinical_note))
    if r.history:
        older = r.history.replace("=", " : ").replace(" ; ", " · ")
        en.append(("Older", older))
        fr.append(("Avant", older))
    if r.with_biochemistry == "1":
        en.append(("Other", "glucose, creatinine and urea printed above"))
        fr.append(("Autres", "glycémie, créatinine et urée imprimées au-dessus"))
    return {"en": en, "fr": fr}


def shows(r):
    fr = [f"{r.age} ans", f"PSA {r.psa_printed} {r.unit}", limit_fr(r) if r.printed_range else "aucune limite imprimée"]
    if r.printed_range and not r.printed_range.startswith("age table"):
        fr[2] = f"limite {r.printed_range}"
    if r.free_ratio_pct:
        fr.append(f"PSA libre {r.free_ratio_pct} %")
    if r.clinical_note:
        fr.append(f"note : {r.clinical_note}")
    if r.history:
        fr.append("avant : " + r.history.replace("=", " → "))
    if r.with_biochemistry == "1":
        fr.append("glycémie, créatinine et urée imprimées au-dessus")
    return {"en": report_text(r), "fr": " · ".join(fr)}


def items_for(data, tab, columns):
    out = []
    for _, r in data.iterrows():
        auto = {c: (r[c] if r[c] == "na" else int(r[c])) for c in columns if c in AUTO and r[c] != ""}
        na = [c for c in columns if r[c] == "na"]
        out.append({
            "id": r.answer_id, "tab": tab, "report": r.report_id, "prompt": r.prompt_id,
            "photo": r.photo_id.replace(r.report_id + "_", "") if tab == "photos" else "",
            "img": "../../" + (r.file_photo if tab == "photos" else r.file),
            "facts": facts(r), "shows": shows(r),
            "level": r.expected_level, "expected": r.expected_answer_fr,
            "answer": r.answer, "cut": bool(r.hit_max_tokens),
            "auto": auto, "na": na, "model": r.model_id,
        })
    return out


def collect():
    manifest = pd.read_csv(ROOT / "reports" / "manifest.csv", dtype=str).fillna("")
    photos_csv = pd.read_csv(ROOT / "photos" / "photos.csv", dtype=str)[["photo_id", "file"]].rename(columns={"file": "file_photo"})
    keys = []
    files = build(load_answers("full"), manifest, FILE_COLUMNS, "F", keys)
    photo_answers = load_answers("photos")
    photo_answers = photo_answers[(photo_answers.prompt_id == "fr") & photo_answers.report_id.isin(PHOTO_REPORTS)]
    photo_answers = photo_answers.merge(photos_csv, on="photo_id", how="left")
    photos = build(photo_answers, manifest, PHOTO_COLUMNS, "P", keys)
    return items_for(files, "files", FILE_COLUMNS) + items_for(photos, "photos", PHOTO_COLUMNS)


def page(items, mode="mine", scores=None, title="Answer annotation"):
    if mode == "mine":
        for it in items:
            it.pop("model")
    meta = {
        "mode": mode, "title": title,
        "columns": {"files": FILE_COLUMNS, "photos": PHOTO_COLUMNS},
        "choices": {c: CHOICES.get(c, "1,0").split(",") for c in set(FILE_COLUMNS + PHOTO_COLUMNS)},
        "auto": sorted(AUTO), "rules": RULES,
        "storageKey": "psa-annotations-v1" if mode == "mine" else "psa-annotations-review-v1",
    }
    data = json.dumps({"meta": meta, "items": items, "scores": scores or {}}, ensure_ascii=False)
    html = TEMPLATE.read_text(encoding="utf-8")
    return html.replace("__TITLE__", title).replace("/*__DATA__*/null", data.replace("</", "<\\/"))


def sheet_scores():
    # what is already in to_score.xlsx, so the page opens with it
    sheet = OUT / "to_score.xlsx"
    if not sheet.exists():
        return {}
    scores = {}
    for tab, columns in [("files", FILE_COLUMNS), ("photos", PHOTO_COLUMNS)]:
        data = pd.read_excel(sheet, sheet_name=tab, dtype=object)
        for _, row in data.iterrows():
            values = {}
            for c in columns:
                v = "" if pd.isna(row[c]) else str(row[c]).strip().lower()
                v = v[:-2] if v.endswith(".0") else v
                if v not in ("", "na"):
                    values[c] = v
            note = "" if pd.isna(row["note"]) else str(row["note"])
            if str(row.get("done", "")).strip() == "ok" or note or any(c not in AUTO for c in values):
                scores[row.answer_id] = {"v": values, "note": note, "touched": True}
    return scores


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    items = collect()
    scores = sheet_scores()
    (OUT / "annotate.html").write_text(page(items, scores=scores), encoding="utf-8")
    print(f"{len(scores)} answers already scored in to_score.xlsx")
    print(f"{len(items)} answers written to {OUT / 'annotate.html'}")


if __name__ == "__main__":
    main()
