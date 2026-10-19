"""Counts the scores for each hypothesis and draws two figures.

Run from the repo root: python analysis/analyze.py

Reads results/scores.csv, results/scores_photos.csv, the photo answers in
results/photos/ and reports/manifest.csv. Writes results/analysis/summary.md,
one csv per table in results/analysis/tables/, and the figures in
results/analysis/figures/.

Every number is written as "x of n", with the percentage only when n is 20 or more.
"""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scoring"))
from make_sheet import HARD_TO_READ, load_answers, reads_value

OUT = ROOT / "results" / "analysis"
MODELS = ["Qwen", "MedGemma"]
COLORS = {"Qwen": "#2a78d6", "MedGemma": "#eb6834"}

RISING = ["R003", "R021", "R035", "R042"]
STABLE = ["R022", "R043"]
FINASTERIDE = ["R002", "R034"]
RECTAL_EXAM = ["R009", "R041"]


def short(model_id):
    return "Qwen" if "Qwen" in model_id else "MedGemma"


def of(hits, n):
    if n == 0:
        return "-"
    if n < 20:
        return f"{hits} of {n}"
    return f"{hits} of {n} ({round(100 * hits / n)}%)"


def count(series, value="1"):
    s = series.dropna()
    return of(int((s == value).sum()), len(s))


def load():
    manifest = pd.read_csv(ROOT / "reports" / "manifest.csv", dtype=str).fillna("")
    keep = ["report_id", "variant", "language", "age", "psa_value", "printed_range", "expected_level"]
    files = pd.read_csv(ROOT / "results" / "scores.csv", dtype=str).merge(manifest[keep], on="report_id")
    photos = pd.read_csv(ROOT / "results" / "scores_photos.csv", dtype=str).merge(manifest[keep], on="report_id")
    for d in (files, photos):
        d["model"] = d.model_id.map(short)
        d["below_limit"] = d.psa_value.astype(float) < 4
    photos["condition"] = photos.photo_id.str.replace(r"^R\d+_", "", regex=True)

    # every photo answer, both questions, only the automatic columns
    every = load_answers("photos").merge(manifest[["report_id", "psa_value"]], on="report_id")
    every["model"] = every.model_id.map(short)
    every["condition"] = every.photo_id.str.replace(r"^R\d+_", "", regex=True)
    every["reads_value"] = [reads_value(a, v) for a, v in zip(every.answer, every.psa_value)]
    every["hedges_image"] = every.answer.map(lambda a: int(bool(HARD_TO_READ.search(a))))
    return files, photos, every


def table(rows, columns):
    return pd.DataFrame(rows, columns=columns)


