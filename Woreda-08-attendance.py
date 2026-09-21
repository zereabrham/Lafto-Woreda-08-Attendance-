import streamlit as str_lit
from datetime import datetime, timedelta
import pandas as pd
import sqlite3
import io

# ለ PDF ሪፖርት ማዘጋጃ የሚያገለግል
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

DB_NAME = "attendance_system_v7.db"

EMPLOYEES_DATABASE = {
    "ፈንታሁን ካሳሁን አሊ": {
        "id": "EMP001",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የሲቪል ምዝገባ ቡድን መሪ",
    },
    "ደጉ ማርቆስ": {
        "id": "EMP002",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የነዋሪነት አገልግሎት ቡድን መሪ",
    },
    "ትግስት ተሊላ": {
        "id": "EMP003",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የሪከርድና ማህደር ህትመት ስርጭት ቁጥጥር ቡድን መሪ",
    },
    "መላኩ ቤዛው": {
        "id": "EMP004",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የነዋሪነት አገልግሎት ባለሙያ",
    },
    "ዘላለም አዲስ": {
        "id": "EMP005",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የነዋሪነት አገልግሎት ባለሙያ",
   },
    "መገርሳ ኦሊቃ": {
        "id": "EMP006",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የነዋሪነት አገልግሎት ባለሙያ",
    },
    "ደበሎ ሀይሉ": {
        "id": "EMP007",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የነዋሪነት አገልግሎት ባለሙያ",
    },
    "ንግስት ግቶሬ": {
        "id": "EMP008",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የነዋሪነት አገልግሎት ባለሙያ",
    },
    "ጀመረ ከበደ": {
        "id": "EMP009",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የክብር መዝገብ ሹም",
    },
    "ባይሳ ደበሎ": {
        "id": "EMP0010",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የክብር መዝገብ ሹም",
    },
    "መስከረም ብርሀኔ": {
        "id": "EMP0011",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የክብር መዝገብ ሹም",
    },
    "አባቦ ፍቃዱ": {
        "id": "EMP0012",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የክብር መዝገብ ሹም",
    },
    "ዳግማዊት ግርማ": {
        "id": "EMP0013",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የክብር መዝገብ ሹም",
    },
    "ደሳለኝ ፀጋዬ": {
        "id": "EMP0014",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የፋይናንስ ባለሙያ",
    },
    "ዘወትር ታምሩ": {
        "id": "EMP0015",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የፋይናንስ ባለሙያ",
    },
    "መሰረት ምስጋናው": {
        "id": "EMP0016",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የህትመት ስርጭት ቁጥጥር ባለሙያ",
    },
    "ፀሀይነሽ ስጦታው": {
        "id": "EMP0017",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የህትመት ስርጭት ቁጥጥር ባለሙያ",
    },
    "አስማሩ አካሌ": {
        "id": "EMP0018",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የሪከርድና ማህደር ባለሙያ",
    },
    "አዝመራ ሁሴን": {
        "id": "EMP0019",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የሪከርድና ማህደር ባለሙያ",
    },
    "ስንዱ ካሳሁን": {
        "id": "EMP0020",
        "office": "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "ሴክሬታሪያት",
    },
    "ናትናኤል ታደለ": {
        "id": "EMP0021",
        "office": "ቢሮ ቁጥር 02 (ዋና ስራአስፈፃሚ)",
        "admin": "ሰለሞን ተስፋዬ",
        "dept": "የመረጃ ቴክኖሎጂ ጥገና ባለሙያ",
    },
    "አስናቀች": {
        "id": "EMP0022",
        "office": "ቢሮ ቁጥር 02 (ዋና ስራአስፈፃሚ)",
        "admin": "ሰለሞን ተስፋዬ",
        "dept": "ሴክሬታሪያት",
    },
}

