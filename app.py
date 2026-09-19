import streamlit as st
import time

# إعدادات الصفحة
st.set_page_config(page_title="متابعة مهام المكتب الفني", layout="wide")

# محاذاة النص والاتجاه لليمين
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div[data-testid="stBlock"] { text-align: right; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #0e1117; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("📋 إدارة مهام المكتب الفني والمؤقت الزمني")

# تهيئة حالة المهام والعدادات
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "id": 101,
            "المشروع": "خلاط",
            "اسم المهمة": "تصميم",
            "القائم بالعمل": "م. سمير",
            "الجهة الطالبة": "الإنتاج",
            "الأولوية": "متوسط",
            "الوقت المخصص (دقيقة)": 30,
            "الوقت المتبقي (ثانية)": 30 * 60,
            "شغال": False
        }
    ]

# عرض قائمة المهام والمؤقت
for i, task in enumerate(st.session_state.tasks):
    with st.container():
        st.markdown(f"### 📌 كود {task['id']} - {task['اسم المهمة']} ({task['المشروع']})")
        
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        
        with col1:
            st.write(f"**القائم بالعمل:** {task['القائم بالعمل']}")
            st.write(f"**الجهة الطالبة:** {task['الجهة الطالبة']} | **الأولوية:** {task['الأولوية']}")
        
        with col2:
            # حساب الوقت المتبقي (دقائق : ثواني)
            mins, secs = divmod(task["الوقت المتبقي (ثانية)"], 60)
            timer_display = f"{mins:02d}:{secs:02d}"
            st.metric(label="⏱️ الوقت المتبقي", value=timer_display)
            
        with col3:
            # أزرار التشغيل والإيقاف المؤقت
            if not task["شغال"]:
                if st.button("▶️ بدء العداد", key=f"start_{i}"):
                    task["شغال"] = True
                    st.rerun()
            else:
                if st.button("⏸️ إيقاف مؤقت", key=f"stop_{i}"):
                    task["شغال"] = False
                    st.rerun()
                    
        with col4:
            if st.button("🔄 إعادة ضبط", key=f"reset_{i}"):
                task["الوقت المتبقي (ثانية)"] = task["الوقت المخصص (دقيقة)"] * 60
                task["شغال"] = False
                st.rerun()

        st.markdown("---")

    # تحديث العداد التنازلي ثانية بثانية إذا كان زر التشغيل مفعلاً
    if task["شغال"] and task["الوقت المتبقي (ثانية)"] > 0:
        time.sleep(1)
        task["الوقت المتبقي (ثانية)"] -= 1
        st.rerun()
