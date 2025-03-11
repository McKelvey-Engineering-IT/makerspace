import React, { useState } from "react";
import "./CheckInTable.css";

const CheckInTable = ({ checkIns, onRowClick, studentId }) => {
  const [selectedId, setSelectedId] = useState(null);

  const handleClick = (studentId) => {
    setSelectedId(studentId);
    onRowClick(studentId);
  };

  return (
    //check in table
    <div className="checkin-list">
      {checkIns.map((checkIn) => (
        <div
          key={checkIn.id}
          className={`checkin-card ${
            checkIn.IsMember ? "member-card" : "nonmember-card"
          } ${studentId === checkIn.Email ? "selected-row" : ""}`}
          onClick={() => handleClick(checkIn.Email)}
        >
          <div className="checkin-info">
            <div className="info-top-row">
              <div className="checkin-name">{checkIn.Name}</div>
              <div className="checkin-email">{checkIn.Email}</div>
            </div>
            <div className="checkin-time">
              {new Date(checkIn.SignInTime).toLocaleString()}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default CheckInTable;
