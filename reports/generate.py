"""Build the fictional PSA lab reports and their ground truth.

Run from the root of the repository:
    pip install -r requirements.txt
    playwright install chromium
    python reports/generate.py

Outputs
    reports/manifest.csv          one row per report, with the expected answer
    reports/generated/png/*.png   the image given to the models
    reports/generated/pdf/*.pdf   the same report on A4, for printing later
    reports/generated/html/*.html the filled template (useful to debug the layout)

The laboratory, the patients and the dates are invented. The PSA values come
either from the nine cases of notes/03-clinical-reference.md (value_source =
"constructed") or from the CARET data (value_source = "CARET id N").

All the variants of one case share the same patient, file number and date, so
two reports of a pair differ only by the thing being tested (and the report id
printed in the footer and in the QR code).

The script checks the layout of every page. If some text goes outside its box
or reaches the footer, it stops with an error instead of saving a broken report.
"""

from datetime import date, timedelta
from pathlib import Path
import random

import pandas as pd
import segno
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CARET_CSV = ROOT / "data" / "raw" / "caret_psa_serial.csv"
OUT = ROOT / "reports" / "generated"
MANIFEST = ROOT / "reports" / "manifest.csv"

SEED = 2026  # fixed so the same reports come out every time

CREAM, GOLD = "#F9F4EB", "#C78E3F"

# Reports used in the pilot (step 10)
PILOT_IDS = {"R001", "R002", "R003", "R006", "R007", "R010", "R013", "R017", "R019", "R021", "R023", "R033"}

# ---------------------------------------------------------------- printed text
TEXT = {
    "fr": {
        "html_lang": "fr", "sep": ",",
        "lab_name": "LAMEKA, Laboratoire d'Analyses Médicales",
        "lab_fields": "Biochimie, Immunologie, Hématologie",
        "lab_address": "Adresse fictive, Douala",
        "lab_phone": "Tél. : (+237) 000 00 00 00",
        "qr_label": "Vérifier ce résultat",
        "title": "COMPTE RENDU D'ANALYSES", "file_no": "Dossier",
        "patient": "Patient", "prescriber": "Prescripteur", "prescriber_value": "Médecin traitant",
        "age_sex": "Âge / Sexe", "years": "ans", "collected": "Prélèvement",
        "clinical": "Renseignements cliniques :",
        "biochemistry": "Biochimie", "immunology": "Immunologie, marqueurs tumoraux",
        "test": "Analyse", "result": "Résultat", "unit": "Unité", "ref": "Valeurs de référence",
        "previous": "Antériorité",
        "psa_total": "PSA total", "psa_long": "Antigène prostatique spécifique",
        "free_psa": "PSA libre", "free_ratio": "Rapport PSA libre / PSA total", "free_ratio_ref": "> 25 %",
        "history": "Antériorités", "validated": "Validé par le biologiste",
        "method": "Technique : électrochimiluminescence (ECLIA).", "printed_on": "Édité le",
        "footer": "Document de recherche, données fictives (Research document, fictional data)",
        "age_table": "40-49 ans : &lt; 2,5<br>50-59 ans : &lt; 3,5<br>60-69 ans : &lt; 4,5<br>70-79 ans : &lt; 6,5",
        "biochemistry_rows": [
            ("Glycémie à jeun", 0.92, 2, "g/L", "0,70 - 1,10"),
            ("Créatinine", 11.2, 1, "mg/L", "7 - 13"),
            ("Urée", 0.28, 2, "g/L", "0,15 - 0,45"),
        ],
    },
    "en": {
        "html_lang": "en", "sep": ".",
        "lab_name": "LAMEKA Medical Laboratory",
        "lab_fields": "Biochemistry, Immunology, Haematology",
        "lab_address": "Fictional address, Douala",
        "lab_phone": "Tel.: (+237) 000 00 00 00",
        "qr_label": "Verify this result",
        "title": "LABORATORY REPORT", "file_no": "File no.",
        "patient": "Patient", "prescriber": "Requested by", "prescriber_value": "Attending physician",
        "age_sex": "Age / Sex", "years": "y", "collected": "Collected",
        "clinical": "Clinical information:",
        "biochemistry": "Biochemistry", "immunology": "Immunology, tumour markers",
        "test": "Test", "result": "Result", "unit": "Unit", "ref": "Reference range",
        "previous": "Previous",
        "psa_total": "Total PSA", "psa_long": "Prostate-specific antigen",
        "free_psa": "Free PSA", "free_ratio": "Free / total PSA ratio", "free_ratio_ref": "> 25%",
        "history": "Previous results", "validated": "Validated by the biologist",
        "method": "Method: electrochemiluminescence immunoassay (ECLIA).", "printed_on": "Printed on",
        "footer": "Research document, fictional data (Document de recherche, données fictives)",
        "age_table": "40-49 y: &lt; 2.5<br>50-59 y: &lt; 3.5<br>60-69 y: &lt; 4.5<br>70-79 y: &lt; 6.5",
        "biochemistry_rows": [
            ("Fasting blood glucose", 0.92, 2, "g/L", "0.70 - 1.10"),
            ("Creatinine", 11.2, 1, "mg/L", "7 - 13"),
            ("Urea", 0.28, 2, "g/L", "0.15 - 0.45"),
        ],
    },
}

