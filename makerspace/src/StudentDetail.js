import React, { useEffect, useState } from 'react';
import './StudentDetail.css';
import { FaCrown, FaCalendarAlt, FaListAlt, FaStar, FaToolbox, FaWrench, FaLaptopCode } from 'react-icons/fa';

const StudentDetail = ({ studentId }) => {
  const [studentInfo, setStudentInfo] = useState(null);

  useEffect(() => {
    const fetchStudentData = async () => {
     
      const logUsersResponse = await fetch('https://makertech.engr.wustl.edu/server/api/log-users/');
      const logUsersData = await logUsersResponse.json();

      // Find the student by email
      const studentData = logUsersData.find((student) => student.email === studentId);

      if (!studentData) {
        console.error('Student not found in log-users');
        setStudentInfo(null);
        return;
      }

      // Fetch badge data 
      const badgeDataResponse = await fetch(`https://makertech.engr.wustl.edu/server/api/badge-data/${studentId}`);
      let badgeData;
      if (badgeDataResponse.ok) {
        badgeData = await badgeDataResponse.json();
      } else {
        // if student not in badge table
        console.warn(`Badge data not found for ${studentId}, defaulting isMember to false`);
        badgeData = { isMember: false };
      }

        const transformedData = {
          name: `${studentData.first_name || 'Unknown'} ${studentData.last_name || 'Unknown'}`,
          email: studentData.email,
          lastSignIn: studentData.login_time || 'Not Available',
          isMember: badgeData.isMember,

        //the following are still hardcoded yet - TODO
        tags: ['Engineering', 'Lab Access'],
        upcomingAppointments: ['OnceHub: 2024-09-25 10:00AM'],
        trainingsCompleted: [
          { name: 'Basic Lab Training', date: 'Sep 20, 2023' },
          { name: 'Advanced Robotics', date: 'Sep 20, 2023' },
        ],
        unicornBadges: [
          { badgeName: 'Creative Badge', icon: <FaStar /> },
          { badgeName: 'Engineering Badge', icon: <FaWrench /> },
          { badgeName: 'Coding Badge', icon: <FaLaptopCode /> },
          { badgeName: 'Builder Badge', icon: <FaToolbox /> },
        ],
      };
      setStudentInfo(transformedData);
    };
    fetchStudentData();
  }, [studentId]);

  if (!studentInfo) {
    return <p>Loading...</p>;
  }

  return (
    // student info
    <div className="student-info-container">
      <div className="student-info-card">
        <div className="header-section">
          {/* <FaUserCircle className="user-icon" /> */}
          <h2>{studentInfo.name}</h2>
          <h2>{studentInfo.email}</h2>
          <p className={`member-status ${studentInfo.isMember ? 'member' : 'non-member'}`}>
            {studentInfo.isMember ? 'Member' : 'Non-member'}
          </p>
        </div>
        <div className="info-block">
          <FaCalendarAlt className="info-icon" />
          <p><strong>Last Sign In:</strong> {new Date(studentInfo.lastSignIn).toLocaleString()}</p>
        </div>
        <div className="info-block">
          <FaListAlt className="info-icon" />
          <p><strong>Tags:</strong> {studentInfo.tags.join(', ')}</p>
        </div>
        {/* appointment section */}
        {/* <div className="info-block">
          <FaCalendarAlt className="info-icon" />
          <p><strong>Upcoming Appointments:</strong></p>
          <ul>
            {studentInfo.upcomingAppointments.map((appointment, index) => (
              <li key={index}>{appointment}</li>
            ))}
          </ul>
        </div> */}

        {/* Training */}
        <div className="info-block training-section">
          <FaListAlt className="info-icon" />
          <p><strong>All Training Completed:</strong></p>
          <div className="trainings">
            {studentInfo.trainingsCompleted.map((training, index) => (
              <div key={index} className="training-box">
                <p>{training.name}</p>
                {/* <p>Completed Time: {training.date}</p> */}
              </div>
            ))}
          </div>
        </div>

        {/* badgr */}
        <div className="info-block badge-section">
          <FaCrown className="info-icon" />
          <p><strong>Unicorn Badges:</strong></p>
          <div className="badges">
            {studentInfo.unicornBadges.map((badge, index) => (
              <div key={index} className="badge-icon">
                {badge.icon}
                <p>{badge.badgeName}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDetail;
