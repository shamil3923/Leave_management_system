from pydantic import BaseModel

class LeaveRequest(BaseModel):
    start_date: str  # Format: YYYY-MM-DD
    end_date: str  # Format: YYYY-MM-DD
    reason: str  # Add the 'reason' field
