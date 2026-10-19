"""Reads my filled sheet and writes results/scores.csv and results/scores_photos.csv.

Run from the repo root: python scoring/read_sheet.py
It stops if a cell is empty or wrong. Add --partial to write anyway.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_sheet import CHOICES, FILE_COLUMNS, PHOTO_COLUMNS, ROOT

SHEET = ROOT / "results" / "scoring" / "to_score.xlsx"
KEY = ROOT / "results" / "scoring" / "key.csv"


def clean(value):
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    return text[:-2] if text.endswith(".0") else text


def read(tab, columns, key):
    sheet = pd.read_excel(SHEET, sheet_name=tab, dtype=object)
    problems = []
    for column in columns:
        allowed = set(CHOICES.get(column, "1,0").split(",")) | {"na"}
        values = sheet[column].map(clean)
        for answer_id, value in zip(sheet.answer_id, values):
            if value == "":
                problems.append(f"{tab} {answer_id} {column} is empty")
            elif value not in allowed:
                problems.append(f"{tab} {answer_id} {column} = '{value}', expected one of {sorted(allowed)}")
        sheet[column] = values.replace({"na": "", "none": ""})
    sheet["note"] = sheet["note"].fillna("")
    scores = key.merge(sheet[["answer_id"] + columns + ["note"]], on="answer_id", how="inner")
    return scores, problems


def main():
    key = pd.read_csv(KEY, dtype=str).fillna("")
    files, problems_files = read("files", FILE_COLUMNS, key)
    photos, problems_photos = read("photos", PHOTO_COLUMNS, key)
    problems = problems_files + problems_photos

    for line in problems[:40]:
        print(line)
    if len(problems) > 40:
        print(f"... and {len(problems) - 40} more")
    if problems and "--partial" not in sys.argv:
        print(f"{len(problems)} cells to fix, nothing written.")
        return

    files.drop(columns=["photo_id"]).to_csv(ROOT / "results" / "scores.csv", index=False)
    photos.to_csv(ROOT / "results" / "scores_photos.csv", index=False)
    print(f"Wrote {len(files)} rows to results/scores.csv and {len(photos)} rows to results/scores_photos.csv")


if __name__ == "__main__":
    main()
