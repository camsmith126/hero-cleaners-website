/**
 * Hero Cleaners — Commercial Payroll Tracker
 *
 * Run setupSheet() once to build all three tabs with formatting,
 * data validation, conditional formatting, and the Monday 8am trigger.
 *
 * Workflow:
 *   - Job Log (Tab 3): source data — all jobs, all weeks
 *   - Fix These (Tab 1): Laura's daily view — only flagged jobs (30+ min over/under)
 *   - Weekly Report (Tab 2): Jaylee + Cam's Monday 3:30pm review
 *
 * After setup, use the "Hero Cleaners" menu to manually refresh any tab.
 */

// ─── CONFIG ──────────────────────────────────────────────────────────
var LABOR_RATE = 15; // $/hr for labor cost calculations — update as needed

var COLORS = {
  heroRed:    "#B71C1C",
  accentRed:  "#D32F2F",
  black:      "#1A1A1A",
  charcoal:   "#2D2D2D",
  white:      "#FFFFFF",
  offWhite:   "#F9F6F4",
  lightRose:  "#FFCDD2",
  border:     "#E8E0DD",
  green:      "#2E7D32",
  greenLight: "#E8F5E9",
  greenBg:    "#C8E6C9",
  yellow:     "#F57F17",
  yellowLight:"#FFF9C4",
  yellowBg:   "#FFF176",
  red:        "#C62828",
  redLight:   "#FFEBEE",
  redBg:      "#FFCDD2",
  gray:       "#757575",
  grayLight:  "#F5F5F5",
  grayBg:     "#E0E0E0"
};

// ─── MENU ────────────────────────────────────────────────────────────
function onOpen() {
  SpreadsheetApp.getUi().createMenu("Hero Cleaners")
    .addItem("Refresh Fix These", "refreshFixThese")
    .addItem("Refresh Weekly Report", "refreshWeeklyReport")
    .addSeparator()
    .addItem("Run Full Setup (first time only)", "setupSheet")
    .addToUi();
}

// ─── FULL SETUP ──────────────────────────────────────────────────────
function setupSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  // Delete default Sheet1 if it exists and we're starting fresh
  var defaultSheet = ss.getSheetByName("Sheet1");

  // Create tabs in reverse order so they appear in correct order
  var jobLog = ss.getSheetByName("📋 Job Log") || ss.insertSheet("📋 Job Log");
  var weeklyReport = ss.getSheetByName("📊 Weekly Report") || ss.insertSheet("📊 Weekly Report", 0);
  var fixThese = ss.getSheetByName("🚩 Fix These") || ss.insertSheet("🚩 Fix These", 0);

  if (defaultSheet) {
    try { ss.deleteSheet(defaultSheet); } catch(e) {}
  }

  setupJobLog_(jobLog);
  setupFixThese_(fixThese);
  setupWeeklyReport_(weeklyReport);
  setupTrigger_();

  // Activate Laura's tab as default view
  ss.setActiveSheet(fixThese);

  SpreadsheetApp.getUi().alert(
    "Setup complete!\n\n" +
    "1. Enter job data in 📋 Job Log\n" +
    "2. Laura checks 🚩 Fix These daily\n" +
    "3. 📊 Weekly Report refreshes every Monday at 8am\n\n" +
    "Use the Hero Cleaners menu to manually refresh anytime."
  );
}

