import axios from 'axios';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TextareaAutosize } from '@mui/base';

function LeaveBalance() {
  const [leaveBalance, setLeaveBalance] = useState(null);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false); // To toggle the form visibility
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [reason, setReason] = useState('');
  const [leaveRequests, setLeaveRequests] = useState([]); // To hold the leave requests and their status
  const navigate = useNavigate();

  // Fetch leave balance and leave status on component load
  useEffect(() => {
    const fetchLeaveBalanceAndStatus = async () => {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        navigate('/');
        return;
      }

      try {
        // Fetch leave balance
        const balanceResponse = await axios.get('http://localhost:8000/leave-balance', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        setLeaveBalance(balanceResponse.data.leave_balance);

        // Fetch leave status
        const statusResponse = await axios.get('http://localhost:8000/leave-status', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        setLeaveRequests(statusResponse.data.leave_requests); // Set the leave requests data
      } catch (err) {
        setError('Failed to fetch data. Please try again.');
        console.error(err);
      }
    };

    fetchLeaveBalanceAndStatus();
  }, [navigate]);

  const handleFileUpload = async (e, requestId) => {
    const file = e.target.files[0];
    if (!file) return;
  
    const formData = new FormData();
    formData.append('document', file);
  
    const token = localStorage.getItem('auth_token');
    if (!token) {
      setError('No valid token found.');
      return;
    }
  
    try {
      await axios.post(`http://localhost:8000/leave-request/${requestId}/upload`, formData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
  
      alert('Document uploaded successfully!');
    } catch (err) {
      console.error('File upload failed:', err);
      alert('Failed to upload document. Please try again.');
    }
  };

  const handleSubmitLeaveRequest = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('auth_token');
    if (!token) {
      setError('No valid token found.');
      return;
    }

    const leaveRequest = {
      start_date: startDate,
      end_date: endDate,
      reason: reason,
    };

    try {
      const response = await axios.post('http://localhost:8000/leave-request', leaveRequest, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      // Show success message or update the UI as needed
      alert('Leave request submitted successfully!');
      setShowForm(false); // Hide form after submission

      // After submission, fetch updated leave requests status
      const statusResponse = await axios.get('http://localhost:8000/leave-status', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      setLeaveRequests(statusResponse.data.leave_requests); // Update leave requests status
    } catch (err) {
      if (err.response && err.response.status === 400) {
        setError(err.response.data.detail); // Display error message returned from the backend
      } else {
        setError('Failed to submit leave request. Please try again.');
      }
      console.error(err);
    }
  };

  return (
    <div className="leave-balance-container w-full p-6">
      <h2 className="text-3xl font-semibold text-gray-800">Your Leave Balance</h2>
      {error && <p className="text-red-500 mt-2">{error}</p>}
      
      {leaveBalance !== null ? (
        <p className="text-xl mt-4">You have <span className="font-bold">{leaveBalance} days</span> of leave remaining.</p>
      ) : (
        <p>Loading...</p>
      )}

      <button
        onClick={() => setShowForm(!showForm)} // Toggle form visibility
        className="mt-6 px-6 py-2 text-white bg-indigo-600 rounded-lg hover:bg-indigo-700"
      >
        Request Leave
      </button>

      {showForm && (
        <form 
          onSubmit={handleSubmitLeaveRequest} 
          className="mt-6 p-6 bg-white shadow-lg rounded-lg w-2/3 md:w-1/2"
        >
          {/* Flexbox for Start and End Date */}
          <div className="flex gap-4">
            {/* Start Date */}
            <div className="w-1/2">
              <label htmlFor="startDate" className="block text-gray-700 font-medium">Start Date</label>
              <input
                type="date"
                id="startDate"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                required
                className="w-full px-4 py-2 mt-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
              />
            </div>

            {/* End Date */}
            <div className="w-1/2">
              <label htmlFor="endDate" className="block text-gray-700 font-medium">End Date</label>
              <input
                type="date"
                id="endDate"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                required
                className="w-full px-4 py-2 mt-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
              />
            </div>
          </div>

          {/* Reason Field */}
          <div className="mt-4">
            <label htmlFor="reason" className="block text-gray-700 font-medium">Reason</label>
            <TextareaAutosize
              id="reason"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              required
              className="w-full px-4 py-2 mt-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
              minRows={4}
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full px-6 py-2 mt-4 text-white bg-indigo-600 rounded-lg hover:bg-indigo-700"
          >
            Submit Leave Request
          </button>
      </form>
      )}

      <div className="leave-requests mt-10 w-full">
        <h3 className="text-2xl font-semibold text-gray-800 mb-4">Leave Request Status</h3>
        {leaveRequests.map((request, index) => (
          <div key={index} className="bg-white p-8 shadow-lg rounded-lg border border-gray-300 w-full">
            <p><strong className="text-gray-600">Start Date:</strong> {request.start_date}</p>
            <p><strong className="text-gray-600">End Date:</strong> {request.end_date}</p>
            <p><strong className="text-gray-600">Reason:</strong> {request.reason}</p>
            <p>
              <strong className="text-gray-600">Status:</strong> 
              <span
                className={`${
                  request.status === 'Approved' ? 'text-green-500' :
                  request.status === 'Pending' ? 'text-yellow-500' : 'text-red-500'
                }`}
              >
                {request.status}
              </span>
            </p>
            <p><strong className="text-gray-600">AI Explanation:</strong></p>
            <div className="ai-explanation" style={{
              whiteSpace: "pre-line",
              padding: "10px",
              border: "1px solid #ccc",
              borderRadius: "5px",
              maxHeight: "200px",  // Adjust this value based on your layout
              overflowY: "auto",    // Enables vertical scrolling
            }}>
              {request.ai_explanation || 'No explanation available'}
            </div>

            {request.status === 'Pending' && (
              <div className="upload-support-docs mt-4">
                <label htmlFor={`fileUpload-${index}`} className="block text-gray-700 font-medium">
                  Upload Supporting Documents:
                </label>
                <input
                  type="file"
                  id={`fileUpload-${index}`}
                  accept=".pdf,.jpg,.png"
                  onChange={(e) => handleFileUpload(e, request.id)}
                  className="w-full mt-2"
                />
              </div>
            )}
          </div>
        ))}

      </div>
    </div>
  );
}

export default LeaveBalance;