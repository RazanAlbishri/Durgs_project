# 💊 Medicine App (Bilingual EN/AR) — Full EDA + Chatbot

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import re

# Config
st.set_page_config(
    page_title="💊 Drugs Data App",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

CSV_PATH = r"medicines.csv"

# Language (EN / AR)
if "language" not in st.session_state:
    st.session_state.language = "English"

def toggle_language():
    st.session_state.language = "Arabic" if st.session_state.language == "English" else "English"

EN = {
    "title": "💊 Durgs Dataset Dashboard & Chatbot",
    "eda_tab": "📊 EDA Dashboard",
    "chat_tab": "💬 Chatbot Assistant",
    "lang_settings": "🌐 Language",
    "switch_lang": "🔄 Switch to Arabic",
    "overview": "📋 Data Overview",
    "data_sample": "Data Sample",
    "data_summary": "Data Summary",
    "rows": "Number of rows:",
    "columns": "Number of columns",
    "no_missing": "✅ No missing values found!",
    "no_duplicates": "✅ No duplicate rows found!",
    "stats": "📊 Data Statistics",
    "num_drugs": "Number of Drugs in Dataset",
    "top_ther": "🏥 Top Therapeutic Classes",
    "top_chem": "🧪 Top Chemical Classes",
    "habit_pie": "Habit Forming Drugs Distribution",
    "top_side": "Top 20 Reported Side Effects",
    "top_uses": "📈 Top 20 Drug Uses",
    "subs_hist": "🔄 Distribution of Substitute Counts per Drug",
    "subs_top10": "Top 10 Drugs with Most Substitutes",
    "quick_overview": "#### Quick Overview",
    "top_action": "Top 10 Action Classes",
    "habit_dist": "Habit Forming Distribution",
    "use_chart": "Top 10 Common Drug Uses",
    "corr": "📊 Correlation Heatmap",
    "summary": "📌 Summary Insights",
    "chat_header": "💬 Smart drug Chatbot",
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
    "uni_med":"Unique Drugs",
    "the_cls":"Therapeutic Classes",
    "uni_side":"Unique Side Effects",
    "avlb_sub":"Available Substitutes",
    "footer": "💊 Drugs Dashboard | Data source: Kaggle Dataset"
}

AR = {
    "title": "💊 لوحة بيانات الأدوية وروبوت المحادثة",
    "eda_tab": "📊 لوحة التحليل",
    "chat_tab": "💬 روبوت المحادثة",
    "lang_settings": "🌐 اللغة",
    "switch_lang": "🔄 التبديل إلى الإنجليزية",
    "overview": "📋 نظرة عامة على البيانات",
    "data_sample": "عينة من البيانات",
    "data_summary": "ملخص البيانات",
    "rows": "عدد الصفوف",
    "columns": "عدد الأعمدة",
    "no_missing": "✅ لا توجد قيم مفقودة!",
    "no_duplicates": "✅ لا توجد صفوف مكررة!",
    "stats": "📊 التحليل الإحصائي",
    "num_drugs": "عدد الأدوية في مجموعة البيانات",
    "top_ther": "🏥 أكثر الفئات العلاجية تكرارًا",
    "top_chem": "🧪 أكثر الفئات الكيميائية تكرارًا",
    "habit_pie": " توزيع قابلية الإدمان",
    "top_side": " أكثر 20 عَرَضًا جانبيًا انتشارًا",
    "top_uses": "📈 أكثر 20 استخدامًا شيوعًا",
    "quick_overview": "#### نظرة سريعة",
    "top_action": "أعلى 10 فئات تأثيرًا",
    "habit_dist": "توزيع الأدوية القابلة للإدمان",
    "use_chart": "أكثر 10 استخدامات شيوعًا للأدوية",
    "subs_hist": "🔄 توزيع عدد البدائل لكل دواء",
    "subs_top10": " أعلى 10 أدوية بعدد بدائل",
    "corr": "📊 خريطة الارتباط",
    "summary": " ملخص الاستنتاجات",
    "chat_header": "💬 روبوت محادثة الأدوية",
    "chat_caption": "اكتب اسم دواء واختر التفاصيل التي تريد عرضها.",
    "select_display": "اختر ما تريد عرضه:",
    "chk_use": "الاستخدام",
    "chk_side": "⚠️ الأعراض الجانبية",
    "chk_sub": "💊 البدائل",
    "chk_tclass": "🏥 الفئة العلاجية",
    "chk_cclass": "🧪 الفئة الكيميائية",
    "chk_habit": "قابلية الإدمان",
    "chat_input": "💬 اكتب اسم دواء (مثل augmentin)...",
    "no_match": "⚠️ لم يتم العثور على دواء مطابق.",
    "uni_med" : "عدد الأدوية الفريدة",
    "the_cls":"عدد الفئات العلاجية",
    "uni_side":"عدد الأعراض الجانبية الفريدة",
    "avlb_sub":"عدد البدائل المتاحة",
    "footer": "💊 لوحة الأدوية | المصدر: Kaggle Dataset"
}

def get_text(key):
    return (AR if st.session_state.language == "Arabic" else EN).get(key, key)

# Sidebar
with st.sidebar:
    st.header(get_text("lang_settings"))
    if st.button(get_text("switch_lang")):
        toggle_language()
    st.title(get_text("title"))
    st.markdown("---")

# Load data

@st.cache_data
def load_data():
    df = pd.read_csv(
        r"medicines.csv",
        dtype=str,
        low_memory=False
    )
    df.columns = df.columns.str.strip()

    df = df.dropna(how="all").copy()            
    df = df.drop_duplicates(keep="first").copy()  
    df = df.dropna(subset=["name"]).copy()      

    df = df.dropna(axis=1, how="all").copy()

    df = df.fillna("Unknown")

    df.reset_index(drop=True, inplace=True)
    return df

data = load_data()

# Tabs
st.title(get_text("title"))
tab1, tab2 = st.tabs([get_text("eda_tab"), get_text("chat_tab")])

# TAB 1: EDA
with tab1:
    st.markdown(get_text("quick_overview"))

    col1, col2, col3, col4 = st.columns(4)

    total_meds = data["name"].nunique()
    classes = data["Therapeutic Class"].nunique() if "Therapeutic Class" in data.columns else 0
    side_effects = data["sideEffect"].nunique() if "sideEffect" in data.columns else 0
    subs = data["substitute"].nunique() if "substitute" in data.columns else 0

    col1.metric(get_text("uni_med"), f"{total_meds:,}")
    col2.metric(get_text("the_cls"), f"{classes:,}")
    col3.metric(get_text("uni_side"), f"{side_effects:,}")
    col4.metric(get_text("avlb_sub"), f"{subs:,}")

    st.header(get_text("overview"))
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📋 " + get_text("data_sample"))
        st.dataframe(data.head(10))

    with col2:
        st.subheader("🔍 " + get_text("data_summary"))
        st.write(f"**{get_text('rows')}:** {data.shape[0]:,}")
        st.write(f"**{get_text('columns')}:** {data.shape[1]}")
        st.success(get_text("no_missing"))
        st.success(get_text("no_duplicates"))

    st.markdown("---")
    st.header(get_text("stats"))

# Plot 1:Therapeutic Class
    if "Therapeutic Class" in data.columns:
        st.subheader(get_text("top_ther"))
        top_thera = data["Therapeutic Class"].value_counts().head(20).reset_index()
        top_thera.columns = ["Therapeutic Class", "Count"]
        fig = px.bar(top_thera, x="Therapeutic Class", y="Count", color="Count",
                     text="Count", color_continuous_scale="Blues")
        fig.update_traces(textposition="outside")
        fig.update_layout(xaxis_tickangle=-60, height=450)
        st.plotly_chart(fig, use_container_width=True)

# Plot 2: Action Class Count 
    if "Action Class" in data.columns:
        st.subheader(get_text("top_action"))
        fig2 = px.bar(
            data["Action Class"].value_counts().head(10),
            labels={"index": "Action Class", "value": "Count"},
            color=data["Action Class"].value_counts().head(10).values
        )
        st.plotly_chart(fig2, use_container_width=True)

# Plot 3: Habit Forming Distribution
    if "Habit Forming" in data.columns:
        st.subheader(get_text("habit_dist"))
        fig3 = px.pie(
            data, names="Habit Forming",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig3, use_container_width=True)

# Plot 4: Clean Common Drug Uses Chart
    if "use" in data.columns:
        use_counts = (
            data["use"].dropna().str.split(",").explode().str.strip().value_counts().head(10)
        )
        st.subheader(get_text("use_chart"))
    fig4 = px.bar(
        use_counts,
        x=use_counts.values,
        y=use_counts.index,
        orientation="h",  
        labels={"x": "Frequency", "y": "Drug Use"},
    )
    fig4.update_layout(
        showlegend=False,
        title_x=None,
        margin=dict(l=100, r=40, t=50, b=40)
    )
    st.plotly_chart(fig4, use_container_width=True)


#------------------------------------------------------------------------------------
# TAB 2: Chatbot
with tab2:
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

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input(get_text("chat_input")):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        q = prompt.lower().strip()
        results = data[data["name"].astype(str).str.lower().str.contains(q, na=False)]

        if results.empty:
            resp = get_text("no_match")
        else:
            resp = ""
            for _, row in results.head(3).iterrows():
                resp += f"### 🩺 {row['name']}\n"
                if show_use and "use" in row:
                    resp += f"**{get_text('chk_use')}:** {row['use']}\n\n"
                if show_side and "sideEffect" in row:
                    resp += f"**{get_text('chk_side')}:** {row['sideEffect']}\n\n"
                if show_sub and "substitute" in row:
                    resp += f"**{get_text('chk_sub')}:** {row['substitute']}\n\n"
                if show_tcl and "Therapeutic Class" in row:
                    resp += f"**{get_text('chk_tclass')}:** {row['Therapeutic Class']}\n\n"
                if show_ccl and "Chemical Class" in row:
                    resp += f"**{get_text('chk_cclass')}:** {row['Chemical Class']}\n\n"
                if show_hab and "Habit Forming" in row:
                    resp += f"**{get_text('chk_habit')}:** {row['Habit Forming']}\n\n"
                resp += "---\n"

        st.session_state.chat_history.append({"role": "assistant", "content": resp})
        with st.chat_message("assistant"):
            st.markdown(resp)

# Footer
st.markdown("---")
st.markdown(f"<div style='text-align:center; color:#666;'>{get_text('footer')}</div>", unsafe_allow_html=True)