// ─── TAB 1: FIX THESE ───────────────────────────────────────────────
function setupFixThese_(sheet) {
  sheet.clear();
  sheet.setTabColor(COLORS.accentRed);

  // Column widths
  sheet.setColumnWidth(1, 110); // Date
  sheet.setColumnWidth(2, 200); // Customer Name
  sheet.setColumnWidth(3, 150); // Cleaner
  sheet.setColumnWidth(4, 130); // Scheduled Time
  sheet.setColumnWidth(5, 130); // Actual Time
  sheet.setColumnWidth(6, 120); // Difference
  sheet.setColumnWidth(7, 180); // Status

  // Title row
  sheet.setRowHeight(1, 50);
  var titleRange = sheet.getRange("A1:G1");
  titleRange.merge()
    .setValue("🚩  Jobs That Need Attention")
    .setFontFamily("Arial")
    .setFontSize(16)
    .setFontWeight("bold")
    .setFontColor(COLORS.white)
    .setBackground(COLORS.heroRed)
    .setVerticalAlignment("middle")
    .setHorizontalAlignment("left");
  sheet.getRange("A1").setNumberFormat("@"); // force text

  // Subtitle row
  sheet.setRowHeight(2, 30);
  var subtitleRange = sheet.getRange("A2:G2");
  subtitleRange.merge()
    .setValue("Jobs from this week where actual time was 30+ minutes over or under scheduled. Laura — update Status when resolved.")
    .setFontFamily("Arial")
    .setFontSize(9)
    .setFontColor(COLORS.gray)
    .setBackground(COLORS.offWhite)
    .setVerticalAlignment("middle");

  // Headers
  var headers = ["Date", "Customer Name", "Cleaner", "Scheduled Time", "Actual Time", "Difference", "Status"];
  sheet.setRowHeight(3, 36);
  var headerRange = sheet.getRange(3, 1, 1, 7);
  headerRange.setValues([headers])
    .setFontFamily("Arial")
    .setFontSize(10)
    .setFontWeight("bold")
    .setFontColor(COLORS.white)
    .setBackground(COLORS.charcoal)
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle");

  // "All clear" placeholder
  sheet.setRowHeight(4, 60);
  var placeholder = sheet.getRange("A4:G4");
  placeholder.merge()
    .setValue("✅ All clear this week")
    .setFontFamily("Arial")
    .setFontSize(14)
    .setFontColor(COLORS.green)
    .setBackground(COLORS.greenLight)
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle");

  // Freeze header rows
  sheet.setFrozenRows(3);

  // Protect title/header rows
  var protection = sheet.getRange("A1:G3").protect();
  protection.setDescription("Headers — do not edit");
  protection.setWarningOnly(true);
}

