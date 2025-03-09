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
            checkIn.isMember ? "member-card" : "nonmember-card"
          } ${studentId === checkIn.email ? "selected-row" : ""}`}
          onClick={() => handleClick(checkIn.email)}
        >
          <div className="checkin-info">
            <div className="info-top-row">
              <div className="checkin-name">{checkIn.name}</div>
              <div className="checkin-email">{checkIn.email}</div>
            </div>
            <div className="checkin-time">
              {new Date(checkIn.signInTime).toLocaleString()}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default CheckInTable;
