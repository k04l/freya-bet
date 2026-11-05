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

  var published = form.getPublishedUrl();
  var formId = published.match(/\/d\/e\/([^/]+)\//)[1];

  var keys = ['name','email','breed1','pct1','breed2','pct2','breed3','pct3','pledge','comment'];
  Logger.log('=== Paste into index.html CONFIG ===');
  Logger.log('formId: "' + formId + '"');
  Logger.log('form edit URL: ' + form.getEditUrl());
  Logger.log('form public URL: ' + published);
  for (var i = 0; i < q.length; i++) {
    Logger.log(keys[i] + ': "entry.' + q[i].getId() + '"');
  }

  var ss = SpreadsheetApp.create('Freya DNA Bet — Responses');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  Logger.log('Responses Sheet: ' + ss.getUrl());
  Logger.log('Next: Sheet → File → Share → Publish to web → CSV → paste URL into CONFIG.sheetCsvUrl');

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