function refreshFixThese() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var fixSheet = ss.getSheetByName("🚩 Fix These");
  var logSheet = ss.getSheetByName("📋 Job Log");

  if (!fixSheet || !logSheet) {
    SpreadsheetApp.getUi().alert("Run setup first.");
    return;
  }

  // Get existing statuses before clearing (preserve Laura's work)
  var existingStatuses = {};
  if (fixSheet.getLastRow() > 3) {
    var oldData = fixSheet.getRange(4, 1, fixSheet.getLastRow() - 3, 7).getValues();
    for (var i = 0; i < oldData.length; i++) {
      if (oldData[i][0] && oldData[i][1]) {
        var key = oldData[i][0].toString() + "|" + oldData[i][1] + "|" + oldData[i][2];
        existingStatuses[key] = oldData[i][6];
      }
    }
  }

  // Clear data rows
  if (fixSheet.getLastRow() > 3) {
    fixSheet.getRange(4, 1, fixSheet.getLastRow() - 3, 7).clear();
    // Unmerge any merged cells in data area
    fixSheet.getRange(4, 1, fixSheet.getLastRow(), 7).breakApart();
  }

  // Get current week boundaries (Monday to Sunday)
  var now = new Date();
  var dayOfWeek = now.getDay();
  var monday = new Date(now);
  monday.setDate(now.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1));
  monday.setHours(0, 0, 0, 0);
  var sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  sunday.setHours(23, 59, 59, 999);

  // Read job log
  var logLastRow = logSheet.getLastRow();
  if (logLastRow < 2) {
    showAllClear_(fixSheet);
    return;
  }

  var logData = logSheet.getRange(2, 1, logLastRow - 1, 8).getValues();
  var flagged = [];

  for (var i = 0; i < logData.length; i++) {
    var jobDate = new Date(logData[i][0]);
    if (jobDate < monday || jobDate > sunday) continue;

    var scheduled = logData[i][4]; // Scheduled Hours (col E)
    var actual = logData[i][5];    // Actual Hours (col F)
    if (!scheduled || !actual) continue;

    var diffMinutes = (actual - scheduled) * 60;
    if (Math.abs(diffMinutes) < 30) continue;

    var key = jobDate.toString() + "|" + logData[i][1] + "|" + logData[i][2];
    var status = existingStatuses[key] || "Needs Review";

    flagged.push([
      jobDate,
      logData[i][1], // Customer
      logData[i][2], // Cleaner
      scheduled,
      actual,
      diffMinutes,
      status
    ]);
  }

  // Sort by most recent date first
  flagged.sort(function(a, b) { return b[0] - a[0]; });

  if (flagged.length === 0) {
    showAllClear_(fixSheet);
    return;
  }

  // Write flagged rows
  var dataRange = fixSheet.getRange(4, 1, flagged.length, 7);
  dataRange.setValues(flagged);

  // Format data rows
  dataRange.setFontFamily("Arial").setFontSize(10).setVerticalAlignment("middle");
  fixSheet.getRange(4, 1, flagged.length, 1).setNumberFormat("M/d/yyyy"); // Date
  fixSheet.getRange(4, 4, flagged.length, 2).setNumberFormat("0.0\" hrs\""); // Scheduled/Actual
  fixSheet.getRange(4, 6, flagged.length, 1).setNumberFormat("+0\" min\";-0\" min\""); // Difference

  // Alternating row colors
  for (var r = 0; r < flagged.length; r++) {
    var rowRange = fixSheet.getRange(4 + r, 1, 1, 7);
    rowRange.setBackground(r % 2 === 0 ? COLORS.white : COLORS.offWhite);
    fixSheet.setRowHeight(4 + r, 32);
  }

  // Difference column color coding
  for (var r = 0; r < flagged.length; r++) {
    var diffCell = fixSheet.getRange(4 + r, 6);
    var diff = flagged[r][5];
    if (diff > 0) {
      diffCell.setFontColor(COLORS.red).setFontWeight("bold");
    } else {
      diffCell.setFontColor(COLORS.yellow).setFontWeight("bold");
    }
  }

  // Status dropdown validation
  var statusRange = fixSheet.getRange(4, 7, flagged.length, 1);
  var rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(["Needs Review", "Fixed in HCP", "Checked — No Issue"])
    .setAllowInvalid(false)
    .build();
  statusRange.setDataValidation(rule);

  // Status color coding
  applyStatusFormatting_(fixSheet, flagged.length);
}

function showAllClear_(sheet) {
  sheet.setRowHeight(4, 60);
  var placeholder = sheet.getRange("A4:G4");
  placeholder.merge()
    .setValue("✅ All clear this week")
    .setFontFamily("Arial")
    .setFontSize(14)
    .setFontColor(COLORS.green)
    .setBackground(COLORS.greenLight)
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle");
}

function applyStatusFormatting_(sheet, numRows) {
  var statusRange = sheet.getRange(4, 7, numRows, 1);

  // Clear existing conditional formatting rules for this range
  var rules = sheet.getConditionalFormatRules();
  var newRules = [];
  for (var i = 0; i < rules.length; i++) {
    var ranges = rules[i].getRanges();
    var keep = true;
    for (var j = 0; j < ranges.length; j++) {
      if (ranges[j].getColumn() === 7 && ranges[j].getRow() >= 4) {
        keep = false;
        break;
      }
    }
    if (keep) newRules.push(rules[i]);
  }

  // Add status rules
  newRules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo("Needs Review")
    .setBackground(COLORS.redBg)
    .setFontColor(COLORS.red)
    .setBold(true)
    .setRanges([statusRange])
    .build());

  newRules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo("Fixed in HCP")
    .setBackground(COLORS.greenBg)
    .setFontColor(COLORS.green)
    .setBold(true)
    .setRanges([statusRange])
    .build());

  newRules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo("Checked — No Issue")
    .setBackground(COLORS.grayBg)
    .setFontColor(COLORS.gray)
    .setBold(true)
    .setRanges([statusRange])
    .build());

  sheet.setConditionalFormatRules(newRules);
}

