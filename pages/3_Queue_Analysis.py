from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="MediQueue AI | ניתוח התור",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ROOT = Path(__file__).resolve().parents[1]

# ---------- Style ----------
st.html("""
<style>
#MainMenu,footer,header[data-testid="stHeader"],section[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"]{display:none!important}
.stApp{background:#eef5f9}
.block-container{max-width:1450px!important;padding:20px 30px 45px!important}
.hero{direction:rtl;padding:28px 32px;border:1px solid #dceaf2;border-radius:20px;
background:linear-gradient(135deg,#fff,#f7fbfd 70%,#eaf7fb)}
.title{color:#07265f;font-size:36px;font-weight:900;margin:7px 0}
.subtitle{color:#5c7186;font-size:13px;line-height:1.8}
.sec{direction:rtl;color:#075e92;font-size:21px;font-weight:900;margin:26px 0 12px}
[data-testid="stMetric"]{min-height:108px;padding:14px 17px;border:1px solid #dce9f1;border-radius:15px;background:#fff}
[data-testid="stMetricValue"]{color:#075b94;font-weight:900}
.note{direction:rtl;padding:16px 18px;border:1px solid #d7edf3;border-radius:12px;
background:#eef9fc;color:#49687d;line-height:1.8;font-size:13px}
.note strong{color:#078fa5}
</style>
""")

# ---------- Header ----------
st.html("""
<div class="hero">
<div style="color:#0797aa;font-size:12px;font-weight:800">MediQueue AI</div>
<div class="title">ניתוח התור ומדדי ביצוע</div>
<div class="subtitle">
השלב השלישי במערכת: נתוני מטופלים ← ניהול התור ← <strong>ניתוח התור</strong> ← תמיכה בהחלטות.
העמוד מנתח את אותן תוצאות שחושבו בשלב הקודם, ללא יצירת מטופלים חדשים וללא שינוי סדר הטיפול.
</div></div>
""")

# ---------- Load Queue Management results ----------
if "mediqueue_queue_results" not in st.session_state:
    st.warning("לא נמצאו תוצאות. יש לעבור קודם לעמוד ניהול התור.")
    st.stop()

q = st.session_state["mediqueue_queue_results"]

df = q["results"].copy()
util = q["doctor_utilization"].copy()

n_patients = int(q["number_of_patients"])
n_doctors = int(q["number_of_doctors"])
avg_wait = float(q["avg_wait"])
median_wait = float(q["median_wait"])
max_wait = float(q["max_wait"])
waited = int(q["patients_waited"])
waited_pct = float(q["waited_percent"])
system_util = float(q["system_utilization"])
status = q["queue_status"]

avg_service = pd.to_numeric(
    df["זמן טיפול משוער (דקות)"],
    errors="coerce"
).mean()

