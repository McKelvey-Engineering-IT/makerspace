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
  const { selectedStudent, membershipYear } = useContext(AppContext);

  useEffect(() => {
    const fetchStudentData = async () => {
      setStudentInfo(null);
      setError(null);

      try {
        const badgeapi = await fetch(
          `${process.env.REACT_APP_API_URL}/logins/retrieve_user?email=${selectedStudent}`
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
  }, [selectedStudent]);

  const handlePopupClose = () => {
    setError(null);
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
              <p
                className={`member-status ${
                  isMemberForYear(studentInfo.membershipYears, membershipYear) ? "member" : "non-member"
                }`}
              >
                {isMemberForYear(studentInfo.membershipYears, membershipYear) ? "Member" : "Non-member"}
              </p>
            </div>
            <div className="info-block badge-section">
              <div className="info-block-header">
                <FaCalendarAlt className="info-icon" />
                <p>
                  <strong>Last Sign In:</strong>{" "}
                </p>
              </div>
              <div className="badges">
                {new Date(studentInfo.LastSignIn).toLocaleString()}
              </div>
            </div>
            <InfoSection
              title="Trainings Completed"
              icon={FaListAlt}
              payload={studentInfo.trainingsCompleted || []}
              isImage={true}
            />
            <InfoSection
              title="Unicorn Badges"
              icon={FaCrown}
              payload={studentInfo.unicornBadges || []}
              isImage={true}
            />
            <InfoSection
              title="PowerTool Training"
              icon={FaTools}
              payload={studentInfo.powertoolTraining || []}
              isImage={true}
            />
            <InfoSection
              title="MakerTech Training"
              icon={FaTools}
              payload={studentInfo.makertechTraining || []}
              isImage={true}
              defaultCollapsed={true}
            />
          </div>
        )}
      </div>
    </>
  );
};

export default StudentDetail;
