# 🏢 AC Cleaning Booking System

This system manages the annual air conditioning cleaning schedule for the 43-room apartment building. It is accessed by tenants directly via our LINE Official Account.

## 🏗️ Architecture Overview

*   **Frontend:** HTML/JS hosted on GitHub Pages (wrapped in LINE LIFF).
*   **Backend / Database:** Google Sheets + Google Apps Script (GAS).
*   **Authentication Sync:** Python script (`sync_tenants.py`) that securely pulls active tenant Line IDs from the Key Box Firebase and whitelists them in the Google Sheet.

---

## 🚀 Pre-Season Runbook (For the Manager)

*Run this process exactly once before announcing the booking season to the tenants.*

1. **Open the local project folder** in VS Code.
2. **Verify Credentials:** Ensure `firebase_key.json` and `sheets_key.json` are present in the folder. *(Never upload these to GitHub!)*
3. **Run the Sync:** Open the VS Code Terminal and run:
   ```bash
   python sync_tenants.py
   ```
4. **Confirm Success:** Wait for the `Sync complete!` message in the terminal.
5. **Verify the Database:** Open the Google Sheet and verify the **Tenants** tab is populated with the latest Line IDs and Room Numbers.
6. **Reset the Schedule:** In the **Schedule** tab, clear out last year's names/Line IDs and reset all slots to "Open".

---

## 🔧 Troubleshooting Guide

### ❌ Issue: "Access Denied" on LINE app
*   **Cause:** The user's Line ID is not in the Key Box database, or the Python sync script wasn't run after they moved in.
*   **Fix:** Add them to the Key Box system, then manually paste their Line ID into the Google Sheet **Tenants** tab and set their status to "Active".

### ⏳ Issue: App freezes on "Loading available slots..."
*   **Cause:** The Google Apps Script deployment URL changed, or the LINE LIFF SDK is failing to initialize. 
*   **Fix:** Check the `SCRIPT_URL` variable in `index.html`. If you recently modified the Google Sheet code, ensure you clicked **New Deployment** (not just save) and updated the URL in the HTML.
