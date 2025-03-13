import React, { useContext } from "react";
import { AppContext } from "../../AppContext";
import "./CheckInTable.css";

const CheckInTable = () => {
  const { recordsInView, selectedStudent, setSelectedStudent } = useContext(AppContext);

  return (
    <div className="checkin-list">
      {recordsInView.map(({ id, Name, Email, IsMember, SignInTime }) => (
        <div
          key={id}
          className={`checkin-card ${IsMember ? "member-card" : "nonmember-card"} 
                      ${selectedStudent === Email ? "selected-row" : ""}`}
          onClick={() => setSelectedStudent(Email)}
        >
          <div className="checkin-info">
            <div className="info-top-row">
              <div className="checkin-name">{Name}</div>
              <div className="checkin-email">{Email}</div>
            </div>
            <div className="checkin-time">
              {SignInTime ? new Date(SignInTime).toLocaleString() : "N/A"}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default CheckInTable;
