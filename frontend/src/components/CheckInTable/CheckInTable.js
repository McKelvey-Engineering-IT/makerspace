import React from "react";
import "./CheckInTable.css"

const CheckInTable = ({ checkIns, onRowClick, studentId }) => {
  return (
    <div className="checkin-list">
      {checkIns.map(({ id, Name, Email, IsMember, SignInTime }) => (
        <div
          key={id}
          className={`checkin-card ${IsMember ? "member-card" : "nonmember-card"} 
                      ${studentId === Email ? "selected-row" : ""}`}
          onClick={() => onRowClick(Email)}
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
