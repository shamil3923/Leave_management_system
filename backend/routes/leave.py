from fastapi import APIRouter, Depends, HTTPException
from schemas.leave_request import LeaveRequest
from database import sqlite3
from utils.ai_decision import ai_leave_decision
from routes.auth import oauth2_scheme
import datetime
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

leave_router = APIRouter()
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'SECRET_KEY')

# Helper function to get user email from the token
def get_user_email(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@leave_router.post("/leave-request")
async def submit_leave_request(request: LeaveRequest, email: str = Depends(get_user_email)):
    # Connect to database
    conn = sqlite3.connect('userDB.db')
    cursor = conn.cursor()

    # Fetch user details from the database
    cursor.execute("SELECT id, leave_balance FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id, leave_balance = user

    # Calculate leave days based on start and end dates
    leave_days = (datetime.datetime.strptime(request.end_date, "%Y-%m-%d") - 
                  datetime.datetime.strptime(request.start_date, "%Y-%m-%d")).days + 1

    # Check if the user has enough leave balance
    if leave_days > leave_balance:
        raise HTTPException(status_code=400, detail="You can't take this amount of leave in your balance")

    # Get AI decision and explanation based on the request details (including reason)
    ai_decision, ai_explanation = ai_leave_decision(email, leave_days, leave_balance, request.reason)

    # Insert leave request into the database
    cursor.execute("INSERT INTO leave_requests (user_id, start_date, end_date, leave_days, ai_decision, ai_explanation, submit_date, reason) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (user_id, request.start_date, request.end_date, leave_days, ai_decision, ai_explanation, datetime.datetime.now(), request.reason))

    # If the AI decision is approved, update the leave balance
    if ai_decision == "Approved":
        cursor.execute("UPDATE users SET leave_balance = leave_balance - ? WHERE id = ?", (leave_days, user_id))

    conn.commit()
    conn.close()

    # Return the result with both decision and explanation
    return {"email": email, "status": ai_decision, "explanation": ai_explanation}

# @leave_router.get("/leave-status")
# async def check_leave_status(email: str = Depends(get_user_email)):
#     conn = sqlite3.connect('userDB.db')
#     cursor = conn.cursor()

#     cursor.execute("SELECT start_date, end_date, ai_decision, reason ,ai_explanation FROM leave_requests WHERE user_id = (SELECT id FROM users WHERE email = ?) ORDER BY submit_date DESC LIMIT 5", (email,))
#     requests = cursor.fetchall()
#     conn.close()


#     return {
#         "leave_requests": [
#             {
#                 "start_date": r[0],
#                 "end_date": r[1],
#                 "ai_decision": r[2],
#                 "reason": r[3],
#                 "ai_explanation" :r[4]
#                 } 
#             for r in requests
#         ]
#     }
@leave_router.get("/leave-status")
async def check_leave_status(email: str = Depends(get_user_email)):
    conn = sqlite3.connect('userDB.db')
    cursor = conn.cursor()

    cursor.execute("SELECT start_date, end_date, ai_decision, reason ,ai_explanation FROM leave_requests WHERE user_id = (SELECT id FROM users WHERE email = ?) ORDER BY submit_date DESC LIMIT 5", (email,))
    requests = cursor.fetchall()
    conn.close()

    return {
        "leave_requests": [
            {
                "start_date": r[0],
                "end_date": r[1],
                "status": r[2],
                "reason": r[3],
                "ai_explanation": r[4]
            } 
            for r in requests
        ]
    }
@leave_router.get("/leave-balance")
async def get_leave_balance(email: str = Depends(get_user_email)):
    conn = sqlite3.connect('userDB.db')
    cursor = conn.cursor()

    cursor.execute("SELECT leave_balance FROM users WHERE email = ?", (email,))
    balance = cursor.fetchone()
    conn.close()

    if balance:
        return {"email": email, "leave_balance": balance[0]}
    raise HTTPException(status_code=404, detail="User not found")
