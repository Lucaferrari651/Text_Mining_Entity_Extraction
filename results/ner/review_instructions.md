# Review of false positives: instructions for the two reviewers

`review_sheet.csv` has 150 sentences (50 each from Few-NERD, WNUT-17, TweetNER7). In each, the model (RoBERTa-large) marked a mention with `[[double brackets]]`
that the dataset does **not** label as a person, company or product. Decide who is right. Work alone: do not look at the other reviewer's column.

Fill `reviewer_a` (or `reviewer_b`) with one word:
- `yes`: the marked text really is a mention of the predicted type (`pred_type`: PER person, COMP company, PROD product), so the dataset missed it.
- `no`: it is not an entity of that type (wrong type, not a name, wrong boundaries, a place or organisation that is not a company, etc.).
- `unsure`: you cannot tell from the sentence.

Rules: a PER is a person's name or a person's account name; COMP is a business or brand-owning company (not a university, party, band, sports team, government, media outlet counts as `no`);
PROD is a named product or service (not a generic thing such as "phone"). Use the `note` column for anything odd. Do not edit the other columns.

Then: `python review_sheet.py score --sheet reviewed.csv --run s_all_rl --out results/ner/review_result.json`.