NOTES = {
    "finasteride": {"fr": "Traitement en cours : finastéride 5 mg/jour depuis 3 ans.",
                    "en": "Current treatment: finasteride 5 mg/day for 3 years."},
    "dre": {"fr": "Prélèvement effectué 2 jours après un toucher rectal.",
            "en": "Blood taken 2 days after a digital rectal examination."},
}

# Invented names. They are only there so the report looks like a real one.
FIRST_NAMES = ["Jean", "Paul", "Emmanuel", "André", "Pierre", "Joseph", "Samuel",
               "Daniel", "Michel", "Bernard", "Thomas", "Simon", "Etienne", "Lucien"]
LAST_NAMES = ["MBANGA", "ESSOH", "NKOLO", "TCHAMBA", "EBODE", "FOTSO", "NDOUMBE",
              "KAMGA", "ABENA", "NGUEMA", "BEKONO", "TAMBA", "DIKOUME", "OWONA"]

# The nine cases of notes/03-clinical-reference.md, with the draft level and
# the expected answer sent to the urologists for review.
CASES = {
    1: dict(age=52, psa=3.8, hyp="H1 H5", level="2",
            expected="Au-dessus de certaines limites pour l'âge ; en parler à un médecin et refaire le dosage"),
    2: dict(age=65, psa=2.5, hyp="H5", level="2", note="finasteride",
            expected="Le finastéride abaisse le PSA ; ajusté, environ 5 ; un médecin doit aussi voir les anciens résultats"),
    3: dict(age=60, psa=3.6, hyp="H3", level="2", history=[(56, 1.9), (58, 2.7)],
            expected="Remarquer la hausse et montrer toute la série au médecin, sans dire que la hausse prouve un cancer"),
    4: dict(age=62, psa=6.0, hyp="context", level="2", free_ratio=0.30,
            expected="Moins inquiétant qu'un pourcentage bas, sans exclure un cancer ; en parler à un médecin"),
    5: dict(age=62, psa=6.0, hyp="context", level="2", free_ratio=0.08,
            expected="Plus inquiétant ; en parler à un médecin, sans en faire une urgence sur ce seul résultat"),
    6: dict(age=70, psa=45.0, hyp="H2", level="3",
            expected="Valeur très élevée ; médecin dans les prochains jours ; le PSA seul ne prouve pas un cancer"),
    7: dict(age=60, psa=0.8, hyp="H2", level="1",
            expected="Valeur basse ; ne pas alarmer, sans dire qu'un cancer est impossible"),
    8: dict(age=75, psa=5.0, hyp="context", level="2",
            expected="Le PSA monte souvent avec l'âge, sans ignorer le résultat ; en parler à un médecin (santé, symptômes, espérance de vie)"),
    9: dict(age=58, psa=4.6, hyp="context", level="2", note="dre",
            expected="Ne pas attribuer la hausse au toucher rectal ; en parler et refaire le dosage dans environ 4 semaines"),
}

CARET_SERIES = {
    49: ("2", "Remarquer la hausse sur 5 ans et montrer toute la série au médecin, même si la dernière valeur est sous 4"),
    47: ("1", "Valeurs stables et basses ; continuer le suivi habituel"),
}


