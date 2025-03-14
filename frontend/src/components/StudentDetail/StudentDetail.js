import React, { useEffect, useContext, useState } from "react";
import { AppContext } from "../../AppContext";
import "./StudentDetail.css";
import {
  FaCrown,
  FaCalendarAlt,
  FaListAlt,
  FaUserCircle,
} from "react-icons/fa";

const StudentDetail = ({ studentId }) => {
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
                  studentInfo.isMember ? "member" : "non-member"
                }`}
              >
                {studentInfo.isMember ? "Member" : "Non-member"}
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
            <div className="info-block badge-section">
              <div className="info-block-header">
                <FaListAlt className="info-icon" />
                <p>
                  <strong>Tags:</strong>{" "}
                </p>
              </div>
              <div className="badges">
                {studentInfo.tags.map((tag, index) => (
                  <div key={index} className="badge-icon">
                    <p>
                      <b>{tag.toUpperCase()}</b>
                    </p>
                  </div>
                ))}
              </div>
            </div>
            <div className="info-block badge-section">
              <div className="info-block-header">
                <FaCrown className="info-icon" />
                <p>
                  <strong>Trainings Completed:</strong>
                </p>
              </div>
              <div className="badges">
                {studentInfo.trainingsCompleted.map((badge, index) => (
                  <div key={index} className="badge-icon">
                    <img src={badge.image} height="72" width="72" />
                    <p>
                      <b>{badge.name}</b>
                    </p>
                  </div>
                ))}
              </div>
            </div>
            <div className="info-block badge-section">
              <div className="info-block-header">
                <FaCrown className="info-icon" />
                <p>
                  <strong>Unicorn Badges:</strong>
                </p>
              </div>
              <div className="badges">
                {studentInfo.unicornBadges.map((badge, index) => (
                  <div key={index} className="badge-icon">
                    <img src={badge.image} height="72" width="72" />
                    <p>
                      <b>{badge.name}</b>
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default StudentDetail;
