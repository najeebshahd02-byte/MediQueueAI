from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="MediQueue AI | אודות המערכת",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ROOT = Path(__file__).resolve().parents[1]

st.html("""
<style>
#MainMenu,footer,header[data-testid="stHeader"],section[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"]{display:none!important}

.stApp{
    background:
      radial-gradient(circle at 90% 5%,rgba(22,165,183,.10),transparent 24%),
      linear-gradient(180deg,#f6fbfd 0%,#edf5f9 100%);
}
.block-container{max-width:1450px!important;padding:24px 34px 55px!important;direction:rtl!important}
.block-container p,.block-container span,.block-container b,.block-container small,
.block-container h1,.block-container h2,.block-container h3,.block-container div{
    text-align:right;
}


/* HERO */
.hero{
    direction:rtl; text-align:right; position:relative; overflow:hidden;
    min-height:255px; padding:42px 46px;
    border:1px solid #d7e8ef; border-radius:28px;
    background:linear-gradient(120deg,#ffffff 0%,#f6fcfe 58%,#e4f6fa 100%);
    box-shadow:0 14px 38px rgba(16,65,95,.08);
}
.hero:after{
    content:""; position:absolute; width:320px;height:320px;border-radius:50%;
    left:-80px;top:-120px;background:rgba(8,151,170,.08);
}
.brand{color:#0797aa;font-size:13px;font-weight:900;letter-spacing:.5px}
.hero h1{color:#082d68;font-size:46px;line-height:1.1;margin:12px 0 13px;font-weight:950}
.hero p{color:#5e7487;font-size:15px;line-height:2;max-width:900px;margin:0 0 0 auto;text-align:right}
.hero-tag{
    display:block;width:max-content;margin:20px 0 0 auto;padding:8px 15px;border-radius:30px;
    background:#e8f7fa;color:#087f96;font-size:12px;font-weight:850
}

/* TITLES */
.sec{direction:rtl;color:#075f91;font-size:23px;font-weight:950;margin:34px 0 15px}

/* OVERVIEW */
.overview{
    direction:rtl;display:grid;grid-template-columns:1.25fr .75fr;gap:18px
}
.panel{
    direction:rtl;text-align:right;background:#fff;border:1px solid #dce9ef;border-radius:20px;padding:25px 27px;
    box-shadow:0 5px 18px rgba(15,61,90,.035)
}
.panel h3{margin:0 0 12px;color:#10366c;font-size:19px}
.panel p{margin:0;color:#607587;font-size:13px;line-height:2}
.io{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.io-card{direction:rtl;text-align:right;background:#f7fbfd;border:1px solid #e1edf2;border-radius:15px;padding:16px}
.io-card b{display:block;color:#087f96;margin-bottom:9px;font-size:13px}
.io-card span{color:#667b8c;font-size:12px;line-height:1.9}

/* FLOW */
.flow{direction:rtl;display:grid;grid-template-columns:repeat(5,1fr);gap:13px}
.step{
    direction:rtl;text-align:right;position:relative;background:#fff;border:1px solid #dce9ef;border-radius:19px;
    padding:21px 17px 19px;min-height:155px;box-shadow:0 5px 18px rgba(15,61,90,.035)
}
.num{
    width:34px;height:34px;border-radius:11px;background:#e8f7fa;color:#07849a;
    display:flex;align-items:center;justify-content:center;font-weight:950;margin-bottom:15px
}
.step b{display:block;color:#10366c;font-size:14px;margin-bottom:8px}
.step span{color:#718494;font-size:11.5px;line-height:1.75}

/* ALGORITHM */
.algo{
    direction:rtl;display:grid;grid-template-columns:repeat(4,1fr);gap:14px
}
.algo-card{
    direction:rtl;text-align:right;background:#fff;border:1px solid #dce9ef;border-radius:18px;padding:20px;
    border-top:4px solid #1498aa
}
.algo-card small{color:#0797aa;font-weight:900}
.algo-card b{display:block;color:#10366c;font-size:16px;margin:8px 0}
.algo-card span{color:#6b8091;font-size:12px;line-height:1.75}

/* LIMIT */
.limit{
    direction:rtl;background:linear-gradient(120deg,#ffffff,#f1fafc);
    border:1px solid #d6e9ef;border-radius:20px;padding:24px 27px;
    color:#5a7183;font-size:13px;line-height:2
}
.limit strong{color:#087f96}

/* TEAM */
.team{direction:rtl;display:grid;grid-template-columns:repeat(5,1fr);gap:13px}
.person{
    direction:rtl;background:#fff;border:1px solid #dce9ef;border-radius:17px;padding:19px 12px;
    text-align:center!important;color:#10366c;font-size:13px;font-weight:900;
    box-shadow:0 4px 15px rgba(15,61,90,.03)
}
.person:before{
    content:"";display:block;width:34px;height:4px;border-radius:5px;
    background:#1498aa;margin:0 auto 12px
}

/* BUTTONS */
.stButton button{height:49px;border-radius:13px;font-weight:850}

@media(max-width:950px){
 .overview{grid-template-columns:1fr}
 .flow,.team{grid-template-columns:1fr 1fr}
 .algo{grid-template-columns:1fr 1fr}
}
</style>
""")