// ─── TAB 2: WEEKLY REPORT ────────────────────────────────────────────
function setupWeeklyReport_(sheet) {
  sheet.clear();
  sheet.setTabColor(COLORS.charcoal);

  // Column widths
  sheet.setColumnWidth(1, 110); // Date
  sheet.setColumnWidth(2, 200); // Customer
  sheet.setColumnWidth(3, 150); // Cleaner
  sheet.setColumnWidth(4, 120); // Revenue
  sheet.setColumnWidth(5, 130); // Scheduled Hours
  sheet.setColumnWidth(6, 130); // Actual Hours
  sheet.setColumnWidth(7, 110); // Labor %
  sheet.setColumnWidth(8, 120); // Status

  // Title
  sheet.setRowHeight(1, 50);
  sheet.getRange("A1:H1").merge()
    .setValue("📊  Weekly Commercial Report")
    .setFontFamily("Arial")
    .setFontSize(16)
    .setFontWeight("bold")
    .setFontColor(COLORS.white)
    .setBackground(COLORS.black)
    .setVerticalAlignment("middle");

  // Summary section label
  sheet.setRowHeight(2, 8);
  sheet.getRange("A2:H2").merge().setBackground(COLORS.heroRed);

  // Summary boxes row
  sheet.setRowHeight(3, 20);
  sheet.getRange("A3:B3").merge().setValue("Total Revenue")
    .setFontFamily("Arial").setFontSize(9).setFontColor(COLORS.gray)
    .setBackground(COLORS.offWhite).setHorizontalAlignment("center");
  sheet.getRange("C3:D3").merge().setValue("Total Labor Cost")
    .setFontFamily("Arial").setFontSize(9).setFontColor(COLORS.gray)
    .setBackground(COLORS.offWhite).setHorizontalAlignment("center");
  sheet.getRange("E3:F3").merge().setValue("Overall Labor %")
    .setFontFamily("Arial").setFontSize(9).setFontColor(COLORS.gray)
    .setBackground(COLORS.offWhite).setHorizontalAlignment("center");
  sheet.getRange("G3:H3").merge().setValue("Reconciliation")
    .setFontFamily("Arial").setFontSize(9).setFontColor(COLORS.gray)
    .setBackground(COLORS.offWhite).setHorizontalAlignment("center");

  // Summary values row
  sheet.setRowHeight(4, 44);
  var summaryStyle = {font: "Arial", size: 18, weight: "bold", bg: COLORS.offWhite, align: "center", valign: "middle"};

  sheet.getRange("A4:B4").merge().setValue("—")
    .setFontFamily("Arial").setFontSize(18).setFontWeight("bold")
    .setBackground(COLORS.offWhite).setHorizontalAlignment("center").setVerticalAlignment("middle");
  sheet.getRange("C4:D4").merge().setValue("—")
    .setFontFamily("Arial").setFontSize(18).setFontWeight("bold")
    .setBackground(COLORS.offWhite).setHorizontalAlignment("center").setVerticalAlignment("middle");
  sheet.getRange("E4:F4").merge().setValue("—")
    .setFontFamily("Arial").setFontSize(18).setFontWeight("bold")
    .setBackground(COLORS.offWhite).setHorizontalAlignment("center").setVerticalAlignment("middle");
  sheet.getRange("G4:H4").merge().setValue("—")
    .setFontFamily("Arial").setFontSize(18).setFontWeight("bold")
    .setBackground(COLORS.offWhite).setHorizontalAlignment("center").setVerticalAlignment("middle");

  // Spacer
  sheet.setRowHeight(5, 8);
  sheet.getRange("A5:H5").merge().setBackground(COLORS.heroRed);

  // Column headers
  var headers = ["Date", "Customer", "Cleaner", "Revenue", "Scheduled Hrs", "Actual Hrs", "Labor %", "Status"];
  sheet.setRowHeight(6, 36);
  sheet.getRange(6, 1, 1, 8).setValues([headers])
    .setFontFamily("Arial")
    .setFontSize(10)
    .setFontWeight("bold")
    .setFontColor(COLORS.white)
    .setBackground(COLORS.charcoal)
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle");

  // Placeholder
  sheet.setRowHeight(7, 60);
  sheet.getRange("A7:H7").merge()
    .setValue("Report generates every Monday at 8am — or refresh manually from the Hero Cleaners menu")
    .setFontFamily("Arial")
    .setFontSize(11)
    .setFontColor(COLORS.gray)
    .setBackground(COLORS.grayLight)
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle");

  sheet.setFrozenRows(6);
}

