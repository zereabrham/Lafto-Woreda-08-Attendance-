import streamlit as st
from datetime import datetime
import pandas as pd
import sqlite3
import io

# ለ PDF ሪፖርት ማዘጋጃ የሚያገለግል
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# የዳታቤዝ ስም
DB_NAME = "attendance_system_v3.db"

# የሰራተኞች እና የቢሮዎች ዳታቤዝ (Leading zeros as strings to prevent syntax errors)
EMPLOYEES_DATABASE = {
    "ፈንታሁን ካሳሁን አሊ": {
        "id": "EMP001",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የሲቪል ምዝገባ ቡድን መሪ",
    },
    "ደጉ ማርቆስ": {
        "id": "EMP002",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የነዋሪነት አገልግሎት ቡድን መሪ",
    },
    "ትግስት ተሊላ": {
        "id": "EMP003",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የሪከርድና ማህደር ህትመት ስርጭት ቁጥጥር ቡድን መሪ",
    },
    "መላኩ ቤዛው": {
        "id": "EMP004",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የነዋሪነት አገልግሎት ባለሙያ",
    },
    "ዘላለም አዲስ": {
        "id": "EMP005",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የነዋሪነት አገልግሎት ባለሙያ",
    },
    "መገርሳ ኦሊቃ": {
        "id": "EMP006",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የነዋሪነት አገልግሎት ባለሙያ",
    },
    "ደበሎ ሀይሉ": {
        "id": "EMP007",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የነዋሪነት አገልግሎት ባለሙያ",
    },
    "ንግስት ግቶሬ": {
        "id": "EMP008",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የነዋሪነት አገልግሎት ባለሙያ",
    },
    "ጀመረ ከበደ": {
        "id": "EMP009",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የክብር መዝገብ ሹም",
    },
    "ባይሳ ደበሎ": {
        "id": "EMP0010",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የክብር መዝገብ ሹም",
    },
    "መስከረም ብርሀኔ": {
        "id": "EMP0011",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የክብር መዝገብ ሹም",
    },
    "አባቦ ፍቃዱ": {
        "id": "EMP0012",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የክብር መዝገብ ሹም",
    },
    "ዳግማዊት ግርማ": {
        "id": "EMP0013",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የክብር መዝገብ ሹም",
    },
    "ደሳለኝ ፀጋዬ": {
        "id": "EMP0014",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የፋይናንስ ባለሙያ",
    },
    "ዘወትር ታምሩ": {
        "id": "EMP0015",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የፋይናንስ ባለሙያ",
    },
    "መሰረት ምስጋናው": {
        "id": "EMP0016",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የህትመት ስርጭት ቁጥጥር ባለሙያ",
    },
    "ፀሀይነሽ ስጦታው": {
        "id": "EMP0017",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የህትመት ስርጭት ቁጥጥር ባለሙያ",
    },
    "አስማሩ አካሌ": {
        "id": "EMP0018",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የሪከርድና ማህደር ባለሙያ",
    },
    "አዝመራ ሁሴን": {
        "id": "EMP0019",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "የሪከርድና ማህደር ባለሙያ",
    },
    "ስንዱ ካሳሁን": {
        "id": "EMP0020",
        "office": "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)",
        "admin": "ዘረአብርሃም ሙሉጌታ",
        "dept": "ሴክሬታሪያት",
    },
    "ናትናኤል ታደለ": {
        "id": "EMP0021",
        "office": "ቢሮ 02 (ዋና ስራአስፈፃሚ)",
        "admin": "ሰለሞን ተስፋዬ",
        "dept": "የመረጃ ቴክኖሎጂ ጥገና ባለሙያ",
    },
    "አስናቀች": {
        "id": "EMP0022",
        "office": "ቢሮ 02 (ዋና ስራአስፈፃሚ)",
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
            signature TEXT,
            timestamp TEXT
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
        ("admin_office1_1", "pass123office1", "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)", "ቢሮ 01 አድሚን 1"),
        ("admin_office2_1", "pass123office2", "ቢሮ 02 (ዋና ስራአስፈፃሚ)", "ቢሮ 02 አድሚን 1"),
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

st.set_page_config(page_title="የንፋስ ስልክ ላፍቶ ክፍለ ከተማ ወረዳ 08 አቴንዳንስ ሲስተም", layout="wide")

# --- Custom Modern UI CSS Styling ---
st.markdown("""
<style>
    /* Main Background & Font Styling */
    .stApp {
        background-color: #f4f7f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Title Customization */
    h1 {
        color: #1b4332;
        font-weight: 800;
        padding-bottom: 10px;
        border-bottom: 3px solid #2d6a4f;
    }
    
    h2, h3 {
        color: #2d6a4f;
    }

    /* Card Containers */
    .css-1r6slb0, .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    /* Tabs Styling */
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

    /* Metric Cards */
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

    /* Buttons Styling */
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

st.title("🏛️ የንፋስ ስልክ ላፍቶ ክፍለ ከተማ ወረዳ 08 አቴንዳንስ ሲስተም")

tabs = st.tabs(["✍️ ግቢ/ውጣ ምዝገባ", "🔲 QR ኮድ ማመንጫ", "📊 አድሚን ዳሽቦርድ እና ሪፖርት"])

# ----------------- TAB 1: Attendance Registration -----------------
with tabs[0]:
    st.header("✍️ የሰራተኞች ግቢ/ውጣ መዝገብ")
    
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            day_val = st.selectbox("ቀን", [str(i) for i in range(1, 32)], index=0)
        with col2:
            months_list = ["መስከረም", "ጥቅምት", "ህዳር", "ታህሳስ", "ጥር", "የካቲት", "መጋቢት", "ሚያዚያ", "ግንቦት", "ሰኔ", "ሀምሌ", "ነሐሴ", "ጳጉሜ"]
            month_val = st.selectbox("ወር", months_list, index=0)
        with col3:
            year_val = st.selectbox("ዓመተ ምህረት", [str(y) for y in range(2015, 2036)], index=3)

    search_query = st.text_input("🔎 ሰራተኛ ለመፈለግ ስም ይጻፉ").strip().lower()
    
    filtered_employees = [name for name in EMPLOYEES_DATABASE.keys() if search_query in name.lower()]
    selected_employee = st.selectbox("የሰራተኛ ስም ይምረጡ", filtered_employees if filtered_employees else list(EMPLOYEES_DATABASE.keys()))
    
    if selected_employee:
        emp_info = EMPLOYEES_DATABASE[selected_employee]
        st.success(f"👤 የተመረጠ ሰራተኛ: **{selected_employee}** | መታወቂያ: `{emp_info['id']}` | ቢሮ: {emp_info['office']} | ኃላፊ: {emp_info['admin']}")

    action_type = st.radio("ክዋኔ", ["ግቢ (Check-In)", "ውጣ (Check-Out)"], horizontal=True)
    status_type = st.selectbox("ሁኔታ", ["በሰዓት ገብቷል/ታለች", "አርፍዷል/አርፍዳለች", "ፈቃድ ነው/ናት"])

    leave_duration = "-"
    late_reason = "-"
    shift = "-"

    if "ፈቃድ" in status_type:
        st.info("📋 የእረፍት/የፈቃድ ዝርዝር መረጃ ይሙሉ")
        leave_days = st.text_input("የቀን ብዛት", "5")
        l_col1, l_col2 = st.columns(2)
        with l_col1:
            leave_from_day = st.selectbox("ከ ቀን", [str(i) for i in range(1, 32)], index=0, key="lf_day")
            leave_from_month = st.selectbox("ከ ወር", months_list, index=0, key="lf_mon")
        with l_col2:
            leave_to_day = st.selectbox("እስከ ቀን", [str(i) for i in range(1, 32)], index=4, key="lt_day")
            leave_to_month = st.selectbox("እስከ ወር", months_list, index=0, key="lt_mon")
        leave_year = st.selectbox("የፈቃድ ዓመተ ምህረት", [str(y) for y in range(2015, 2036)], index=3, key="l_yr")
        leave_duration = f"የቀን ብዛት: {leave_days} | ከ {leave_from_month} {leave_from_day} እስከ {leave_to_month} {leave_to_day}, {leave_year} ዓ.ም"
    elif "አርፍዷል" in status_type or "አርፍዳለች" in status_type:
        late_reason = st.text_input("⏰ ያረፈዱበት ምክንያት", "ምክንያት አልተጻፈም")

    if not "ፈቃድ" in status_type:
        shift = st.radio("⏰ መግቢያ/ውጣ ሰዓት መምረጫ", [
            "2:30 (የጠዋት መግቢያ)",
            "6:30 (የእኩለ ቀን መውጫ)",
            "7:30 (የከሰዓት መግቢያ)",
            "11:30 (የማታ መውጫ)"
        ], horizontal=True)

    st.markdown("---")
    sig_file = st.file_uploader("✍️ የተፈረመበትን ፋይል (ပုံ፣ ፒዲኤፍ ወይም ዶክመንት) ይጫኑ", type=["jpg", "jpeg", "png", "pdf", "docx"])

    if st.button("💾 መረጃውን በመዝገብ አስቀምጥ", type="primary"):
        if not sig_file:
            st.error("❌ እባክዎ የተፈረመበትን ፋይል ይጫኑ!")
        else:
            attendance_date = f"{month_val} {day_val}, {year_val} ዓ.ም"
            raw_date_val = datetime.now()
            current_time = get_ethiopian_time()
            sig_filename = sig_file.name

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('''
                INSERT INTO attendance (date_str, raw_date, name, emp_id, office, dept, admin, action_type, shift, status, leave_duration, late_reason, signature, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (attendance_date, raw_date_val, selected_employee, emp_info['id'], emp_info['office'], emp_info['dept'], emp_info['admin'], action_type, shift, status_type, leave_duration, late_reason, sig_filename, current_time))
            conn.commit()
            conn.close()
            st.success(f"✅ {selected_employee} መረጃው በተሳካ ሁኔታ ተመዝግቧል!")

# ----------------- TAB 2: QR Code Generator -----------------
with tabs[1]:
    st.header("🔲 የሰራተኞች QR ኮድ ማመንጫ ማዕከል")
    qr_search = st.text_input("ተለዋጭ ሰራተኛ ፈልግ", "").strip().lower()
    
    filtered_qr_emps = {name: info for name, info in EMPLOYEES_DATABASE.items() if qr_search in name.lower()}
    selected_qr_emp = st.selectbox("ሰራተኛ ይምረጡ (ለ QR)", list(filtered_qr_emps.keys()) if filtered_qr_emps else list(EMPLOYEES_DATABASE.keys()))
    
    if selected_qr_emp:
        emp = EMPLOYEES_DATABASE[selected_qr_emp]
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f1faee 100%); padding:25px; border-radius:15px; border-left: 6px solid #2d6a4f; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <h3 style="color: #1b4332; margin-top:0;">የሰራተኛ መለያ መረጃ</h3>
            <p><b>ስም:</b> {selected_qr_emp}</p>
            <p><b>መታወቂያ (ID):</b> <code style="background:#e9ecef; padding:2px 6px; border-radius:4px;">{emp['id']}</code></p>
            <p><b>ቢሮ:</b> {emp['office']}</p>
            <p><b>ክፍል:</b> {emp['dept']}</p>
            <p><b>ኃላፊ:</b> {emp['admin']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("📋 የሁሉም ሰራተኞች ዝርዝር")
    for name, emp in EMPLOYEES_DATABASE.items():
        st.markdown(f"• **ስም:** `{name}` | **መታወቂያ:** `{emp['id']}` | **ቢሮ:** {emp['office']}")

# ----------------- TAB 3: Admin Dashboard & Reports -----------------
with tabs[2]:
    st.header("📊 አድሚን ዳሽቦርድ እና ሪፖርት")
    
    if "admin_logged" not in st.session_state:
        st.session_state.admin_logged = False

    if not st.session_state.admin_logged:
        st.markdown("""
        <div style="max-width: 450px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 6px 15px rgba(0,0,0,0.08); border-top: 5px solid #2d6a4f;">
            <h3 style="text-align: center; color: #1b4332;">🔐 አድሚን መግቢያ</h3>
        """, unsafe_allow_html=True)
        
        u_input = st.text_input("ዩዘርኔም (Username)")
        p_input = st.text_input("ፓስወርድ (Password)", type="password")
        
        if st.button("ግባ ወደ ዳሽቦርድ", use_container_width=True):
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT password, office, role FROM admins WHERE username = ?", (u_input,))
            row = c.fetchone()
            conn.close()
            
            if row and row[0] == p_input:
                st.session_state.admin_logged = True
                st.session_state.admin_username = u_input
                st.session_state.admin_office = row[1]
                st.session_state.admin_role = row[2]
                st.rerun()
            else:
                st.error("❌ የተሳሳተ ዩዘርኔም ወይም ፓስወርድ!")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.success(f"እንኳን ደህና መጡ: **{st.session_state.admin_role}** ({st.session_state.admin_username})")
        if st.button("🚪 ውጣ (Logout)"):
            st.session_state.admin_logged = False
            st.rerun()

        admin_tabs = st.tabs(["📈 ሪፖርቶች እና ማጠቃለያ", "⚙️ አድሚኖች ማስተዳደሪያ"])

        with admin_tabs[0]:
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                report_period = st.selectbox("የሪፖርት ዓይነት", ["ዕለታዊ (Daily)", "ሳምንታዊ (Weekly)", "ወርሃዊ (Monthly)", "ጠቅላላ (All-Time)"])
            with f_col2:
                office_filter_list = ["ሁሉም ቢሮዎች", "ቢሮ 01 (የሲቪል ምዝገባ እና የነዋሪነት አገልግሎት)", "ቢሮ 02 (ዋና ስራአስፈፃሚ)"]
                report_office = st.selectbox("ቢሮ ማጣሪያ", office_filter_list)

            conn = sqlite3.connect(DB_NAME)
            query = "SELECT date_str, name, office, action_type, shift, status, leave_duration, late_reason, signature, timestamp FROM attendance"
            df = pd.read_sql(query, conn)
            conn.close()

            if report_office != "ሁሉም ቢሮዎች":
                df = df[df["office"] == report_office]

            # Metrics
            total_count = len(df)
            present_count = len(df[df["status"] == "በሰዓት ገብቷል/ታለች"]) if not df.empty else 0
            late_count = len(df[df["status"].str.contains("አርፍዷል|አርፍዳለች", na=False)]) if not df.empty else 0
            leave_count = len(df[df["status"].str.contains("ፈቃድ", na=False)]) if not df.empty else 0

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("ጠቅላላ የተመዘገቡ", total_count)
            m2.metric("በሰዓት የገቡ", present_count)
            m3.metric("ያረፈዱ", late_count)
            m4.metric("ፈቃድ ላይ ያሉ", leave_count)

            st.markdown("---")
            st.dataframe(df, use_container_width=True)

            # Export buttons
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                if not df.empty:
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Attendance')
                    excel_data = output.getvalue()
                    st.download_button("📥 ሪፖርቱን ወደ Excel አውርድ (.xlsx)", data=excel_data, file_name="attendance_report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            with col_ex2:
                if not df.empty:
                    pdf_buffer = io.BytesIO()
                    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                    elements = []
                    styles = getSampleStyleSheet()
                    
                    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#2c3e50'), alignment=1)
                    elements.append(Paragraph("<b>የንፋስ ስልክ ላፍቶ ክፍለ ከተማ ወረዳ 08 አቴንዳንስ ሪፖርት</b>", title_style))
                    elements.append(Spacer(1, 15))

                    table_data = [["ቀን", "ስም", "ቢሮ", "ክዋኔ", "ሁኔታ", "ሰዓት"]]
                    for _, row in df.iterrows():
                        table_data.append([str(row['date_str']), str(row['name']), str(row['office']), str(row['action_type']), str(row['status']), str(row['timestamp'])])

                    t = Table(table_data, colWidths=[80, 100, 120, 60, 90, 80])
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
                    st.download_button("📄 ሪፖርቱን ወደ PDF አውርድ (.pdf)", data=pdf_data, file_name="attendance_report.pdf", mime="application/pdf")

        with admin_tabs[1]:
            if st.session_state.admin_username == "superadmin":
                st.subheader("👑 የሱፐር አድሚን መለያ መቀየሪያ")
                s_user = st.text_input("አዲስ ሱፐር አድሚን ዩዘርኔም", "superadmin")
                s_pass = st.text_input("አዲስ ሱፐር አድሚን ፓስወርድ", type="password")
                if st.button("🔄 የሱፐር አድሚን መለያ አዘምን"):
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute("UPDATE admins SET username = ?, password = ? WHERE username = 'superadmin'", (s_user, s_pass))
                    conn.commit()
                    conn.close()
                    st.success("✅ የሱፐር አድሚን መለያ ተዘምኗል!")

                st.markdown("---")
                st.subheader("➕ አዲስ አድሚን መፍጠሪያ")
                new_u = st.text_input("ዩዘርኔም", key="new_u")
                new_p = st.text_input("ፓስወርድ", type="password", key="new_p")
                new_off = st.selectbox("ቢሮ", office_filter_list, key="new_off")
                new_role = st.text_input("ሚና/ሮል", "የቢሮ ኃላፊ አድሚን", key="new_role")
                if st.button("💾 አድሚን አስቀምጥ"):
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    try:
                        c.execute("INSERT INTO admins (username, password, office, role) VALUES (?, ?, ?, ?)", (new_u, new_p, new_off, new_role))
                        conn.commit()
                        st.success("✅ አዲስ አድሚን ተፈጥሯል!")
                    except Exception as e:
                        st.error(f"ስህተት: {e}")
                    finally:
                        conn.close()

                st.markdown("---")
                st.subheader("👥 ነባር አድሚኖች ዝርዝር")
                conn = sqlite3.connect(DB_NAME)
                admins_df = pd.read_sql("SELECT username, office, role FROM admins", conn)
                conn.close()
                st.dataframe(admins_df, use_container_width=True)

                sel_admin_to_delete = st.selectbox("ለመሰረዝ አድሚን ይምረጡ", admins_df['username'].tolist())
                if st.button("🗑️ የተመረጠውን አድሚን ሰርዝ"):
                    if sel_admin_to_delete == "superadmin":
                        st.error("❌ ዋናውን ሱፐር አድሚን መሠረዝ አይቻልም!")
                    else:
                        conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        c.execute("DELETE FROM admins WHERE username = ?", (sel_admin_to_delete,))
                        conn.commit()
                        conn.close()
                        st.success(f"✅ አድሚን {sel_admin_to_delete} ተሰርዟል!")
                        st.rerun()
            else:
                st.warning("⚠️ ይህን ገጽ ማየት የሚችሉት ዋናው አድሚን (Super Admin) ብቻ ናቸው።")