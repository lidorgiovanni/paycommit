const slides = [];

// 1 — HERO
slides.push(`<div class="slide hero-slide">
  <div class="slide-number">01 / 08</div>
  <div class="logo-big">Pay<span>Commit</span></div>
  <h1>ההתחייבות הפיננסית<br/><span class="accent">של המאה ה-21</span></h1>
  <div class="divider"></div>
  <p class="sub">שכבת ניהול התחייבויות תשלום דיגיטליות — חכמה, מאובטחת, ומשולבת עם כל מערכת בנקאית קיימת</p>
</div>`);

// 2 — PROBLEM
slides.push(`<div class="slide">
  <div class="slide-number">02 / 08</div>
  <div class="tag">הבעיה</div>
  <h2 style="text-align:center;margin-bottom:40px">הצ'ק עדיין קיים ב-2025.<br/><span class="accent">למה?</span></h2>
  <div class="grid-3">
    <div class="card">
      <div style="font-size:2rem;margin-bottom:12px">📄</div>
      <h3>צ'ק נייר</h3>
      <p>מיושן, קל לזיוף, אין מעקב, אין סטטוסים, אין התראות</p>
    </div>
    <div class="card">
      <div style="font-size:2rem;margin-bottom:12px">⚡</div>
      <h3>ביט / העברה</h3>
      <p>מיידי בלבד — אין אפשרות להתחייב לתשלום עתידי</p>
    </div>
    <div class="card">
      <div style="font-size:2rem;margin-bottom:12px">📋</div>
      <h3>חוזה / הסכם</h3>
      <p>מסורבל, יקר, דורש עורך דין, לא דיגיטלי</p>
    </div>
  </div>
  <p style="margin-top:32px;font-size:1.1rem;text-align:center"><span class="accent">אין פתרון פשוט</span> להתחייבות תשלום עתידית, מחייבת, ודיגיטלית</p>
</div>`);

// 3 — SOLUTION
slides.push(`<div class="slide">
  <div class="slide-number">03 / 08</div>
  <div class="tag">הפתרון</div>
  <h2 style="text-align:center;margin-bottom:16px">PayCommit — <span class="accent">צ'ק חכם</span></h2>
  <p style="text-align:center;margin-bottom:48px">התחייבות תשלום דיגיטלית עם lifecycle מלא, חתימה, ומעקב</p>
  <div class="flow">
    <div class="flow-step"><div class="step-icon">✍️</div><div class="step-label">יצירה</div></div>
    <div class="flow-arrow">→</div>
    <div class="flow-step"><div class="step-icon">🔐</div><div class="step-label">חתימה</div></div>
    <div class="flow-arrow">→</div>
    <div class="flow-step"><div class="step-icon">📤</div><div class="step-label">שליחה</div></div>
    <div class="flow-arrow">→</div>
    <div class="flow-step"><div class="step-icon">✅</div><div class="step-label">קבלה</div></div>
    <div class="flow-arrow">→</div>
    <div class="flow-step" style="border-color:rgba(0,200,150,0.4)"><div class="step-icon">💰</div><div class="step-label" style="color:#00c896">מימוש</div></div>
  </div>
  <div class="grid-2" style="margin-top:40px;max-width:700px">
    <div class="card"><h3>🔐 חתימה דיגיטלית</h3><p>SHA256 על כל ההתחייבות — בלתי ניתנת לשינוי</p></div>
    <div class="card"><h3>📜 Audit Trail</h3><p>כל פעולה נשמרת — מי, מתי, מה</p></div>
  </div>
</div>`);

// 4 — FOR BANKS
slides.push(`<div class="slide">
  <div class="slide-number">04 / 08</div>
  <div class="tag">לבנקים</div>
  <h2 style="text-align:center;margin-bottom:40px">למה זה <span class="accent">מושלם לבנק</span>?</h2>
  <div class="grid-2" style="max-width:900px">
    <div class="card highlight">
      <div style="font-size:1.8rem;margin-bottom:12px">🏦</div>
      <h3>אין שינוי בתשתית</h3>
      <p>PayCommit יושב מעל המערכת הקיימת. הבנק ממשיך להזיז כסף — אנחנו מנהלים את ההתחייבות לפניו</p>
    </div>
    <div class="card highlight">
      <div style="font-size:1.8rem;margin-bottom:12px">📊</div>
      <h3>Context לכל תשלום</h3>
      <p>הבנק יודע שכסף זז, אבל לא יודע למה. PayCommit נותן את הסיבה</p>
    </div>
    <div class="card highlight">
      <div style="font-size:1.8rem;margin-bottom:12px">⚖️</div>
      <h3>ציות רגולטורי</h3>
      <p>Audit trail מלא, חתימה דיגיטלית, ותיעוד כל פעולה</p>
    </div>
    <div class="card highlight">
      <div style="font-size:1.8rem;margin-bottom:12px">💳</div>
      <h3>הזדמנות אשראי</h3>
      <p>התחייבות חתומה = בטוחה. הבנק יכול להציע מימון מראש</p>
    </div>
  </div>
</div>`);

