# 💊 Medicine App (Bilingual EN/AR) — Smart Display (Shows Both Names)
import streamlit as st
import pandas as pd
import re

# Config
st.set_page_config(
    page_title="💊 Drugs Data App",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Drugs_discription.csv", dtype=str, low_memory=False)
    df.columns = df.columns.str.strip()
    df = df.dropna(how="all").drop_duplicates().fillna("Unknown")
    return df

df = load_data()

# Language Setup
if "language" not in st.session_state:
    st.session_state.language = "English"

def toggle_language():
    st.session_state.language = "Arabic" if st.session_state.language == "English" else "English"

EN = {
    "title": "💊 Drugs Dataset Dashboard & Chatbot",
    "chat_header": "💬 Smart Drugs Chatbot",
    "chat_caption": "Type a drug name and choose what details to display.",
    "select_display": "Select what to display:",
    "chk_use": "Use",
    "chk_side": "⚠️ Side Effects",
    "chk_sub": "💊 Substitutes",
    "chk_tclass": "🏥 Therapeutic Class",
    "chk_cclass": "🧪 Chemical Class",
    "chk_habit": "Habit Forming",
    "chat_input": "💬 Type a drug name (e.g., augmentin)...",
    "no_match": "⚠️ No matching drug found.",
    "footer": "💊 Drugs Dashboard | Data source: Kaggle Dataset",
    "switch_lang": "Switch to Arabic",
    "lang_settings": "Language"
}

AR = {
    "title": "💊 لوحة بيانات الأدوية وروبوت المحادثة",
    "chat_header": "💬 روبوت الأدوية الذكي",
    "chat_caption": "اكتب اسم الدواء واختر التفاصيل التي تريد عرضها.",
    "select_display": "اختر ما تريد عرضه:",
    "chk_use": "الاستخدام",
    "chk_side": "⚠️ الأعراض الجانبية",
    "chk_sub": "💊 البدائل",
    "chk_tclass": "🏥 الفئة العلاجية",
    "chk_cclass": "🧪 الفئة الكيميائية",
    "chk_habit": "قابلية الإدمان",
    "chat_input": "💬 اكتب اسم دواء (مثل augmentin)...",
    "no_match": "⚠️ لم يتم العثور على دواء مطابق.",
    "footer": "💊 لوحة الأدوية | المصدر: Kaggle Dataset",
    "switch_lang": "التبديل إلى الإنجليزية",
    "lang_settings": "اللغة"
}

def get_text(key):
    return (AR if st.session_state.language == "Arabic" else EN)[key]

# Sidebar
with st.sidebar:
    st.header(get_text("lang_settings"))
    if st.button(get_text("switch_lang")):
        toggle_language()
    st.title(get_text("chat_header"))
    st.markdown("---")

# Main Interface
st.header(get_text("chat_header"))
st.caption(get_text("chat_caption"))

st.markdown("### " + get_text("select_display"))
c1, c2, c3, c4, c5, c6 = st.columns(6)
show_use  = c1.checkbox(get_text("chk_use"), True)
show_side = c2.checkbox(get_text("chk_side"), True)
show_sub  = c3.checkbox(get_text("chk_sub"), False)
show_tcl  = c4.checkbox(get_text("chk_tclass"), False)
show_ccl  = c5.checkbox(get_text("chk_cclass"), False)
show_hab  = c6.checkbox(get_text("chk_habit"), False)

st.markdown("---")

drug_name = st.text_input(get_text("chat_input"))

if drug_name:
    q = drug_name.lower().strip()

    # 🔍 بحث ذكي يشمل الاسم التجاري والعلمي (Exact Match)
    search_columns = ["TradeName", "ScientificName"]
    search_columns = [col for col in search_columns if col in df.columns]

    mask = pd.Series(False, index=df.index)
    pattern = rf"\b{re.escape(q)}\b"
    for col in search_columns:
        mask |= df[col].astype(str).str.lower().str.contains(pattern, na=False, regex=True)

    results = df[mask]

    if results.empty:
        st.warning(get_text("no_match"))
    else:
        for _, row in results.head(3).iterrows():
            trade = row.get("TradeName", "Unknown")
            sci = row.get("ScientificName", "Unknown")

            # 🎯 تحديد طريقة العرض بناءً على ما كتبه المستخدم
            if q in str(sci).lower():
                st.markdown(f"### 🧪 {sci}")
                st.caption(f"**💊 Trade Name:** {trade}")
            else:
                st.markdown(f"### 💊 {trade}")
                st.caption(f"**🧪 Scientific Name:** {sci}")

            if show_use and "use" in row:
                st.write(f"**{get_text('chk_use')}:** {row['use']}")
            if show_side and "sideEffect" in row:
                st.write(f"**{get_text('chk_side')}:** {row['sideEffect']}")
            if show_sub and "substitute" in row:
                st.write(f"**{get_text('chk_sub')}:** {row['substitute']}")
            if show_tcl and "Therapeutic Class" in row:
                st.write(f"**{get_text('chk_tclass')}:** {row['Therapeutic Class']}")
            if show_ccl and "Chemical Class" in row:
                st.write(f"**{get_text('chk_cclass')}:** {row['Chemical Class']}")
            if show_hab and "Habit Forming" in row:
                st.write(f"**{get_text('chk_habit')}:** {row['Habit Forming']}")
            st.markdown("---")

# Footer
st.markdown(
    f"<div style='text-align:center; color:#666; margin-top: 50px;'>{get_text('footer')}</div>",
    unsafe_allow_html=True
)
