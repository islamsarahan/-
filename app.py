import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="إدارة مهام المكتب الفني", layout="wide", page_icon="📋")

st.markdown("""
    <style>
    .main { text-align: right; }
    h1, h2, h3, p, div { text-align: right; direction: rtl; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("📋 نظام إدارة مهام المكتب الفني والمؤقت الزمني")
st.write("مرحباً بك! يمكنك إضافة المهام وتتبعها ومشاركتها عبر الرابط.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

with st.expander("➕ إضافة مهمة جديدة", expanded=True):
    with st.form("task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            task_name = st.text_input("اسم المهمة *")
            project_name = st.text_input("المشروع / المعدة")
            req_dept = st.text_input("الجهة الطالبة")
        with col2:
            assignee = st.text_input("القائم بالعمل")
            priority = st.selectbox("الأولوية", ["عالي جداً", "عالي", "متوسط", "عادي"], index=2)
            timer_min = st.number_input("الوقت المخصص (بالدقائق)", min_value=1, value=30, step=5)

        submit_button = st.form_submit_button("حفظ وإضافة المهمة")

        if submit_button:
            if not task_name:
                st.error("يرجى كتابة اسم المهمة على الأقل.")
            else:
                new_task = {
                    "كود": len(st.session_state.tasks) + 101,
                    "اسم المهمة": task_name,
                    "المشروع/المعدة": project_name,
                    "الجهة الطالبة": req_dept,
                    "القائم بالعمل": assignee,
                    "الأولوية": priority,
                    "الوقت المخصص (دقيقة)": timer_min,
                    "تاريخ الإضافة": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "الحالة": "قيد الانتظار"
                }
                st.session_state.tasks.append(new_task)
                st.success("تمت إضافة المهمة بنجاح!")

st.subheader("📊 جدول المهام الحالية")

if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🗑️ مسح كافة المهام"):
            st.session_state.tasks = []
            st.rerun()
    with col_b:
        st.info("💡 للطباعة على ورق A4 أو التصدير PDF: اضغط (Ctrl + P) من المتصفح أو اختر طباعة من القائمة.")
else:
    st.info("لا توجد مهام مسجلة حالياً. استخدم النموذج أعلاه لإضافة مهام جديدة.")