// 5 — MARKET
slides.push(`<div class="slide">
  <div class="slide-number">05 / 08</div>
  <div class="tag">שוק</div>
  <h2 style="text-align:center;margin-bottom:48px">גודל <span class="accent">ההזדמנות</span></h2>
  <div class="grid-3" style="max-width:900px">
    <div class="card" style="text-align:center">
      <div class="big-stat">8M+</div>
      <p style="margin-top:8px">צ'קים בשנה בישראל בלבד</p>
    </div>
    <div class="card" style="text-align:center">
      <div class="big-stat green">$4.6B</div>
      <p style="margin-top:8px">שוק ה-B2B Payments בישראל</p>
    </div>
    <div class="card" style="text-align:center">
      <div class="big-stat">5</div>
      <p style="margin-top:8px">בנקים גדולים שמחפשים פתרון דיגיטלי</p>
    </div>
  </div>
  <p style="margin-top:40px;text-align:center;font-size:1rem">כל צ'ק שמוחלף ב-PayCommit = <span class="accent">עסקה שניתן לנהל, לעקוב, ולממן</span></p>
</div>`);

// 6 — TECH
slides.push(`<div class="slide">
  <div class="slide-number">06 / 08</div>
  <div class="tag">טכנולוגיה</div>
  <h2 style="text-align:center;margin-bottom:40px">ארכיטקטורה <span class="accent">מוכנה לסקייל</span></h2>
  <div class="grid-3" style="max-width:900px">
    <div class="card"><h3>🔄 State Machine</h3><p>כל מעבר סטטוס נבדק — אי אפשר לבצע פעולה לא חוקית</p></div>
    <div class="card"><h3>🔐 Digital Signature</h3><p>SHA256 על כל ההתחייבות — נועל את הנתונים בחתימה</p></div>
    <div class="card"><h3>📜 Audit Log</h3><p>כל פעולה מתועדת עם timestamp, actor, ו-status change</p></div>
    <div class="card"><h3>🔌 REST API</h3><p>Stateless, קל לאינטגרציה עם כל מערכת בנקאית קיימת</p></div>
    <div class="card"><h3>📧 OTP Auth</h3><p>אימות מייל מובנה — ניתן להחליף ל-SMS או Gov ID</p></div>
    <div class="card"><h3>🚀 Extensible</h3><p>מוכן לחיבור Blockchain, Gov Signature, ו-Open Banking</p></div>
  </div>
</div>`);

// 7 — ROADMAP
slides.push(`<div class="slide">
  <div class="slide-number">07 / 08</div>
  <div class="tag">רודמאפ</div>
  <h2 style="text-align:center;margin-bottom:40px">3 שלבים ל<span class="accent">שוק</span></h2>
  <div class="grid-3" style="max-width:900px">
    <div class="card highlight">
      <div style="color:#7c6fff;font-size:0.78rem;font-weight:700;margin-bottom:12px">שלב 1 — עכשיו</div>
      <h3>MVP</h3>
      <p style="margin-top:8px">API עובד, UI מוכן, חתימה דיגיטלית, Audit Trail</p>
    </div>
    <div class="card">
      <div style="color:#8890b0;font-size:0.78rem;font-weight:700;margin-bottom:12px">שלב 2 — Q3 2025</div>
      <h3>פיילוט בנקאי</h3>
      <p style="margin-top:8px">אינטגרציה עם בנק אחד, 100 לקוחות עסקיים, סנדבוקס בנק ישראל</p>
    </div>
    <div class="card">
      <div style="color:#8890b0;font-size:0.78rem;font-weight:700;margin-bottom:12px">שלב 3 — 2026</div>
      <h3>White Label</h3>
      <p style="margin-top:8px">מוצר White Label לבנקים, חיבור Open Banking, הרחבה לאירופה</p>
    </div>
  </div>
</div>`);

// 8 — CTA
slides.push(`<div class="slide cta-slide">
  <div class="slide-number">08 / 08</div>
  <div class="tag">הצעד הבא</div>
  <h1 style="text-align:center;margin-bottom:20px">בואו נבנה את<br/><span class="green">עתיד ההתחייבויות</span><br/>ביחד</h1>
  <div class="divider"></div>
  <p style="text-align:center;font-size:1.1rem;margin:24px 0 48px">MVP עובד · API מוכן · מוכן לפיילוט</p>
  <div class="grid-3" style="max-width:700px">
    <div class="card" style="text-align:center">
      <div style="font-size:1.5rem;margin-bottom:8px">🏦</div>
      <h3>פיילוט עם בנק</h3>
      <p style="font-size:0.82rem">3 חודשים, 100 משתמשים</p>
    </div>
    <div class="card" style="text-align:center">
      <div style="font-size:1.5rem;margin-bottom:8px">🏗️</div>
      <h3>סנדבוקס בנק ישראל</h3>
      <p style="font-size:0.82rem">רגולציה מהיום הראשון</p>
    </div>
    <div class="card" style="text-align:center">
      <div style="font-size:1.5rem;margin-bottom:8px">🤝</div>
      <h3>שיתוף פעולה</h3>
      <p style="font-size:0.82rem">White Label לבנקים</p>
    </div>
  </div>
</div>`);

document.getElementById('deck').innerHTML = slides.join('');