function refreshWeeklyReport() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var reportSheet = ss.getSheetByName("📊 Weekly Report");
  var logSheet = ss.getSheetByName("📋 Job Log");
  var fixSheet = ss.getSheetByName("🚩 Fix These");

  if (!reportSheet || !logSheet) {
    SpreadsheetApp.getUi().alert("Run setup first.");
    return;
  }

  // Clear data rows (keep header structure rows 1-6)
  if (reportSheet.getLastRow() > 6) {
    reportSheet.getRange(7, 1, reportSheet.getLastRow() - 6, 8).clear();
    reportSheet.getRange(7, 1, reportSheet.getLastRow() - 6, 8).breakApart();
  }

  // Get prior week boundaries (Monday to Sunday before current week)
  var now = new Date();
  var dayOfWeek = now.getDay();
  var thisMonday = new Date(now);
  thisMonday.setDate(now.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1));
  thisMonday.setHours(0, 0, 0, 0);
  var lastMonday = new Date(thisMonday);
  lastMonday.setDate(thisMonday.getDate() - 7);
  var lastSunday = new Date(thisMonday);
  lastSunday.setDate(thisMonday.getDate() - 1);
  lastSunday.setHours(23, 59, 59, 999);

  // Read job log
  var logLastRow = logSheet.getLastRow();
  if (logLastRow < 2) {
    reportSheet.getRange("A7:H7").merge()
      .setValue("No data for last week")
      .setFontFamily("Arial").setFontSize(11).setFontColor(COLORS.gray)
      .setBackground(COLORS.grayLight).setHorizontalAlignment("center").setVerticalAlignment("middle");
    resetSummaryBoxes_(reportSheet);
    return;
  }

  var logData = logSheet.getRange(2, 1, logLastRow - 1, 8).getValues();
  var weekJobs = [];
  var totalRevenue = 0;
  var totalActualHours = 0;

  for (var i = 0; i < logData.length; i++) {
    var jobDate = new Date(logData[i][0]);
    if (jobDate < lastMonday || jobDate > lastSunday) continue;

    var revenue = logData[i][3] || 0;
    var scheduled = logData[i][4] || 0;
    var actual = logData[i][5] || 0;
    var laborCost = actual * LABOR_RATE;
    var laborPct = revenue > 0 ? (laborCost / revenue) * 100 : 0;

    var status;
    if (laborPct <= 35) status = "🟢 Healthy";
    else if (laborPct <= 50) status = "🟡 Watch";
    else status = "🔴 Over";

    totalRevenue += revenue;
    totalActualHours += actual;

    weekJobs.push([
      jobDate,
      logData[i][1],
      logData[i][2],
      revenue,
      scheduled,
      actual,
      laborPct / 100,
      status
    ]);
  }

  // Sort by date descending
  weekJobs.sort(function(a, b) { return b[0] - a[0]; });

  // Update summary boxes
  var totalLaborCost = totalActualHours * LABOR_RATE;
  var overallLaborPct = totalRevenue > 0 ? (totalLaborCost / totalRevenue) : 0;

  reportSheet.getRange("A4:B4").merge().setValue("$" + totalRevenue.toFixed(0))
    .setFontFamily("Arial").setFontSize(18).setFontWeight("bold")
    .setFontColor(COLORS.green).setBackground(COLORS.offWhite)
    .setHorizontalAlignment("center").setVerticalAlignment("middle");

  reportSheet.getRange("C4:D4").merge().setValue("$" + totalLaborCost.toFixed(0))
    .setFontFamily("Arial").setFontSize(18).setFontWeight("bold")
    .setFontColor(COLORS.charcoal).setBackground(COLORS.offWhite)
    .setHorizontalAlignment("center").setVerticalAlignment("middle");

  var laborPctColor = overallLaborPct <= 0.35 ? COLORS.green : overallLaborPct <= 0.50 ? COLORS.yellow : COLORS.red;
  reportSheet.getRange("E4:F4").merge().setValue((overallLaborPct * 100).toFixed(1) + "%")
    .setFontFamily("Arial").setFontSize(18).setFontWeight("bold")
    .setFontColor(laborPctColor).setBackground(COLORS.offWhite)
    .setHorizontalAlignment("center").setVerticalAlignment("middle");

  // Reconciliation status — check Fix These tab
  var reconStatus = "✅ All Clear";
  var reconColor = COLORS.green;
  if (fixSheet && fixSheet.getLastRow() > 3) {
    var statuses = fixSheet.getRange(4, 7, fixSheet.getLastRow() - 3, 1).getValues();
    var pending = false;
    for (var i = 0; i < statuses.length; i++) {
      if (statuses[i][0] === "Needs Review") { pending = true; break; }
    }
    if (pending) {
      reconStatus = "⚠️ Items Pending";
      reconColor = COLORS.yellow;
    }
  }
  reportSheet.getRange("G4:H4").merge().setValue(reconStatus)
    .setFontFamily("Arial").setFontSize(14).setFontWeight("bold")
    .setFontColor(reconColor).setBackground(COLORS.offWhite)
    .setHorizontalAlignment("center").setVerticalAlignment("middle");

  if (weekJobs.length === 0) {
    reportSheet.getRange("A7:H7").merge()
      .setValue("No commercial jobs last week")
      .setFontFamily("Arial").setFontSize(11).setFontColor(COLORS.gray)
      .setBackground(COLORS.grayLight).setHorizontalAlignment("center").setVerticalAlignment("middle");
    return;
  }

  // Write job rows
  var dataRange = reportSheet.getRange(7, 1, weekJobs.length, 8);
  dataRange.setValues(weekJobs);
  dataRange.setFontFamily("Arial").setFontSize(10).setVerticalAlignment("middle");

  // Formatting
  reportSheet.getRange(7, 1, weekJobs.length, 1).setNumberFormat("M/d/yyyy");
  reportSheet.getRange(7, 4, weekJobs.length, 1).setNumberFormat("$#,##0.00");
  reportSheet.getRange(7, 5, weekJobs.length, 2).setNumberFormat("0.0\" hrs\"");
  reportSheet.getRange(7, 7, weekJobs.length, 1).setNumberFormat("0.0%");
  reportSheet.getRange(7, 8, weekJobs.length, 1).setHorizontalAlignment("center");

  // Alternating rows + status colors
  for (var r = 0; r < weekJobs.length; r++) {
    var rowRange = reportSheet.getRange(7 + r, 1, 1, 8);
    rowRange.setBackground(r % 2 === 0 ? COLORS.white : COLORS.offWhite);
    reportSheet.setRowHeight(7 + r, 32);

    var statusCell = reportSheet.getRange(7 + r, 8);
    var laborVal = weekJobs[r][6];
    if (laborVal <= 0.35) {
      statusCell.setFontColor(COLORS.green);
    } else if (laborVal <= 0.50) {
      statusCell.setFontColor(COLORS.yellow);
    } else {
      statusCell.setFontColor(COLORS.red).setFontWeight("bold");
    }
  }

  // Week label in subtitle
  var weekLabel = Utilities.formatDate(lastMonday, "America/Denver", "MMM d") +
    " – " + Utilities.formatDate(lastSunday, "America/Denver", "MMM d, yyyy");
  reportSheet.getRange("A1:H1").merge()
    .setValue("📊  Weekly Commercial Report — " + weekLabel)
    .setFontFamily("Arial").setFontSize(16).setFontWeight("bold")
    .setFontColor(COLORS.white).setBackground(COLORS.black).setVerticalAlignment("middle");
}

