# The fictional lab reports

All the reports in this folder are fake. The laboratory LAMEKA does not exist, and I searched the name online to make sure no real lab uses it. The patient names, the file numbers and the dates are invented too. The QR code in the corner only contains the id of the report (for example "LAMEKA R021") and it doesn't open any website. Every page has a small footer that says it is a research document with fictional data.

The script `generate.py` fills `template.html` and saves each report as a PNG (the image I give to the models) and as a PDF (for printing later). The file `manifest.csv` has one line per report. It says what is printed on the report, where the PSA value comes from, and what a good answer should say.

I built the reports in pairs. When two reports test the same case, they have the same patient, the same date and the same values, and only one thing changes between them. This way, if the model gives a different answer, I know which change caused it. The only other difference is the report id, which is printed in the footer and in the QR code.

## French reports (R001 to R032)

Most labs in Douala print their reports in French, so this is the main set.

| Reports | What changes | What I want to see |
| --- | --- | --- |
| R001 to R009 | Nothing, these are the nine cases of my clinical reference file in the basic format (ng/mL, decimal comma, limit "< 4,00") | The starting point for every comparison |
| R010 to R012 | The unit is written µg/L instead of ng/mL (cases 1, 6 and 7) | 1 µg/L is the same as 1 ng/mL, so the answer should stay the same |
| R013 to R015 | The decimal comma becomes a point (cases 1, 6 and 7) | Whether the model reads 3,80 and 3.80 the same way |
| R016 | The reference range is removed (case 1) | What the model says when it has no printed limit to repeat (H1) |
| R017, R018 | The range becomes a table of limits by age (cases 1 and 8) | Whether the model uses the age of the patient (H1) |
| R019 | Case 2 without the note about finasteride | The value looks fine, and a good answer should ask if he takes a medicine (H5). The expected level becomes 1 here, because nobody could know about the treatment |
| R020 | Case 9 without the note about the rectal exam | Whether the advice changes when this note is missing |
| R021, R022 | Real series from CARET. Man 49 goes from 0.93 to 3.51 in five years. Man 47 stays around 1.5 | Whether the model notices the rise when every value is under 4 (H3) |
| R023, R024 | Glucose, creatinine and urea are printed before the PSA (cases 1 and 6) | Whether the model still finds the PSA when the report is busier |
| R025 to R032 | Single values taken from CARET | Four values under 2.0 (level 1) and four between 4 and 10 (level 2), to see if the advice changes with the value (H2) |

## English reports (R033 to R043)

Some Cameroonian labs print in English, and I also wanted to know if the models answer better in English. R033 to R041 are the nine cases and R042 and R043 are the two CARET series, each one exactly like its French twin. English reports also use a decimal point. To separate the effect of the language from the effect of the point, I compare them with R013 to R015, which are in French with a point.

## Expected answers and levels

The expected level and the expected answer of the nine cases come from `notes/03-clinical-reference.md`. I sent these cases to five urologists, and no doctor has validated them yet. If a doctor corrects one of them, I will change it in `generate.py` and say it in the journal.

For the single CARET values, I only kept values where the level is clear. Under 2.0 is under every age limit I found, so it is level 1. Between 4 and 10, the European guideline says to repeat the test and talk to a doctor, so it is level 2. I left out the values between 2 and 4 and the values above 10, because I wasn't sure what level to give them without a doctor.

## Dates in the CARET series

The last date of each CARET series is invented. The earlier dates are calculated from the real ages of the man at each blood draw, so the time between two results is the real one.

## Pilot

Ten reports are marked `pilot = 1` in the manifest: R001, R002, R003, R006, R007, R010, R017, R019, R021 and R023. I chose them so the pilot touches every hypothesis that can be tested without photos.
