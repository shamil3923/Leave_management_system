Leave Management System - Documentation

1. Project Overview
The Leave Management System is a web application that allows employees to submit leave requests, check leave balances, and track approval statuses. The system includes AI-powered decision-making using the Gemini API to assist in approving or rejecting leave requests.

2. Features
•User Authentication: Employees can sign up and log in using token authentication.
•Leave Request Submission: Employees can submit leave requests with reasons and upload medical reports if required.
•Leave Balance Verification: The system checks if the employee has sufficient leave days.
•AI-Powered Decision Making: Gemini API evaluates leave requests based on company policies.

3. Tech Stack
Frontend:
•React.js (UI Framework)
•Material-UI / Tailwind CSS (Styling)
•Axios (API Requests)

Backend:
•FastAPI (Python framework)
•SQLite (Database)
•Google Gemini API (AI-based leave approval)

4. Project Setup
Prerequisites
•Node.js and Yarn installed
•Python and FastAPI installed
•SQLite for the database

Frontend Setup
cd frontend
yarn install
yarn start

Backend Setup
cd backend
pip install -r requirements.txt
pip install PyJWT
pip install python-multipart
pip install google-generativeai
uvicorn main:app -–reload

5. AI-Powered Leave Approval
The AI assistant evaluates leave requests using Google Gemini API based on:
•Leave balance
•Validity of reason (e.g., medical emergencies are prioritized)
•Uploaded medical reports
•Company policies

6. Future Improvements
Enhanced Medical Report Submission and AI Decision-Making