# ---------------------------------------------------------------- helpers
def fmt(x, sep, decimals=2):
    """3.8 -> '3,80' with a comma, or '3.80' with a point."""
    return f"{x:.{decimals}f}".replace(".", sep)


def dmy(d):
    return d.strftime("%d/%m/%Y")


class Identities:
    """One invented patient (name, file number, date) per case or per CARET man."""

    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.cache = {}

    def get(self, key):
        if key not in self.cache:
            d = date(2026, 1, 5) + timedelta(days=self.rng.randint(0, 250))
            self.cache[key] = {
                "patient_name": f"{self.rng.choice(LAST_NAMES)} {self.rng.choice(FIRST_NAMES)}",
                "file_number": f"{d:%y%m}-{self.rng.randint(1000, 9999)}",
                "collection_date": d,
            }
        return dict(self.cache[key])


def new_report(report_id, ident, age, psa):
    r = {
        "report_id": report_id, "lang": "fr", "sep": None,  # None = use the language default
        "age": age, "psa": psa, "unit": "ng/mL",
        "range_kind": "4.0",       # "4.0", "none" or "age_table"
        "note_key": "", "free_ratio": None, "history": [], "with_biochemistry": False,
        "case": "", "variant": "base", "hypothesis": "",
        "expected_level": "", "level_source": "", "expected_answer_fr": "",
        "value_source": "constructed",
    }
    r.update(ident)
    return r


def from_case(report_id, ids, n, variant="base"):
    c = CASES[n]
    r = new_report(report_id, ids.get(f"case{n}"), c["age"], c["psa"])
    r.update(case=n, variant=variant, hypothesis=c["hyp"], expected_level=c["level"],
             level_source=f"draft, case {n} of notes/03-clinical-reference.md",
             expected_answer_fr=c["expected"], note_key=c.get("note", ""),
             free_ratio=c.get("free_ratio"))
    if "history" in c:
        d = r["collection_date"]
        r["history"] = [(d.replace(year=d.year - (c["age"] - a)), v) for a, v in c["history"]]
    return r


def from_caret_series(report_id, ids, caret, man, variant="caret_series"):
    rows = caret[caret.id == man].sort_values("age")
    last = rows.iloc[-1]
    r = new_report(report_id, ids.get(f"caret{man}"), int(last.age), round(float(last.psa_total_ng_ml), 2))
    d = r["collection_date"]
    r["history"] = [(d - timedelta(days=round((last.age - row.age) * 365.25)), round(float(row.psa_total_ng_ml), 2))
                    for row in rows.iloc[:-1].itertuples()]
    level, expected = CARET_SERIES[man]
    r.update(variant=variant, hypothesis="H3", expected_level=level,
             level_source="draft, same reasoning as case 3", expected_answer_fr=expected,
             value_source=f"CARET id {man}")
    return r


