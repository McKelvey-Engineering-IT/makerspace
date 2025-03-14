import React, { useEffect, useContext, useState } from "react";
import { AppContext } from "../../AppContext";
import "./StudentDetail.css";
import {
  FaCrown,
  FaCalendarAlt,
  FaListAlt,
  FaUserCircle,
} from "react-icons/fa";
import InfoSection from "./InfoSection";

const StudentDetail = () => {
  const [studentInfo, setStudentInfo] = useState(null);
  const { selectedStudent } = useContext(AppContext);

  useEffect(() => {
    const fetchStudentData = async () => {
      setStudentInfo(null);

      const badgeapi = await fetch(
        `${process.env.REACT_APP_API_URL}/logins/retrieve_user?email=${selectedStudent}`
      );
      
      let badges = await badgeapi.json();
      badges.tags = ["Engineering", "Lab Access"];

      setStudentInfo(badges);
    };
    fetchStudentData();
  }, [selectedStudent]);

  return (
    <>
      <div className="student-info-container">
        {!studentInfo ? (
          <div className="spinner"></div>
        ) : (
          <div className="student-info-card">
            <div className="header-section">
              <FaUserCircle className="user-icon" />
              <h2>{studentInfo.Name}</h2>
              <h3>{studentInfo.Email}</h3>
              <p
                className={`member-status ${
                  studentInfo.IsMember ? "member" : "non-member"
                }`}
              >
                {studentInfo.IsMember ? "Member" : "Non-member"}
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
              icon={FaCrown}
              payload={studentInfo.trainingsCompleted}
              isImage
            />
            <InfoSection
              title="Unicorn Badges"
              icon={FaCrown}
              payload={studentInfo.unicornBadges}
              isImage
            />
          </div>
        )}
      </div>
    </>
  );
};

export default StudentDetail;