# ---------------- HERO ----------------
st.html("""
<div class="hero">
    <div class="brand">MediQueue AI</div>
    <h1>ניהול תורים חכם.<br>החלטות טובות יותר.</h1>
    <p>
        מערכת מידע גנרית לניהול תורים במרפאות ובבתי חולים,
        המשלבת זמני הגעה, זמני טיפול ורמות דחיפות כדי לנהל את סדר הטיפול,
        לחשב זמני המתנה, לחלק מטופלים בין רופאים ולנתח את ניצול המשאבים.
    </p>
    <div class="hero-tag">Queueing Theory · Priority Queue · Decision Support</div>
</div>
""")

# ---------------- OVERVIEW ----------------
st.markdown('<div class="sec">מהי MediQueue AI?</div>', unsafe_allow_html=True)

st.html("""
<div class="overview">
  <div class="panel">
    <h3>המטרה</h3>
    <p>
      MediQueue AI נועדה להתמודד עם זמני המתנה ארוכים הנוצרים כאשר חלוקת המטופלים
      בין הרופאים אינה יעילה. המערכת מנהלת את התור באופן דינמי על בסיס נתוני התרחיש,
      ומציגה מידע תפעולי שמאפשר להבין את מצב התור ולבחון חלופות ניהוליות.
    </p>
  </div>

  <div class="panel">
    <div class="io">
      <div class="io-card">
        <b>קלט למערכת</b>
        <span>מספר מטופלים<br>מספר רופאים<br>זמן הגעה<br>זמן טיפול<br>רמת דחיפות</span>
      </div>
      <div class="io-card">
        <b>פלט מהמערכת</b>
        <span>סדר טיפול<br>זמן המתנה<br>הקצאה לרופאים<br>ניצול משאבים<br>מדדי ביצוע</span>
      </div>
    </div>
  </div>
</div>
""")

# ---------------- FLOW ----------------
st.markdown('<div class="sec">איך המערכת עובדת?</div>', unsafe_allow_html=True)

st.html("""
<div class="flow">
 <div class="step"><div class="num">1</div><b>נתוני מטופלים</b><span>הגדרת מספר הרופאים והמטופלים, זמני הגעה, זמני טיפול ורמות דחיפות.</span></div>
 <div class="step"><div class="num">2</div><b>ניהול התור</b><span>קביעת סדר הטיפול, הקצאת המטופלים לרופאים וחישוב זמני ההמתנה.</span></div>
 <div class="step"><div class="num">3</div><b>ניתוח התור</b><span>ניתוח זמני ההמתנה, העומס וניצול המשאבים על בסיס תוצאות התור.</span></div>
 <div class="step"><div class="num">4</div><b>תמיכה בהחלטות</b><span>השוואת חלופות במספר הרופאים תוך שמירה על אותם נתוני מטופלים.</span></div>
 <div class="step"><div class="num">5</div><b>הערכת המערכת</b><span>בדיקות תקינות, איכות הפתרון ומהירות הפעלת מנגנון ניהול התור.</span></div>
</div>
""")

# ---------------- ALGORITHM ----------------
st.markdown('<div class="sec">הלוגיקה שמאחורי המערכת</div>', unsafe_allow_html=True)

st.html("""
<div class="algo">
 <div class="algo-card"><small>01</small><b>תורת התורים</b><span>המטופלים הם הלקוחות בתור והרופאים הם שרתי השירות.</span></div>
 <div class="algo-card"><small>02</small><b>Priority Queue</b><span>מטופל שכבר הגיע ובעל רמת דחיפות גבוהה יותר מקבל קדימות.</span></div>
 <div class="algo-card"><small>03</small><b>FCFS</b><span>בתוך אותה רמת דחיפות, המטופל שהגיע קודם מקבל שירות קודם.</span></div>
 <div class="algo-card"><small>04</small><b>פתרון היוריסטי</b><span>המערכת מספקת פתרון ישים ומהיר, ללא הבטחה לאופטימום גלובלי.</span></div>
</div>
""")

# ---------------- LIMITATIONS ----------------
st.markdown('<div class="sec">גבולות המערכת</div>', unsafe_allow_html=True)

st.html("""
<div class="limit">
    MediQueue AI פותחה כ<strong>אב-טיפוס אקדמי</strong>.
    המערכת פועלת על נתוני תרחיש ואינה מחוברת למערכת רפואית אמיתית.
    בשלב הנוכחי השוואת החלופות מתמקדת במספר הרופאים ואינה כוללת
    עלויות כוח אדם, משמרות או אילוצים רפואיים נוספים.
    לכן המערכת נועדה <strong>לתמוך בהחלטה ניהולית</strong> ולא להחליף שיקול דעת מקצועי.
</div>
""")

# ---------------- TEAM ----------------
st.markdown('<div class="sec">צוות הפרויקט</div>', unsafe_allow_html=True)

st.html("""
<div class="team">
 <div class="person">שהד אבו נגיב</div>
 <div class="person">שהד רמלאוי</div>
 <div class="person">פאטמה אבו גוש</div>
 <div class="person">ביאן אבו דאוד</div>
 <div class="person">מגד עווידה</div>
</div>
""")

# ---------------- NAV ----------------
st.markdown('<div class="sec">ניווט</div>', unsafe_allow_html=True)
left, right = st.columns(2)

with left:
    if st.button("חזרה להערכת המערכת", use_container_width=True):
        st.switch_page("pages/5_System_Evaluation.py")

with right:
    if st.button("חזרה לדף הבית", type="primary", use_container_width=True):
        for page in ["Home.py", "app.py", "pages/0_Home.py", "pages/Home.py"]:
            if (ROOT / page).exists():
                st.switch_page(page)
                break
        else:
            st.info("לא נמצא דף הבית בנתיב הצפוי.")