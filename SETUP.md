# Freya DNA Bet — setup (≈2 minutes)

The landing page is ready. Google Drive's connector couldn't *create* a Form/Sheet (read scopes only), so do this once in your browser.

## 1. Create the Google Form

1. Open [forms.google.com](https://forms.google.com) while signed into your personal Gmail.
2. Blank form → title: **Freya DNA Bet**
3. Add these questions (short answer unless noted):

| # | Question title (exact) | Type | Required |
|---|------------------------|------|----------|
| 1 | Name | Short answer | Yes |
| 2 | Email | Short answer | No |
| 3 | Breed 1 | Short answer | Yes |
| 4 | Pct 1 | Short answer | Yes |
| 5 | Breed 2 | Short answer | Yes |
| 6 | Pct 2 | Short answer | Yes |
| 7 | Breed 3 | Short answer | Yes |
| 8 | Pct 3 | Short answer | Yes |
| 9 | Pledge USD | Short answer | Yes |
| 10 | Comment | Short answer | No |

4. **Responses** tab → Link to Sheets → create **Freya DNA Bet — Responses**.
5. (Optional live board) In that Sheet: **File → Share → Publish to web** → choose the responses sheet → **CSV** → Publish. Copy the CSV URL.

## 2. Wire the landing page

1. Open the Form → ⋮ → **Get pre-filled link** → fill dummy values → Get link.
2. The URL looks like:
   `https://docs.google.com/forms/d/e/FORM_ID/viewform?usp=pp_url&entry.111111=...&entry.222222=...`
3. Edit `/workspace/freya-bet/index.html` (or the hosted copy) — find the `CONFIG` block near the bottom:

```js
const CONFIG = {
  formId: "PASTE_FORM_ID_HERE",
  entries: {
    name: "entry.111111",
    email: "entry.222222",
    breed1: "entry.333333",
    pct1: "entry.444444",
    breed2: "entry.555555",
    pct2: "entry.666666",
    breed3: "entry.777777",
    pct3: "entry.888888",
    pledge: "entry.999999",
    comment: "entry.000000"
  },
  sheetCsvUrl: "PASTE_PUBLISHED_CSV_URL_OR_LEAVE_BLANK"
};
```

4. Redeploy / push the updated file.

## 3. Hosting

If GitHub Pages is live: `https://k04l.github.io/freya-bet/`  
Otherwise any static host works (Netlify drop, Cloudflare Pages, Drive public HTML, etc.).

## 4. QR code

Regenerate after you have the final URL:

```bash
/workspace/freya-bet/.venv/bin/python /workspace/freya-bet/make_qr.py "https://YOUR-URL/"
```

## Scoring reminder

Score = sum over matching breeds of `min(guessed%, DNA%)`. Highest wins. Pot → Charity TBD (collected after results).
