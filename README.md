# Payment Commitments API

מערכת לניהול התחייבויות תשלום דיגיטליות.

## התקנה והרצה

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Swagger UI: http://localhost:8000/docs

---

## State Machine

```
CREATED → SIGNED → SENT → ACCEPTED → REDEEMED
                              ↓
                           REJECTED
CREATED/SIGNED/ACCEPTED → CANCELED
```

---

## Flow מלא לדוגמה

### 1. יצירת התחייבות
```
POST /commitments
{
  "amount": 1500,
  "due_date": "2025-09-01",
  "creator_id": "user_a",
  "recipient_id": "user_b",
  "description": "שכר דירה אוגוסט"
}
```

### 2. חתימה (נועלת את הנתונים)
```
POST /commitments/{id}/sign?actor_id=user_a
```

### 3. שליחה לנמען
```
POST /commitments/{id}/send?actor_id=user_a
```

### 4. קבלה על ידי הנמען
```
POST /commitments/{id}/accept?actor_id=user_b
```

### 5. מימוש (לאחר תשלום בפועל)
```
POST /commitments/{id}/redeem?actor_id=user_a
```

### 6. Audit Trail
```
GET /commitments/{id}/audit
```

---

## Endpoints

| Method | Path | תיאור |
|--------|------|-------|
| POST | /commitments | יצירת התחייבות |
| GET | /commitments/{id} | קבלת התחייבות |
| GET | /commitments?user_id=&status= | רשימה עם פילטרים |
| POST | /commitments/{id}/sign | חתימה |
| POST | /commitments/{id}/send | שליחה |
| POST | /commitments/{id}/accept | קבלה |
| POST | /commitments/{id}/reject | דחייה |
| POST | /commitments/{id}/redeem | מימוש |
| POST | /commitments/{id}/cancel | ביטול |
| GET | /commitments/{id}/audit | היסטוריה מלאה |

---

## חתימה דיגיטלית

```
signature = SHA256(amount + due_date + creator_id + created_at)
```

נשמרת בעת SIGN ומקבעת את הנתונים — כל שינוי יפר את החתימה.