def init_sqlite_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_str TEXT,
            raw_date DATETIME,
            name TEXT,
            emp_id TEXT,
            office TEXT,
            dept TEXT,
            admin TEXT,
            action_type TEXT,
            shift TEXT,
            status TEXT,
            leave_duration TEXT,
            late_reason TEXT,
            worked_hours REAL,
            overtime_hours REAL,
            day_type TEXT,
            signature TEXT,
            timestamp TEXT,
            approval_status TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            username TEXT PRIMARY KEY,
            password TEXT,
            office TEXT,
            role TEXT
        )
    ''')
    
    default_admins = [
        ("superadmin", "super08password", "ሁሉም ቢሮዎች", "ዋና አድሚን (Super Admin)"),
        ("admin_office1", "pass123office1", "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)", "ቢሮ 01 አድሚን (ዘረአብርሃም)"),
        ("admin_office2", "pass123office2", "ቢሮ ቁጥር 02 (ዋና ስራአስፈፃሚ)", "ቢሮ 02 አድሚን (ሰለሞን)"),
    ]
    for adm in default_admins:
        c.execute("INSERT OR IGNORE INTO admins (username, password, office, role) VALUES (?, ?, ?, ?)", adm)
    conn.commit()
    conn.close()

init_sqlite_db()

def get_ethiopian_time():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    date_str = now.strftime("%Y-%m-%d")
    if 6 <= hour < 18:
        eth_hour = hour - 6
        if eth_hour == 0: eth_hour = 12
        period = "ጠዋት" if hour < 12 else "ከሰዓት"
    else:
        eth_hour = hour - 18 if hour >= 18 else hour + 6
        if eth_hour == 0: eth_hour = 12
        period = "ማታ"
    return f"{date_str} {eth_hour}:{minute:02d}:{second:02d} {period}"

str_lit.set_page_config(page_title="የንፋስ ስልክ ላፍቶ ክፍለ ከተማ ወረዳ 08 አቴንዳንስ ሲስተም", layout="wide")

str_lit.markdown("""
<style>
    .stApp {
        background-color: #f4f7f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1 {
        color: #1b4332;
        font-weight: 800;
        padding-bottom: 10px;
        border-bottom: 3px solid #2d6a4f;
    }
    h2, h3 {
        color: #2d6a4f;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e9ecef;
        border-radius: 8px 8px 0px 0px;
        color: #212529;
        font-weight: bold;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2d6a4f !important;
        color: white !important;
    }
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #2d6a4f 0%, #40916c 100%);
        border: none;
        padding: 15px;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div[data-testid="metric-container"] label {
        color: #e9ecef !important;
        font-weight: 600;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: white !important;
        font-size: 26px;
    }
    .stButton button {
        background-color: #2d6a4f;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #1b4332;
        color: #ffffff;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

str_lit.title("🏛️ የንፋስ ስልክ ላፍቶ ክፍለ ከተማ ወረዳ 08 አቴንዳንስ ሲስተም")

tabs = str_lit.tabs(["✍️ ግቢ/ውጣ ምዝገባ", "🔲 QR ኮድ ማመንጫ", "📊 አድሚን ዳሽቦርድ እና ማጽደቂያ"])

# ----------------- TAB 1: Attendance Registration -----------------
with tabs[0]:
    str_lit.header("✍️ የሰራተኞች ግቢ/ውጣ መዝገብ")
    
    with str_lit.container():
        col1, col2, col3 = str_lit.columns(3)
        with col1:
            day_val = str_lit.selectbox("ቀን", [str(i) for i in range(1, 32)], index=0)
        with col2:
            months_list = ["መስከረም", "ጥቅምት", "ህዳር", "ታህሳስ", "ጥር", "የካቲት", "መጋቢት", "ሚያዚያ", "ግንቦት", "ሰኔ", "ሀምሌ", "ነሐሴ", "ጳጉሜ"]
            month_val = str_lit.selectbox("ወር", months_list, index=0)
        with col3:
            year_val = str_lit.selectbox("ዓመተ ምህረት", [str(y) for y in range(2015, 2036)], index=3)

    search_query = str_lit.text_input("🔎 ሰራተኛ ለመፈለግ ስም ይጻፉ").strip().lower()
    
    filtered_employees = [name for name in EMPLOYEES_DATABASE.keys() if search_query in name.lower()]
    selected_employee = str_lit.selectbox("የሰራተኛ ስም ይምረጡ", filtered_employees if filtered_employees else list(EMPLOYEES_DATABASE.keys()))
    
    if selected_employee:
        emp_info = EMPLOYEES_DATABASE[selected_employee]
        str_lit.success(f"👤 የተመረጠ ሰራተኛ: **{selected_employee}** | መታወቂያ: `{emp_info['id']}` | ቢሮ: {emp_info['office']} | ኃላፊ: {emp_info['admin']}")

    action_type = str_lit.radio("ክዋኔ", ["ግቢ (Check-In)", "ውጣ (Check-Out)"], horizontal=True)
    
    day_type = str_lit.selectbox("የቀኑ ሁኔታ (Day/Shift Type)", [
        "መደበኛ የስራ ቀን (Day)",
        "ማታ ስራ (Night Shift)",
        "ቅዳሜ / እሁድ የትርፍ ስዓት (Weekend Overtime)"
    ])

    shift = str_lit.radio("⏰ መግቢያ/ውጣ ሰዓት መምረጫ (ፈረቃ)", [
        "2:30 (የጠዋት መግቢያ - ከ 2:10 ጀምሮ አክቲቭ)",
        "6:30 (የእኩለ ቀን መውጫ - ከአርብ 5:30 ጀምሮ አክቲቭ)",
        "7:30 (የከሰዓት መግቢያ - ከ 7:30 ጀምሮ አክቲቭ)",
        "11:30 (የማታ መውጫ - ከ 11:15 ጀምሮ አክቲቭ)"
    ], horizontal=True)

    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    
    is_auto_late = False
    is_active_allowed = True

    if "2:30" in shift:
        if (current_hour < 8) or (current_hour == 8 and current_minute < 10):
            is_active_allowed = False
        if (current_hour > 8) or (current_hour == 8 and current_minute > 45):
            is_auto_late = True
    elif "6:30" in shift:
        if (current_hour > 12) or (current_hour == 12 and current_minute > 45):
            is_auto_late = True
    elif "7:30" in shift:
        if (current_hour < 13) or (current_hour == 13 and current_minute < 30):
            is_active_allowed = False
        if (current_hour > 13) or (current_hour == 13 and current_minute > 45):
            is_auto_late = True
    elif "11:30" in shift:
        if (current_hour < 17) or (current_hour == 17 and current_minute < 15):
            is_active_allowed = False
        if (current_hour > 17) or (current_hour == 17 and current_minute > 45):
            is_auto_late = True

    if not is_active_allowed:
        str_lit.warning("⚠️ ትኩረት: ለዚህ ፈረቃ የተፈቀደው የአክቲቭ ሰዓት ገደብ ገና አልደረሰም!")

    default_status_index = 1 if is_auto_late else 0
    status_type = str_lit.selectbox("ሁኔታ", ["በሰዓት ገብቷል/ታለች", "አርፍዷል/አርፍዳለች", "ፈቃድ ነው/ናት"], index=default_status_index)

    if is_auto_late and status_type != "ፈቃድ ነው/ናት":
        str_lit.warning("⚠️ ከፈረቃ ሰዓት ውጭ ከ 15 ደቂቃ በላይ ዘግይተው ስለተመዘገቡ ሲስተሙ በራስ-ሰር 'አርፍዷል' ብሎ መዝግቧል!")

    leave_duration = "-"
    late_reason = "-"

    if "ፈቃድ" in status_type:
        str_lit.info("📋 የእረፍት/የፈቃድ ዝርዝር መረጃ ይሙሉ")
        leave_days = str_lit.text_input("የቀን ብዛት", "5")
        l_col1, l_col2 = str_lit.columns(2)
        with l_col1:
            leave_from_day = str_lit.selectbox("ከ ቀን", [str(i) for i in range(1, 32)], index=0, key="lf_day")
            leave_from_month = str_lit.selectbox("ከ ወር", months_list, index=0, key="lf_mon")
        with l_col2:
            leave_to_day = str_lit.selectbox("እስከ ቀን", [str(i) for i in range(1, 32)], index=4, key="lt_day")
            leave_to_month = str_lit.selectbox("እስከ ወር", months_list, index=0, key="lt_mon")
        leave_year = str_lit.selectbox("የፈቃድ ዓመተ ምህረት", [str(y) for y in range(2015, 2036)], index=3, key="l_yr")
        leave_duration = f"የቀን ብዛት: {leave_days} | ከ {leave_from_month} {leave_from_day} እስከ {leave_to_month} {leave_to_day}, {leave_year} ዓ.ም"
    elif "አርፍዷል" in status_type or "አርፍዳለች" in status_type or is_auto_late:
        late_reason = str_lit.text_input("⏰ ያረፈዱበት/የዘገዩበት ምክንያት", "ምክንያት ተጻፈ")

    str_lit.markdown("### ⏱️ የስራ ሰዓት እና የትርፍ ሰዓት ስሌት መለኪያ")
    w_col1, w_col2 = str_lit.columns(2)
    with w_col1:
        worked_hours = str_lit.number_input("የተሰራ ሰዓት ብዛት (በሰዓት)", min_value=0.0, max_value=24.0, value=8.0, step=0.5)
    with w_col2:
        overtime_hours = str_lit.number_input("የትርፍ ሰዓት ብዛት (Overtime Hours)", min_value=0.0, max_value=12.0, value=0.0, step=0.5)

    str_lit.markdown("---")
    sig_file = str_lit.file_uploader("✍️ የተፈረመበትን ፋይል (ပုံ፣ ፒዲኤፍ ወይም ዶክመንት) ይጫኑ", type=["jpg", "jpeg", "png", "pdf", "docx"])

    if str_lit.button("💾 መረጃውን ለአድሚን ማጽደቂያ ላክ", type="primary"):
        if not sig_file:
            str_lit.error("❌ እባክዎ የተፈረመበትን ፋይል ይጫኑ!")
        else:
            attendance_date = f"{month_val} {day_val}, {year_val} ዓ.ም"
            raw_date_val = datetime.now()
            current_time = get_ethiopian_time()
            sig_filename = sig_file.name
            approval_status = "በማጣራት ላይ (Pending)"

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('''
                INSERT INTO attendance (date_str, raw_date, name, emp_id, office, dept, admin, action_type, shift, status, leave_duration, late_reason, worked_hours, overtime_hours, day_type, signature, timestamp, approval_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (attendance_date, raw_date_val, selected_employee, emp_info['id'], emp_info['office'], emp_info['dept'], emp_info['admin'], action_type, shift, status_type, leave_duration, late_reason, worked_hours, overtime_hours, day_type, sig_filename, current_time, approval_status))
            conn.commit()
            conn.close()
            str_lit.success(f"✅ {selected_employee} ጥያቄው ተልኳል! አድሚኑ እስኪገመግመው ይጠብቁ።")

