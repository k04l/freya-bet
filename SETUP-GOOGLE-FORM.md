# Google Form setup for Who’s Freya?

Two options. **A** is click-through (~3 min). **B** is a paste-and-run Apps Script that builds the form and prints the IDs for you.

---

## Option A — Manual (≈3 minutes)

### 1. Create the form
1. Open [forms.google.com](https://forms.google.com) (personal Gmail).
2. **Blank form** → title: **Freya DNA Bet**
3. Add these questions (all **Short answer**):

| # | Question title (exact) | Required? |
|---|------------------------|-----------|
| 1 | Name | Yes |
| 2 | Email | No |
| 3 | Breed 1 | Yes |
| 4 | Pct 1 | Yes |
| 5 | Breed 2 | Yes |
| 6 | Pct 2 | Yes |
| 7 | Breed 3 | Yes |
| 8 | Pct 3 | Yes |
| 9 | Pledge USD | Yes |
| 10 | Comment | No |

### 2. Get `formId` + `entry.XXXX` IDs
1. Form → **⋮** (top right) → **Get pre-filled link**
2. Type dummy values in every field → **Get link** → **Copy link**
3. The URL looks like:

```
https://docs.google.com/forms/d/e/FORM_ID_HERE/viewform?usp=pp_url&entry.111111=Alex&entry.222222=a@b.com&entry.333333=Husky&entry.444444=40&...
```

- `FORM_ID_HERE` (between `/e/` and `/viewform`) → `CONFIG.formId`
- Each `entry.########` maps to the field you filled, in order of the questions above

### 3. Paste into `index.html`
Find this block near the bottom of `index.html` and fill it in:

```js
const CONFIG = {
  formId: "PASTE_FORM_ID_HERE",
  entries: {
    name: "entry.1111111111",
    email: "entry.2222222222",
    breed1: "entry.3333333333",
    pct1: "entry.4444444444",
    breed2: "entry.5555555555",
    pct2: "entry.6666666666",
    breed3: "entry.7777777777",
    pct3: "entry.8888888888",
    pledge: "entry.9999999999",
    comment: "entry.0000000000"
  },
  sheetCsvUrl: ""
};
```

Commit / push (or re-upload) so the live site picks it up. The orange “Form backend isn’t wired” banner disappears once `formId` + `entries.name` + `entries.breed1` are set.

### 4. Responses Sheet + live leaderboard (optional)
1. Form → **Responses** → green Sheets icon → **Create a new spreadsheet** (name it **Freya DNA Bet — Responses**).
2. In that Sheet: **File → Share → Publish to web**
3. Pick the responses sheet tab → format **Comma-separated values (.csv)** → **Publish**
4. Copy the CSV URL into `CONFIG.sheetCsvUrl`
5. Push again. The “Bets so far” section will load from that CSV.

### 5. Test
1. Open the live page → submit a test bet with your name
2. Confirm a new row appears in the Responses Sheet
3. Confirm the toast says the guess is locked in (banner gone)

---

## Option B — Apps Script (auto-create)

1. Open [script.google.com](https://script.google.com) → **New project**
2. Paste the contents of [`create-form.gs`](./create-form.gs) (also copied below)
3. Save → Run **`createFreyaForm`** → authorize with your personal Google account
4. Open **View → Logs** (or Execution log). Copy:
   - `formId`
   - each `entry.…` line  
   into the `CONFIG` block above
5. The script also creates / links a Responses spreadsheet. Publish that sheet as CSV (step 4 in Option A) if you want the live board.

### Full script (`create-form.gs`)

```javascript
/**
 * Creates "Freya DNA Bet" Google Form + linked Responses sheet.
 * Run createFreyaForm(), then copy formId + entry IDs from the logs into index.html CONFIG.
 */
function createFreyaForm() {
  var form = FormApp.create('Freya DNA Bet');
  form.setDescription(
    "Guess Freya's top 3 breeds with percentages. Closest guess wins — pot goes to charity."
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setLimitOneResponsePerUser(false);

  var q = [];
  q.push(form.addTextItem().setTitle('Name').setRequired(true));
  q.push(form.addTextItem().setTitle('Email').setRequired(false));
  q.push(form.addTextItem().setTitle('Breed 1').setRequired(true));
  q.push(form.addTextItem().setTitle('Pct 1').setRequired(true));
  q.push(form.addTextItem().setTitle('Breed 2').setRequired(true));
  q.push(form.addTextItem().setTitle('Pct 2').setRequired(true));
  q.push(form.addTextItem().setTitle('Breed 3').setRequired(true));
  q.push(form.addTextItem().setTitle('Pct 3').setRequired(true));
  q.push(form.addTextItem().setTitle('Pledge USD').setRequired(true));
  q.push(form.addTextItem().setTitle('Comment').setRequired(false));

  // Published form ID used in /forms/d/e/FORM_ID/formResponse
  var published = form.getPublishedUrl(); // .../d/e/FORM_ID/viewform
  var formId = published.match(/\/d\/e\/([^/]+)\//)[1];

  var keys = ['name','email','breed1','pct1','breed2','pct2','breed3','pct3','pledge','comment'];
  Logger.log('=== Paste into index.html CONFIG ===');
  Logger.log('formId: "' + formId + '"');
  Logger.log('form edit URL: ' + form.getEditUrl());
  Logger.log('form public URL: ' + published);
  for (var i = 0; i < q.length; i++) {
    Logger.log(keys[i] + ': "entry.' + q[i].getId() + '"');
  }

  // Linked responses sheet
  var ss = SpreadsheetApp.create('Freya DNA Bet — Responses');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  Logger.log('Responses Sheet: ' + ss.getUrl());
  Logger.log('Next: Sheet → File → Share → Publish to web → CSV → paste URL into CONFIG.sheetCsvUrl');

  // Also dump a ready-to-paste CONFIG snippet
  var lines = [];
  lines.push('const CONFIG = {');
  lines.push('  formId: "' + formId + '",');
  lines.push('  entries: {');
  for (var j = 0; j < q.length; j++) {
    var comma = j < q.length - 1 ? ',' : '';
    lines.push('    ' + keys[j] + ': "entry.' + q[j].getId() + '"' + comma);
  }
  lines.push('  },');
  lines.push('  sheetCsvUrl: ""');
  lines.push('};');
  Logger.log(lines.join('\n'));
}
```

---

## Reminder
- Bets POST to `https://docs.google.com/forms/d/e/{formId}/formResponse` (the page already does this).
- Pledges are paid via Venmo/PayPal on the page; the form only **tracks** amounts.
- After wiring CONFIG, hard-refresh the live site.