function resetSummaryBoxes_(sheet) {
  var cells = [["A4:B4"], ["C4:D4"], ["E4:F4"], ["G4:H4"]];
  for (var i = 0; i < cells.length; i++) {
    sheet.getRange(cells[i][0]).merge().setValue("—")
      .setFontFamily("Arial").setFontSize(18).setFontWeight("bold")
      .setFontColor(COLORS.charcoal).setBackground(COLORS.offWhite)
      .setHorizontalAlignment("center").setVerticalAlignment("middle");
  }
}

// ─── TAB 3: JOB LOG ─────────────────────────────────────────────────
function setupJobLog_(sheet) {
  sheet.clear();
  sheet.setTabColor(COLORS.gray);

  // Column widths
  sheet.setColumnWidth(1, 110); // Date
  sheet.setColumnWidth(2, 200); // Customer Name
  sheet.setColumnWidth(3, 150); // Cleaner
  sheet.setColumnWidth(4, 120); // Revenue
  sheet.setColumnWidth(5, 130); // Scheduled Hours
  sheet.setColumnWidth(6, 130); // Actual Hours
  sheet.setColumnWidth(7, 120); // Labor Cost
  sheet.setColumnWidth(8, 200); // Notes

  // Title
  sheet.setRowHeight(1, 40);
  sheet.getRange("A1:H1").merge()
    .setValue("📋  Commercial Job Log — All Historical Data")
    .setFontFamily("Arial")
    .setFontSize(14)
    .setFontWeight("bold")
    .setFontColor(COLORS.white)
    .setBackground(COLORS.gray)
    .setVerticalAlignment("middle");

  // Headers
  var headers = ["Date", "Customer Name", "Cleaner", "Revenue", "Scheduled Hours", "Actual Hours", "Labor Cost", "Notes"];
  sheet.setRowHeight(2, 34);
  sheet.getRange(2, 1, 1, 8).setValues([headers])
    .setFontFamily("Arial")
    .setFontSize(10)
    .setFontWeight("bold")
    .setFontColor(COLORS.white)
    .setBackground(COLORS.charcoal)
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle");

  sheet.setFrozenRows(2);

  // Format columns for data entry
  sheet.getRange("A3:A1000").setNumberFormat("M/d/yyyy");
  sheet.getRange("D3:D1000").setNumberFormat("$#,##0.00");
  sheet.getRange("E3:F1000").setNumberFormat("0.00");
  sheet.getRange("G3:G1000").setNumberFormat("$#,##0.00");

  // Labor Cost auto-calc hint in first data row
  sheet.getRange("G3").setFormula("=IF(F3=\"\",\"\",F3*" + LABOR_RATE + ")");
  sheet.getRange("G3").setFontColor(COLORS.gray);

  // Copy labor cost formula down
  for (var r = 4; r <= 100; r++) {
    sheet.getRange("G" + r).setFormula("=IF(F" + r + "=\"\",\"\",F" + r + "*" + LABOR_RATE + ")");
  }

  // Light gridlines for data area
  sheet.getRange("A3:H100").setBorder(null, null, null, null, true, true, COLORS.border, SpreadsheetApp.BorderStyle.SOLID);
}

// ─── TRIGGER ─────────────────────────────────────────────────────────
function setupTrigger_() {
  // Remove existing triggers for this function
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === "mondayMorningRefresh") {
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }

  // Monday at 8am Mountain Time
  ScriptApp.newTrigger("mondayMorningRefresh")
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(8)
    .nearMinute(0)
    .create();
}

function mondayMorningRefresh() {
  refreshFixThese();
  refreshWeeklyReport();
}