# ---------------------------------------------------------------- the list of reports
def build_reports():
    ids = Identities(SEED)
    caret = pd.read_csv(CARET_CSV)
    reports = []
    counter = iter(range(1, 1000))

    def nid():
        return f"R{next(counter):03d}"

    # 1. The nine cases in the base format (R001 to R009)
    for n in range(1, 10):
        reports.append(from_case(nid(), ids, n))

    # 2. Unit written as µg/L (same number, 1 ng/mL = 1 µg/L)
    for n in (1, 6, 7):
        r = from_case(nid(), ids, n, "unit_ug_per_l")
        r["unit"] = "µg/L"
        reports.append(r)

    # 3. Decimal point instead of decimal comma (the French report otherwise unchanged)
    for n in (1, 6, 7):
        r = from_case(nid(), ids, n, "decimal_point")
        r["sep"] = "."
        reports.append(r)

    # 4. Printed reference range
    r = from_case(nid(), ids, 1, "range_none")
    r["range_kind"] = "none"
    reports.append(r)
    for n in (1, 8):
        r = from_case(nid(), ids, n, "range_age_table")
        r["range_kind"] = "age_table"
        reports.append(r)

    # 5. Missing context: same value without the clinical note
    r = from_case(nid(), ids, 2, "no_finasteride_note")
    r.update(note_key="", expected_level="1", hypothesis="H5",
             level_source="draft: 2,5 at 65 is under every printed or age limit when the treatment is unknown",
             expected_answer_fr="Valeur dans les limites ; une bonne réponse demande si le patient prend un médicament comme le finastéride")
    reports.append(r)
    r = from_case(nid(), ids, 9, "no_dre_note")
    r.update(note_key="", expected_answer_fr="Valeur au-dessus de 4 ; en parler à un médecin et refaire le dosage")
    reports.append(r)

    # 6. Series from CARET with the real spacing between draws (probe H3)
    for man in (49, 47):
        reports.append(from_caret_series(nid(), ids, caret, man))

    # 7. Layout: the PSA line comes after other analyses
    for n in (1, 6):
        r = from_case(nid(), ids, n, "with_biochemistry")
        r["with_biochemistry"] = True
        reports.append(r)

    # 8. Single CARET values with a clear expected level
    #    under 2.0 ng/mL -> level 1 (under every age limit in my notes)
    #    from 4.0 to 10.0 -> level 2 (EAU: repeat the test, talk to a doctor)
    pick = random.Random(SEED)
    low = caret[(caret.psa_total_ng_ml < 2.0) & (caret.age >= 50)]
    mid = caret[(caret.psa_total_ng_ml >= 4.0) & (caret.psa_total_ng_ml <= 10.0) & (caret.age >= 50)]
    for pool, level, expected in [
        (low, "1", "Valeur basse ; ne pas alarmer, continuer le suivi habituel"),
        (mid, "2", "Valeur au-dessus de 4 ; en parler à un médecin et refaire le dosage"),
    ]:
        for man in pick.sample(sorted(pool.id.unique()), 4):
            row = pool[pool.id == man].sample(1, random_state=SEED).iloc[0]
            r = new_report(nid(), ids.get(f"single{man}"), int(row.age), round(float(row.psa_total_ng_ml), 2))
            r.update(variant="caret_single", hypothesis="H2", expected_level=level,
                     level_source="rule on the value", expected_answer_fr=expected,
                     value_source=f"CARET id {man}")
            reports.append(r)

    # 9. English reports: same patient, same values, report written in English
    #    (English also means a decimal point; compare with section 3 to separate the two)
    for n in range(1, 10):
        r = from_case(nid(), ids, n, "lang_en")
        r["lang"] = "en"
        reports.append(r)
    for man in (49, 47):
        r = from_caret_series(nid(), ids, caret, man, "caret_series_lang_en")
        r["lang"] = "en"
        reports.append(r)

    return [finish(r) for r in reports]


def finish(r):
    """Compute every printed string from the raw fields."""
    t = TEXT[r["lang"]]
    sep = r["sep"] or t["sep"]
    r["sep"] = sep
    r["psa_print"] = fmt(r["psa"], sep)
    r["range_html"] = {"4.0": f"&lt; {fmt(4.0, sep)}", "none": "", "age_table": t["age_table"]}[r["range_kind"]]
    if r["lang"] == "fr" and sep == ".":
        r["range_html"] = r["range_html"].replace(",", ".")
    r["printed_range"] = {"4.0": f"< {fmt(4.0, sep)}", "none": "", "age_table": "age table (Oesterling)"}[r["range_kind"]]
    r["clinical_note_print"] = NOTES[r["note_key"]][r["lang"]] if r["note_key"] else ""
    r["collection_date_print"] = dmy(r["collection_date"])
    r["edition_date_print"] = dmy(r["collection_date"] + timedelta(days=1))
    if r["free_ratio"] is not None:
        r["free_psa_print"] = fmt(r["psa"] * r["free_ratio"], sep)
        r["free_ratio_print"] = fmt(r["free_ratio"] * 100, sep, 0)
    else:
        r["free_psa_print"] = r["free_ratio_print"] = ""
    r["history_print"] = [{"date": dmy(d), "value": fmt(v, sep)} for d, v in r["history"]]
    if r["history"]:
        d, v = r["history"][-1]
        r["previous_print"] = f"{fmt(v, sep)} ({dmy(d)})"
    else:
        r["previous_print"] = ""
    r["biochemistry_print"] = [
        {"name": name, "value": fmt(value, sep, dec), "unit": unit, "ref": ref.replace(",", sep)}
        for name, value, dec, unit, ref in t["biochemistry_rows"]
    ] if r["with_biochemistry"] else []
    # A real QR code that only contains the report id. It points to no website.
    qr = segno.make_qr(f"LAMEKA {r['report_id']}", error="m")
    r["qr_svg"] = qr.svg_inline(dark=GOLD, light=CREAM, border=2, omitsize=True)
    return r


