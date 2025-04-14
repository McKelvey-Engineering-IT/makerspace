import React, { useEffect, useContext, useState } from "react";
import { AppContext } from "../../AppContext";
import "./StudentDetail.css";
import {
  FaCrown,
  FaCalendarAlt,
  FaListAlt,
  FaUserCircle,
  FaTools,
} from "react-icons/fa";
import InfoSection from "./InfoSection";
import { isMemberForYear } from '../../utils/membershipUtils';

const StudentDetail = () => {
  const [studentInfo, setStudentInfo] = useState(null);
  const [error, setError] = useState(null);
  const { selectedLog } = useContext(AppContext);

  useEffect(() => {
    const fetchStudentData = async () => {
      setStudentInfo(null);
      setError(null);

      try {
        const badgeapi = await fetch(
          `${process.env.REACT_APP_API_URL}/logins/retrieve_user?log_id=${selectedLog}`
        );

        if (!badgeapi.ok) {
          throw new Error(`Error ${badgeapi.status}: Unable to fetch student data`);
        }

        let badges = await badgeapi.json();
        badges.tags = ["Engineering", "Lab Access"];

        setStudentInfo(badges);
      } catch (err) {
        console.error("Failed to fetch student data:", err);
        setError("The record is corrupted. Please contact support.");
      }
    };

    fetchStudentData();
  }, [selectedLog]);

  const handlePopupClose = () => {
    setError(null);
  };

  const renderBadgeLevels = (badges) => {
    if (!badges || !badges.length) return null;
    
    return badges.map(level => (
      <InfoSection
        key={level.name}
        title={level.name}
        defaultCollapsed={!level.expanded}
        icon={FaTools}
        payload={level.badges || []}
        isImage={true}
        titleBarStyle={{
          backgroundColor: '#424242',
          color: level.color || '#FFFFFF'
        }}
      />
    ));
  };

  return (
    <>
      <div className="student-info-container">
        {error ? (
          <div className="error-popup">
            <p>{error}</p>
          </div>
        ) : !studentInfo ? (
          <div className="spinner"></div>
        ) : (
          <div className="student-info-card">
            <div className="header-section">
              <FaUserCircle className="user-icon" />
              <h2>{studentInfo.Name}</h2>
              <h3>{studentInfo.Email}</h3>
              <p className={`member-status ${studentInfo.membershipStatus.toLowerCase().replace(' ', '-')}`}>
                {studentInfo.membershipStatus}
              </p>
            </div>
            <div className="info-block badge-section">
              <div className="info-block-header">
                <FaCalendarAlt className="info-icon" />
                <h3>Sign In Information</h3>
              </div>
              <div className="sign-in-details">
                <div className="sign-in-entry">
                  <p><b>{new Date(studentInfo.SignInTime).toLocaleString()}</b></p>
                </div>
              </div>
            </div>
            {renderBadgeLevels(studentInfo.badges)}
          </div>
        )}
      </div>
    </>
  );
};

export default StudentDetail;
