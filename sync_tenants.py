import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import gspread
from google.oauth2.service_account import Credentials

# --- 1. FIREBASE SETUP (READ-ONLY) ---
firebase_cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(firebase_cred, {
    'databaseURL': 'https://keybox-system-default-rtdb.asia-southeast1.firebasedatabase.app'
})

# --- 2. GOOGLE SHEETS SETUP (WRITE) ---
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
sheets_cred = Credentials.from_service_account_file(
    'sheets_key.json', scopes=scopes)
client = gspread.authorize(sheets_cred)

# --- 3. EXTRACT FROM KEY BOX T-0001 ---
print("Fetching active tenants from Key Box database...")
ref = db.reference('tenants/T-0001/boxes')
boxes = ref.get()

# Initialize with the header row for the sheet
tenant_list = [["LineID", "Room", "Status"]]

if boxes:
    for room_num, room_data in boxes.items():
        users = room_data.get('users', {})
        for line_id, is_active in users.items():
            if is_active:
                tenant_list.append([line_id, room_num, "Active"])

print(f"Found {len(tenant_list) - 1} active tenants.")

# --- 4. UPLOAD TO GOOGLE SHEETS ---
print("Uploading to Google Sheets...")
# Paste your actual Google Sheet URL here
sheet_url = "https://docs.google.com/spreadsheets/d/1UxXESKKLAItPxPXk3C8q6y62UHuwExFFDdvyqL5nRzo/edit?gid=707578519#gid=707578519"
sheet = client.open_by_url(sheet_url).worksheet("Tenants")

# Clear old directory data and write the fresh batch
sheet.clear()
sheet.update(values=tenant_list, range_name='A1')

print("Sync complete! The booking system is up to date.")