# ----------------- TAB 2: QR Code Generator -----------------
with tabs[1]:
    str_lit.header("🔲 የሰራተኞች QR ኮድ ማመንጫ ማዕከል")
    qr_search = str_lit.text_input("ተለዋጭ ሰራተኛ ፈልግ", "").strip().lower()
    
    filtered_qr_emps = {name: info for name, info in EMPLOYEES_DATABASE.items() if qr_search in name.lower()}
    selected_qr_emp = str_lit.selectbox("ሰራተኛ ይምረጡ (ለ QR)", list(filtered_qr_emps.keys()) if filtered_qr_emps else list(EMPLOYEES_DATABASE.keys()))
    
    if selected_qr_emp:
        emp = EMPLOYEES_DATABASE[selected_qr_emp]
        str_lit.markdown(f"""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f1faee 100%); padding:25px; border-radius:15px; border-left: 6px solid #2d6a4f; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <h3 style="color: #1b4332; margin-top:0;">የሰራተኛ መለያ መረጃ</h3>
            <p><b>ስም:</b> {selected_qr_emp}</p>
            <p><b>መታወቂያ (ID):</b> <code style="background:#e9ecef; padding:2px 6px; border-radius:4px;">{emp['id']}</code></p>
            <p><b>ቢሮ:</b> {emp['office']}</p>
            <p><b>ክፍል:</b> {emp['dept']}</p>
            <p><b>ኃላፊ:</b> {emp['admin']}</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 3: Admin Dashboard, Approvals & Reports -----------------
with tabs[2]:
    str_lit.header("📊 አድሚን ዳሽቦርድ እና ማጽደቂያ ማዕከል")
    
    if "admin_logged" not in str_lit.session_state:
        str_lit.session_state.admin_logged = False

    if not str_lit.session_state.admin_logged:
        str_lit.markdown("""
        <div style="max-width: 450px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 6px 15px rgba(0,0,0,0.08); border-top: 5px solid #2d6a4f;">
            <h3 style="text-align: center; color: #1b4332;">🔐 አድሚን መግቢያ</h3>
        """, unsafe_allow_html=True)
        
        u_input = str_lit.text_input("ዩዘርኔም (Username)")
        p_input = str_lit.text_input("ፓስወርድ (Password)", type="password")
        
        if str_lit.button("ግባ ወደ ዳሽቦርድ", use_container_width=True):
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT password, office, role FROM admins WHERE username = ?", (u_input,))
            row = c.fetchone()
            conn.close()
            
            if row and row[0] == p_input:
                str_lit.session_state.admin_logged = True
                str_lit.session_state.admin_username = u_input
                str_lit.session_state.admin_office = row[1]
                str_lit.session_state.admin_role = row[2]
                str_lit.rerun()
            else:
                str_lit.error("❌ የተሳሳተ ዩዘርኔም ወይም ፓስወርድ!")
        str_lit.markdown("</div>", unsafe_allow_html=True)
    else:
        str_lit.success(f"እንኳን ደህና መጡ: **{str_lit.session_state.admin_role}** ({str_lit.session_state.admin_username})")
        if str_lit.button("🚪 ውጣ (Logout)"):
            str_lit.session_state.admin_logged = False
            str_lit.rerun()

        admin_tabs = str_lit.tabs(["📥 የምዝገባ ማጽደቂያ (Approvals)", "📈 የጸደቁ ሪፖርቶች እና ማጣሪያ", "⚙️ አድሚኖች ማስተዳደሪያ እና መፍጠሪያ"])

        # TAB 3.1: Approvals
        with admin_tabs[0]:
            str_lit.subheader("🛠️ የሰራተኞች የምዝገባና የፈቃድ ጥያቄዎች ማጣሪያ")
            
            conn = sqlite3.connect(DB_NAME)
            query = "SELECT id, date_str, name, office, action_type, status, leave_duration, late_reason, worked_hours, overtime_hours, day_type, timestamp, approval_status FROM attendance WHERE approval_status = 'በማጣራት ላይ (Pending)'"
            pending_df = pd.read_sql(query, conn)
            conn.close()

            if str_lit.session_state.admin_username != "superadmin":
                pending_df = pending_df[pending_df["office"] == str_lit.session_state.admin_office]

            if pending_df.empty:
                str_lit.info("🎉 ምንም በመጠባበቅ ላይ ያለ አዲስ ጥያቄ የለም!")
            else:
                for index, row in pending_df.iterrows():
                    with str_lit.expander(f"📌 {row['name']} - {row['status']} ({row['action_type']}) - ቀን: {row['date_str']}"):
                        str_lit.write(f"**ቢሮ:** {row['office']}")
                        str_lit.write(f"**የቀኑ ሁኔታ:** {row['day_type']}")
                        str_lit.write(f"**ሁኔታ:** {row['status']}")
                        str_lit.write(f"**የተሰራ ሰዓት:** {row['worked_hours']} ሰዓት | **የትርፍ ሰዓት:** {row['overtime_hours']} ሰዓት")
                        str_lit.write(f"**የፈቃድ ዝርዝር:** {row['leave_duration']}")
                        str_lit.write(f"**ያረፈደበት ምክንያት:** {row['late_reason']}")
                        str_lit.write(f"**የተላከበት ሰዓት:** {row['timestamp']}")
                        
                        col_acc, col_rej, col_ret = str_lit.columns(3)
                        
                        with col_acc:
                            if str_lit.button("✅ Accept (ተቀበል)", key=f"acc_{row['id']}"):
                                conn = sqlite3.connect(DB_NAME)
                                c = conn.cursor()
                                c.execute("UPDATE attendance SET approval_status = 'ጸድቋል (Approved)' WHERE id = ?", (row['id'],))
                                conn.commit()
                                conn.close()
                                str_lit.success("ጥያቄው ተቀባይነት አግኝቷል!")
                                str_lit.rerun()
                                
                        with col_rej:
                            if str_lit.button("❌ Reject (ውድቅ አድርግ)", key=f"rej_{row['id']}"):
                                conn = sqlite3.connect(DB_NAME)
                                c = conn.cursor()
                                c.execute("UPDATE attendance SET approval_status = 'ውድቅ ተደርጓል (Rejected)' WHERE id = ?", (row['id'],))
                                conn.commit()
                                conn.close()
                                str_lit.warning("ጥያቄው ውድቅ ተደርጓል!")
                                str_lit.rerun()
                                
                        with col_ret:
                            if str_lit.button("🔄 Return (እንዲስተካከል መልስ)", key=f"ret_{row['id']}"):
                                conn = sqlite3.connect(DB_NAME)
                                c = conn.cursor()
                                c.execute("UPDATE attendance SET approval_status = 'ተመልሷል (Returned)' WHERE id = ?", (row['id'],))
                                conn.commit()
                                conn.close()
                                str_lit.info("ጥያቄው እንዲስተካከል ተመልሷል!")
                                str_lit.rerun()

        # TAB 3.2: Daily, Weekly, Monthly, Yearly Reports & Office Breakdown
        with admin_tabs[1]:
            str_lit.subheader("📈 ዕለታዊ፣ ሳምንታዊ፣ ወርሃዊ እና ዓመታዊ ሪፖርቶች ማዕከል")
            
            conn = sqlite3.connect(DB_NAME)
            query = "SELECT date_str, raw_date, name, office, action_type, shift, status, worked_hours, overtime_hours, day_type, leave_duration, late_reason, timestamp FROM attendance WHERE approval_status = 'ጸድቋል (Approved)'"
            df = pd.read_sql(query, conn)
            conn.close()

            if not df.empty:
                df['raw_date'] = pd.to_datetime(df['raw_date'], errors='coerce')

            # የጊዜ ማጣሪያ ምርጫ (Time Filter)
            time_filter = str_lit.selectbox("የሪፖርት የጊዜ ገደብ ይምረጡ", [
                "ሁሉም (All-Time)",
                "ዕለታዊ ሪፖርት (Daily)",
                "ሳምንታዊ ሪፖርት (Weekly)",
                "ወርሃዊ ሪፖርት (Monthly)",
                "ዓመታዊ ሪፖርት (Yearly)"
            ])

            if not df.empty and time_filter != "ሁሉም (All-Time)":
                now = datetime.now()
                if "ዕለታዊ" in time_filter:
                    df = df[df['raw_date'].dt.date == now.date()]
                elif "ሳምንታዊ" in time_filter:
                    start_week = now - timedelta(days=7)
                    df = df[df['raw_date'] >= start_week]
                elif "ወርሃዊ" in time_filter:
                    df = df[(df['raw_date'].dt.year == now.year) & (df['raw_date'].dt.month == now.month)]
                elif "ዓመታዊ" in time_filter:
                    df = df[df['raw_date'].dt.year == now.year]

            # የቢሮ ማጣሪያ ምርጫ (Office Filter)
            unique_offices = ["ሁሉም ቢሮዎች"] + list(df["office"].unique()) if not df.empty else ["ሁሉም ቢሮዎች"]
            selected_report_office = str_lit.selectbox("ቢሮ ይምረጡ", unique_offices)

            if str_lit.session_state.admin_username != "superadmin":
                selected_report_office = str_lit.session_state.admin_office
                str_lit.info(f"ማሳሰቢያ፦ የእርስዎ መለያ ማየት የሚችለው ለተፈቀደለት ቢሮ ብቻ ነው: {selected_report_office}")

            if selected_report_office != "ሁሉም ቢሮዎች" and not df.empty:
                df = df[df["office"] == selected_report_office]

            # ሪፖርት ማጠቃለያ መለኪያዎች (Metrics)
            total_count = len(df)
            present_count = len(df[df["status"] == "በሰዓት ገብቷል/ታለች"]) if not df.empty else 0
            late_count = len(df[df["status"].str.contains("አርፍዷል|አርፍዳለች", na=False)]) if not df.empty else 0
            leave_count = len(df[df["status"].str.contains("ፈቃድ", na=False)]) if not df.empty else 0
            total_worked = df["worked_hours"].sum() if not df.empty else 0
            total_ot = df["overtime_hours"].sum() if not df.empty else 0

            str_lit.markdown(f"### 📋 የ {selected_report_office} ማጠቃለያ ሪፖርት ({time_filter})")
            m1, m2, m3, m4, m5 = str_lit.columns(5)
            m1.metric("ጠቅላላ የገቡ", total_count)
            m2.metric("በሰዓት የገቡ", present_count)
            m3.metric("ያረፈዱ", late_count)
            m4.metric("ፈቃድ ላይ ያሉ", leave_count)
            m5.metric("የትርፍ ሰዓት (OT)", f"{total_ot} ሰዓት")

            str_lit.markdown("---")
            str_lit.dataframe(df[["date_str", "name", "office", "action_type", "status", "worked_hours", "overtime_hours", "timestamp"]], use_container_width=True)

            col_ex1, col_ex2 = str_lit.columns(2)
            with col_ex1:
                if not df.empty:
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Report')
                    excel_data = output.getvalue()
                    str_lit.download_button("📥 ሪፖርቱን ወደ Excel አውርድ (.xlsx)", data=excel_data, file_name="attendance_report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            with col_ex2:
                if not df.empty:
                    pdf_buffer = io.BytesIO()
                    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                    elements = []
                    styles = getSampleStyleSheet()
                    
                    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#2c3e50'), alignment=1)
                    elements.append(Paragraph(f"<b>የንፋስ ስልክ ላፍቶ ክፍለ ከተማ ወረዳ 08 ሪፖርት ({selected_report_office})</b>", title_style))
                    elements.append(Spacer(1, 15))

                    table_data = [["ቀን", "ስም", "ቢሮ", "ሁኔታ", "ሰዓት", "OT"]]
                    for _, row in df.iterrows():
                        table_data.append([str(row['date_str']), str(row['name']), str(row['office']), str(row['status']), str(row['timestamp']), str(row['overtime_hours'])])

                    t = Table(table_data, colWidths=[75, 100, 115, 80, 80, 50])
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d6a4f')),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0,0), (-1,0), 6),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                        ('FONTSIZE', (0,0), (-1,-1), 8),
                    ]))
                    elements.append(t)
                    doc.build(elements)
                    pdf_data = pdf_buffer.getvalue()
                    str_lit.download_button("📄 ሪፖርቱን ወደ PDF አውርድ (.pdf)", data=pdf_data, file_name="attendance_report.pdf", mime="application/pdf")

        # TAB 3.3: Admin Management & Creator
        with admin_tabs[2]:
            if str_lit.session_state.admin_username == "superadmin":
                str_lit.subheader("👑 አዲስ አድሚን መፍጠሪያ (Add New Admin)")
                
                with str_lit.form("new_admin_form"):
                    new_user = str_lit.text_input("አዲስ ዩዘርኔም (Username)")
                    new_pass = str_lit.text_input("ፓስወርድ (Password)", type="password")
                    new_office = str_lit.selectbox("የሚቆጣጠረው ቢሮ", [
                        "ሁሉም ቢሮዎች",
                        "ቢሮ ቁጥር 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
                        "ቢሮ ቁጥር 02 (ዋና ስራአስፈፃሚ)"
                    ])
                    new_role = str_lit.text_input("የአድሚኑ ስም እና የኃላፊነት መግለጫ (Role)", "ቢሮ አድሚን")
                    
                    submit_admin = str_lit.form_submit_button("➕ አዲስ አድሚን ፍጠር")
                    if submit_admin:
                        if new_user and new_pass:
                            try:
                                conn = sqlite3.connect(DB_NAME)
                                c = conn.cursor()
                                c.execute("INSERT INTO admins (username, password, office, role) VALUES (?, ?, ?, ?)", (new_user, new_pass, new_office, new_role))
                                conn.commit()
                                conn.close()
                                str_lit.success(f"✅ አዲሱ አድሚን ({new_user}) በተሳካ ሁኔታ ተፈጥሯል!")
                            except sqlite3.IntegrityError:
                                str_lit.error("❌ ይህ ዩዘርኔም ቀደም ሲል አለ፤ እባክዎ වෙන ስም ይጠቀሙ።")
                        else:
                            str_lit.error("❌ እባክዎ ዩዘርኔም እና ፓስወርድ በትክክል ይሙሉ!")

                str_lit.markdown("---")
                str_lit.subheader("👥 ነባር አድሚኖች ዝርዝር")
                conn = sqlite3.connect(DB_NAME)
                admins_df = pd.read_sql("SELECT username, office, role FROM admins", conn)
                conn.close()
                str_lit.dataframe(admins_df, use_container_width=True)
            else:
                str_lit.warning("⚠️ አድሚኖችን ማስተዳደር እና አዲስ መፍጠር የሚችሉት ዋናው ሱፐር አድሚን ብቻ ናቸው።")
