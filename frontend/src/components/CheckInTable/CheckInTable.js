import React, { useContext, useEffect, useRef } from "react";
import { AppContext } from "../../AppContext";
import "./CheckInTable.css";

const CheckInTable = () => {
  const { 
    recordsInView, 
    selectedLog, 
    setSelectedLog, 
    newRecordsUnread, 
    soundAlertsEnabled 
  } = useContext(AppContext);

  const audioRef = useRef(new Audio(process.env.PUBLIC_URL + "/alert.wav"));

  useEffect(() => {
    if (recordsInView.length > 0 && !selectedLog) {
      setSelectedLog(recordsInView[0].LogID);
    }
  }, [recordsInView, selectedLog, setSelectedLog]); // Run when records or selection changes

  useEffect(() => {
      if (newRecordsUnread > 0 && soundAlertsEnabled) {
          audioRef.current.play().catch(err => console.log("Audio playback prevented:", err));
      }
  }, [newRecordsUnread, soundAlertsEnabled]);

  return (
    <div className="checkin-list">
      {recordsInView.map(({ LogID, Name, Email, membershipStatus, SignInTime }) => (
        <div
          key={LogID}
          className={`checkin-card ${membershipStatus.toLowerCase().replace(' ', '-')}-card
          ${newRecordsUnread.includes(LogID) ? "unread" : ""}
          ${selectedLog === LogID ? "selected-row" : ""}`}
          onClick={() => setSelectedLog(LogID)}
        >
          <div className="checkin-info">
            <div className="info-top-row">
              <div className="checkin-name">{Name}</div>
              <div className="checkin-email">{Email}</div>
              <div className={`status-badge ${membershipStatus.toLowerCase().replace(' ', '-')}`}>
                {membershipStatus}
              </div>
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