def to_md(df):
    head = "| " + " | ".join(df.columns) + " |"
    line = "| " + " | ".join("---" for _ in df.columns) + " |"
    body = ["| " + " | ".join(str(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join([head, line] + body)


def overview(files):
    columns = ["reads_value", "range_comparison", "says_normal", "uses_age", "uses_note", "sees_trend",
               "asks_missing", "false_reassurance", "invents", "talks_fictional"]
    rows = []
    for c in columns:
        rows.append([c] + [count(files[files.model == m][c]) for m in MODELS])
    return table(rows, ["column (1 means yes)"] + MODELS)


def comparison(files):
    rows = []
    groups = [
        ("value below the printed limit", files.below_limit),
        ("value above the printed limit", ~files.below_limit),
        ("question in French", files.prompt_id == "fr"),
        ("question in English", files.prompt_id == "en"),
        ("report in µg/L", files.variant == "unit_ug_per_l"),
        ("report with a decimal point", files.variant == "decimal_point"),
        ("report in English", files.language == "en"),
    ]
    for name, mask in groups:
        rows.append([name] + [count(files[mask & (files.model == m)].range_comparison, "0") for m in MODELS])
    return table(rows, ["wrong side of the limit, when it compares"] + MODELS)


def echo(files):
    # value under the printed limit, but my expected level is 2
    trap = files[files.below_limit & (files.expected_level == "2")]
    rows = []
    for name, col, value in [("calls the result normal", "says_normal", "1"),
                             ("false reassurance", "false_reassurance", "1"),
                             ("level 1, nothing to do", "level_given", "1")]:
        rows.append([name] + [count(trap[trap.model == m][col], value) for m in MODELS])
    rows.append(["asks for a doctor, but after putting the value above the limit"] +
                [of(int(((trap.model == m) & (trap.range_comparison == "0") & trap.level_given.isin(["2", "3"])).sum()),
                    int((trap.model == m).sum())) for m in MODELS])
    reports = ", ".join(sorted(trap.report_id.unique()))
    return table(rows, ["value under the limit, level 2 expected"] + MODELS), reports


def age(files):
    age_table = files[files.variant == "range_age_table"]
    rows = [["uses the age to read the value, all reports"] + [count(files[files.model == m].uses_age) for m in MODELS],
            ["right row of the age table (R017, R018)"] + [count(age_table[age_table.model == m].range_comparison) for m in MODELS]]
    return table(rows, ["age"] + MODELS)


def levels(files):
    rows = []
    for m in MODELS:
        g = files[files.model == m]
        for exp in ["1", "2", "3"]:
            h = g[g.expected_level == exp]
            given = h.level_given.fillna("none")
            rows.append([m, exp, len(h)] + [int((given == v).sum()) for v in ["1", "2", "3", "none"]])
    return table(rows, ["model", "expected level", "answers", "gave 1", "gave 2", "gave 3", "no advice"])


def level_fit(files):
    rows = []
    for m in MODELS:
        g = files[(files.model == m) & files.level_given.notna()]
        given, exp = g.level_given.astype(int), g.expected_level.astype(int)
        n = len(g)
        rows.append([m, of(int((given < exp).sum()), n), of(int((given == exp).sum()), n), of(int((given > exp).sum()), n)])
    return table(rows, ["model", "less urgent than expected", "same level", "more urgent than expected"])


def trend(files):
    rows = []
    for name, ids in [("rising series", RISING), ("stable series", STABLE)]:
        g = files[files.report_id.isin(ids)]
        rows.append([f"sees the {name.split()[0]} values"] + [count(g[g.model == m].sees_trend) for m in MODELS])
    rising = files[files.report_id.isin(RISING)]
    rows.append(["rising series, level 1 given"] + [count(rising[rising.model == m].level_given, "1") for m in MODELS])
    rows.append(["rising series, false reassurance"] + [count(rising[rising.model == m].false_reassurance) for m in MODELS])
    return table(rows, ["older results on the report"] + MODELS)


def photos_auto(every):
    rows = []
    for m in MODELS:
        g = every[every.model == m]
        for cond in ["light", "shade", "light_wa", "shade_wa"]:
            h = g[g.condition == cond]
            rows.append([m, cond, count(h.reads_value.astype(str)), count(h.hedges_image.astype(str))])
        rows.append([m, "all photos", count(g.reads_value.astype(str)), count(g.hedges_image.astype(str))])
    return table(rows, ["model", "photo", "gives the printed PSA value", "says the image is hard to read"])


def photos_vs_files(files, photos):
    same = files[(files.prompt_id == "fr") & files.report_id.isin(photos.report_id.unique())]
    rows = []
    for name, col, value in [("wrong side of the limit", "range_comparison", "0"),
                             ("false reassurance", "false_reassurance", "1")]:
        for m in MODELS:
            rows.append([name, m, count(same[same.model == m][col], value), count(photos[photos.model == m][col], value)])
    for m in MODELS:
        s, p = same[same.model == m], photos[photos.model == m]
        rows.append(["same level as expected", m, of(int((s.level_given == s.expected_level).sum()), len(s)),
                     of(int((p.level_given == p.expected_level).sum()), len(p))])
    return table(rows, ["what", "model", "files (11 reports, French question)", "photos (same reports, 4 photos each)"])


def missing(files):
    rows = [["asks me a question (medicines, older results, symptoms)"] + [count(files[files.model == m].asks_missing) for m in MODELS]]
    for name, ids in [("finasteride note used well", FINASTERIDE), ("rectal exam note used well", RECTAL_EXAM)]:
        g = files[files.report_id.isin(ids)]
        rows.append([name] + [count(g[g.model == m].uses_note) for m in MODELS])
    for name, a, b in [("finasteride", "R002", "R019"), ("rectal exam", "R009", "R020")]:
        for report, label in [(a, "with the note"), (b, "without the note")]:
            g = files[files.report_id == report]
            rows.append([f"{name}, {label} ({report}): level 1 given"] +
                        [count(g[g.model == m].level_given, "1") for m in MODELS])
    return table(rows, ["missing information"] + MODELS)


def figures(files):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    ink, muted, grid, surface = "#0b0b0b", "#52514e", "#e4e2dc", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": grid,
                         "axes.labelcolor": muted, "xtick.color": muted, "ytick.color": ink})

    def bars(ax, groups, values, labels, title):
        y = range(len(groups))
        h = 0.36
        for i, m in enumerate(MODELS):
            pos = [k + (i - 0.5) * (h + 0.04) for k in y]
            ax.barh(pos, values[m], height=h, color=COLORS[m], label=m, edgecolor=surface, linewidth=2)
            for p, v, t in zip(pos, values[m], labels[m]):
                ax.text(v + 1.5, p, t, va="center", fontsize=9, color=muted)
        ax.set_yticks(list(y), groups)
        ax.tick_params(length=0)
        ax.invert_yaxis()
        ax.set_xlim(0, 115)
        ax.set_xticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
        ax.grid(axis="x", color=grid, linewidth=0.8)
        ax.set_axisbelow(True)
        for s in ["top", "right", "left"]:
            ax.spines[s].set_visible(False)
        ax.set_title(title, loc="left", fontsize=11, color=ink, pad=12)
        ax.legend(frameon=False, loc="lower right", fontsize=9)

    # 1. wrong side of the limit, value under or over the limit
    groups = ["value under the limit", "value over the limit"]
    values, labels = {}, {}
    for m in MODELS:
        g = files[files.model == m]
        values[m], labels[m] = [], []
        for mask in [g.below_limit, ~g.below_limit]:
            s = g[mask].range_comparison.dropna()
            k, n = int((s == "0").sum()), len(s)
            values[m].append(100 * k / n)
            labels[m].append(f"{k} of {n}")
    fig, ax = plt.subplots(figsize=(7.5, 2.8), facecolor=surface)
    ax.set_facecolor(surface)
    bars(ax, groups, values, labels, "Puts the value on the wrong side of the printed limit")
    fig.tight_layout()
    fig.savefig(OUT / "figures" / "wrong_side.png", dpi=160, facecolor=surface)
    plt.close(fig)

    # 2. level given compared with my expected level
    groups = ["less urgent than expected", "same level", "more urgent than expected"]
    values, labels = {}, {}
    for m in MODELS:
        g = files[(files.model == m) & files.level_given.notna()]
        given, exp = g.level_given.astype(int), g.expected_level.astype(int)
        ks = [int((given < exp).sum()), int((given == exp).sum()), int((given > exp).sum())]
        values[m] = [100 * k / len(g) for k in ks]
        labels[m] = [f"{k} of {len(g)}" for k in ks]
    fig, ax = plt.subplots(figsize=(7.5, 3.2), facecolor=surface)
    ax.set_facecolor(surface)
    bars(ax, groups, values, labels, "Urgency of the advice compared with my expected level")
    fig.tight_layout()
    fig.savefig(OUT / "figures" / "levels.png", dpi=160, facecolor=surface)
    plt.close(fig)


def main():
    files, photos, every = load()
    (OUT / "tables").mkdir(parents=True, exist_ok=True)

    echo_table, trap_reports = echo(files)
    parts = [
        ("Every column, answers on files", "overview", overview(files),
         "172 answers, 86 per model. A cell is left out when the column doesn't apply to the report."),
        ("H1. The value and the printed limit", "comparison", comparison(files),
         "Out of the answers where the model says on which side of the limit the value is."),
        ("H1. Value under the limit, but a doctor is needed", "echo", echo_table,
         f"Reports: {trap_reports}."),
        ("H1. The age", "age", age(files), ""),
        ("H2. Level given for each expected level", "levels", levels(files), ""),
        ("H2. Level given compared with the expected level", "level_fit", level_fit(files),
         "Only the answers that give some advice."),
        ("H3. Older results", "trend", trend(files),
         f"Rising: {', '.join(RISING)}. Stable: {', '.join(STABLE)}."),
        ("H4. Every photo answer, automatic columns", "photos_auto", photos_auto(every),
         ("344 answers per model, French and English question, filled by the same script as the sheet. "
          "The 8 MedGemma answers caught by the hard to read search all talk about the line under the PSA, "
          "\"Antigène prostatique spécifique\", as if it were a second test with a value they can't see. "
          "None of them doubts the PSA value itself.")),
        ("H4. Photos scored by hand compared with the files", "photos_vs_files", photos_vs_files(files, photos),
         "French question on the 11 pilot reports."),
        ("H5. Missing information", "missing", missing(files), ""),
    ]

    lines = ["# Results tables", "", "Written by analysis/analyze.py. Don't edit by hand, run the script again.", ""]
    for title, name, df, note in parts:
        df.to_csv(OUT / "tables" / f"{name}.csv", index=False)
        lines += [f"## {title}", ""]
        if note:
            lines += [note, ""]
        lines += [to_md(df), ""]
    lines += ["## Figures", "", "![Wrong side of the limit](figures/wrong_side.png)", "",
              "![Level given](figures/levels.png)", ""]
    (OUT / "summary.md").write_text("\n".join(lines), encoding="utf-8")

    figures(files)
    print(f"Wrote {OUT / 'summary.md'}, {len(parts)} tables and 2 figures")


if __name__ == "__main__":
    main()