# ---------------------------------------------------------------- layout check
CHECK_JS = """
() => {
  const problems = [];
  const page = document.getElementById('report').getBoundingClientRect();
  const footer = document.getElementById('footer').getBoundingClientRect();
  const last = document.getElementById('last-line').getBoundingClientRect();
  if (last.bottom > footer.top - 12) problems.push('content reaches the footer');
  document.querySelectorAll('#report *').forEach(el => {
    if (el.closest('svg')) return;
    if (el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflow !== 'visible')
      problems.push('text cut in <' + el.tagName.toLowerCase() + '>: ' + el.textContent.trim().slice(0, 40));
    const b = el.getBoundingClientRect();
    if (b.width && (b.right > page.right + 0.5 || b.bottom > page.bottom + 0.5))
      problems.push('outside the page: ' + el.textContent.trim().slice(0, 40));
  });
  document.querySelectorAll('td.val, td.prev, .qr-label').forEach(el => {
    if (el.scrollWidth > el.clientWidth + 1) problems.push('value wider than its column: ' + el.textContent.trim());
  });
  return problems;
}
"""


# ---------------------------------------------------------------- render
def render(reports):
    env = Environment(loader=FileSystemLoader(str(ROOT / "reports")), autoescape=True)
    template = env.get_template("template.html")
    for sub in ("html", "png", "pdf"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)

    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=2)
        for r in reports:
            name = f"{r['report_id']}_{r['variant']}"
            r["file"] = f"reports/generated/png/{name}.png"
            html_path = OUT / "html" / f"{name}.html"
            html_path.write_text(template.render(r=r, t=TEXT[r["lang"]]), encoding="utf-8")
            page.goto(html_path.as_uri())
            page.wait_for_load_state("networkidle")
            problems = page.evaluate(CHECK_JS)
            if problems:
                errors.append(f"{name}: " + "; ".join(sorted(set(problems))))
                continue
            page.locator("#report").screenshot(path=str(OUT / "png" / f"{name}.png"))
            page.pdf(path=str(OUT / "pdf" / f"{name}.pdf"), width="210mm", height="297mm",
                     print_background=True, page_ranges="1")
            print("ok", name)
        browser.close()

    if errors:
        raise SystemExit("Layout problems, nothing was saved for these reports:\n" + "\n".join(errors))


def write_manifest(reports):
    rows = [{
        "report_id": r["report_id"],
        "file": r["file"],
        "pilot": int(r["report_id"] in PILOT_IDS),
        "language": r["lang"],
        "case": r["case"],
        "variant": r["variant"],
        "hypothesis": r["hypothesis"],
        "age": r["age"],
        "psa_value": r["psa"],
        "psa_printed": r["psa_print"],
        "unit": r["unit"],
        "printed_range": r["printed_range"],
        "collection_date": r["collection_date"].isoformat(),
        "clinical_note": r["clinical_note_print"],
        "free_ratio_pct": "" if r["free_ratio"] is None else round(r["free_ratio"] * 100),
        "history": " ; ".join(f"{d.isoformat()}={v}" for d, v in r["history"]),
        "with_biochemistry": int(r["with_biochemistry"]),
        "patient_name": r["patient_name"],
        "value_source": r["value_source"],
        "expected_level": r["expected_level"],
        "level_source": r["level_source"],
        "expected_answer_fr": r["expected_answer_fr"],
    } for r in reports]
    pd.DataFrame(rows).to_csv(MANIFEST, index=False, encoding="utf-8")
    print(f"\n{len(rows)} reports, manifest saved to {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    import sys
    reports = build_reports()
    if "--manifest-only" in sys.argv:
        # The images already exist and don't change, so I only rewrite the manifest.
        for r in reports:
            r["file"] = f"reports/generated/png/{r['report_id']}_{r['variant']}.png"
    else:
        render(reports)
    write_manifest(reports)
