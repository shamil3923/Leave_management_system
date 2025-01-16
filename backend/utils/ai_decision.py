import os
import google.generativeai as genai

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def ai_leave_decision(username: str, leave_days: int, current_balance: int, reason: str):
    """
    Determines whether the leave request should be Approved, Pending, or Rejected using Gemini AI.
    """
    # prompt = (
    #         f"You are an HR assistant. Employee {username} has {current_balance} leave days remaining. "
    #         f"The employee is requesting {leave_days} days off. The reason provided for the leave is: {reason}. "
    #         f"Based on this information, should the leave request be Approved, Pending, or Rejected?Your answer should return like, Approved, Rejected, Pending "
    #         f"Consider the employee's leave balance, the validity of the reason (such as medical emergencies, personal reasons, etc.), "
    #         f"Non-critical reasons like social events, or personal leisure should  be minimum 2 days, more than that should be rejected. "
    #         f"and the company policies for leave approval. Please provide a clear decision and the reasoning behind your decision."
    #     )

    prompt = (
            f"Hello {username}, you currently have {current_balance} leave days remaining. "
            f"You have requested {leave_days} days off for the following reason: {reason}. "
            f"After considering your leave balance, the reason for your request, and company policies: "
            f"Requests for medical emergencies or personal reasons are evaluated with priority. "
            f"For non-critical reasons like social events or personal leisure, a maximum of 2 days can be approved; "
            f"requests exceeding this will be declined. Based on these factors, your leave request is: Approved, Rejected, or Pending. Don't add any symbols to these words "
            f"Here is the decision and the reasoning behind it:"
        )
    try:
        # Create a GenerativeModel object and call generate_content
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        # Extract AI-generated decision and explanation
        content = response.text
        decision, explanation = content.split("\n", 1)  # Assuming the response separates decision and explanation
        return decision.strip(), explanation.strip()

    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return "Pending Review", "AI decision is pending due to an error."