# ---------- Summary ----------
st.markdown('<div class="sec">סיכום התרחיש</div>', unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
c1.metric("מספר מטופלים", n_patients)
c2.metric("מספר רופאים", n_doctors)
c3.metric("זמן המתנה ממוצע", f"{avg_wait:.1f} דקות")
c4.metric("ניצול משאבים", f"{system_util:.1f}%")

c1,c2,c3,c4 = st.columns(4)
c1.metric("זמן טיפול ממוצע", f"{avg_service:.1f} דקות")
c2.metric("חציון זמן המתנה", f"{median_wait:.1f} דקות")
c3.metric("זמן המתנה מקסימלי", f"{max_wait:.1f} דקות")
c4.metric("מטופלים שהמתינו", f"{waited} ({waited_pct:.1f}%)")

st.html("""
<div class="note">
<strong>הקשר לתורת התורים:</strong>
המטופלים הם הלקוחות והרופאים הם שרתי השירות.
המערכת משתמשת בזמני הגעה, זמני טיפול ורמות דחיפות.
זמן ההמתנה מחושב כתוצאה של ניהול התור.
עדיפות גבוהה קודמת, ובתוך אותה רמת דחיפות נשמר FCFS.
</div>
""")

# ---------- Waiting by patient ----------
st.markdown('<div class="sec">זמן המתנה לפי מטופל</div>', unsafe_allow_html=True)

plot_df = df.copy()
plot_df["_n"] = plot_df["מטופל"].astype(str).str.extract(r"(\d+)")[0].astype(int)
plot_df = plot_df.sort_values("_n")

fig = px.bar(
    plot_df,
    x="מטופל",
    y="זמן המתנה (דקות)",
    color="רמת דחיפות",
    text="זמן המתנה (דקות)",
    category_orders={
        "מטופל": plot_df["מטופל"].tolist(),
        "רמת דחיפות": ["גבוהה","בינונית","נמוכה"]
    },
    color_discrete_map={
        "גבוהה":"#e63946",
        "בינונית":"#457b9d",
        "נמוכה":"#2a9d8f"
    }
)

fig.update_traces(textposition="outside")
fig.update_layout(
    height=410,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="מטופל",
    yaxis_title="זמן המתנה (דקות)"
)
st.plotly_chart(fig, use_container_width=True)

# ---------- Analysis by urgency ----------
st.markdown('<div class="sec">ניתוח לפי רמת דחיפות</div>', unsafe_allow_html=True)

urg = (
    df.groupby("רמת דחיפות")
    .agg(**{
        "מספר מטופלים":("מטופל","count"),
        "זמן המתנה ממוצע":("זמן המתנה (דקות)","mean"),
        "זמן המתנה מקסימלי":("זמן המתנה (דקות)","max")
    })
    .reset_index()
)

urg["זמן המתנה ממוצע"] = urg["זמן המתנה ממוצע"].round(1)
urg["זמן המתנה מקסימלי"] = urg["זמן המתנה מקסימלי"].round(1)
urg["_o"] = urg["רמת דחיפות"].map({"גבוהה":1,"בינונית":2,"נמוכה":3})
urg = urg.sort_values("_o").drop(columns="_o")

st.dataframe(urg, use_container_width=True, hide_index=True)

# ---------- Doctor utilization ----------
st.markdown('<div class="sec">ניצול הרופאים</div>', unsafe_allow_html=True)

fig2 = px.bar(
    util,
    x="רופא",
    y="ניצול (%)",
    text="ניצול (%)"
)

fig2.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig2.update_layout(
    height=360,
    yaxis_range=[0,105],
    showlegend=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="רופא",
    yaxis_title="ניצול (%)"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------- Conclusion ----------
st.markdown('<div class="sec">מסקנת הניתוח</div>', unsafe_allow_html=True)

if status == "עומס גבוה":
    insight = "המערכת פועלת בעומס גבוה ולכן יש מקום לבחון תרחישים חלופיים של מספר רופאים."
elif status == "עומס בינוני":
    insight = "המערכת פועלת בעומס בינוני וקיים איזון סביר בין זמני ההמתנה לניצול הרופאים."
else:
    insight = "המערכת פועלת בעומס נמוך וקיימת קיבולת שירות פנויה."

st.html(f"""
<div class="note">
<strong>סיכום:</strong><br>
בתרחיש קיימים <strong>{n_patients} מטופלים</strong> ו-<strong>{n_doctors} רופאים</strong>.
זמן ההמתנה הממוצע הוא <strong>{avg_wait:.1f} דקות</strong>,
המקסימלי <strong>{max_wait:.1f} דקות</strong>,
וניצול המשאבים <strong>{system_util:.1f}%</strong>.<br><br>

<strong>{status}:</strong> {insight}<br><br>

בשלב הבא נבחן תרחישים חלופיים של מספר רופאים
ונשווה את זמני ההמתנה וניצול המשאבים,
תוך שימוש באותם מטופלים ובאותם נתוני קלט.
</div>
""")

# ---------- Save for Decision Support ----------
st.session_state["mediqueue_analysis"] = {
    "results": df.copy(),
    "number_of_patients": n_patients,
    "number_of_doctors": n_doctors,
    "avg_wait": avg_wait,
    "max_wait": max_wait,
    "system_utilization": system_util,
    "queue_status": status
}

# ---------- Navigation ----------
st.markdown('<div class="sec">המשך במערכת</div>', unsafe_allow_html=True)

b1,b2 = st.columns(2)

with b1:
    if st.button("חזרה לניהול התור", use_container_width=True):
        for p in ["pages/2_Queue_Management.py","pages/Queue_Management.py"]:
            if (ROOT/p).exists():
                st.switch_page(p)
                break

with b2:
    if st.button("המשך לתמיכה בהחלטות", type="primary", use_container_width=True):
        for p in ["pages/4_Decision_Support.py","pages/Decision_Support.py"]:
            if (ROOT/p).exists():
                st.switch_page(p)
                break