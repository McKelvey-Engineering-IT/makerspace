import React, { useContext, useEffect, useRef } from "react";
import { AppContext } from "../../AppContext";
import { isMemberForYear } from '../../utils/membershipUtils';
import "./CheckInTable.css";

const CheckInTable = () => {
  const { 
    recordsInView, 
    selectedStudent, 
    setSelectedStudent, 
    newRecordsUnread, 
    soundAlertsEnabled, 
    membershipYear 
  } = useContext(AppContext);

  const audioRef = useRef(new Audio(process.env.PUBLIC_URL + "/alert.wav"));

  useEffect(() => {
      if (newRecordsUnread > 0 && soundAlertsEnabled) {
          audioRef.current.play().catch(err => console.log("Audio playback prevented:", err));
      }
  }, [newRecordsUnread, soundAlertsEnabled]);

  return (
    <div className="checkin-list">
      {recordsInView.map(({ LogID, Name, Email, membershipYears, SignInTime }) => (
        <div
          key={LogID}
          className={`checkin-card ${
            isMemberForYear(membershipYears, membershipYear) ? "member-card" : "nonmember-card"
          } ${newRecordsUnread.includes(LogID) ? "unread" : ""}
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
