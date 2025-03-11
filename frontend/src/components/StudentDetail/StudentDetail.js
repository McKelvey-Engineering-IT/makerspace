import React from "react";
import "./StudentDetail.css";
import { FaCrown, FaCalendarAlt, FaListAlt, FaUserCircle } from "react-icons/fa";
import useApi from "../../hooks/UseApi";

const StudentDetail = ({ studentId }) => {
 const { data: studentInfo, loading } = useApi({
   endpoint: `${process.env.REACT_APP_API_URL}/logins/retrieve_user?email=${studentId}`,
   method: "GET"
 });

 const enrichedStudentInfo = studentInfo 
   ? { ...studentInfo, tags: ["Engineering", "Lab Access"] } 
   : null;

 if (loading || !enrichedStudentInfo) {
   return <div className="spinner"></div>;
 }

 return (
   <div className="student-info-container">
     <div className="student-info-card">
       <div className="header-section">
         <FaUserCircle className="user-icon" />
         <h2>{enrichedStudentInfo.name}</h2>
         <h2>{enrichedStudentInfo.email}</h2>
         <p className={`member-status ${enrichedStudentInfo.isMember ? "member" : "non-member"}`}>
           {enrichedStudentInfo.isMember ? "Member" : "Non-member"}
         </p>
       </div>
       
       <div className="info-block badge-section">
         <div className="info-block-header">
           <FaCalendarAlt className="info-icon" />
           <p><strong>Last Sign In:</strong></p>
         </div>
         <div className="badges">
           {new Date(enrichedStudentInfo.LastSignIn).toLocaleString()}
         </div>
       </div>
       
       <div className="info-block badge-section">
         <div className="info-block-header">
           <FaListAlt className="info-icon" />
           <p><strong>Tags:</strong></p>
         </div>
         <div className="badges">
           {enrichedStudentInfo.tags.map((tag, index) => (
             <div key={index} className="badge-icon">
               <p><b>{tag.toUpperCase()}</b></p>
             </div>
           ))}
         </div>
       </div>
       
       <div className="info-block badge-section">
         <div className="info-block-header">
           <FaCrown className="info-icon" />
           <p><strong>Trainings Completed:</strong></p>
         </div>
         <div className="badges">
           {enrichedStudentInfo.trainingsCompleted.map((badge, index) => (
             <div key={index} className="badge-icon">
               <img src={badge.image} alt={badge.name} height="72" width="72" />
               <p><b>{badge.name}</b></p>
             </div>
           ))}
         </div>
       </div>
       
       <div className="info-block badge-section">
         <div className="info-block-header">
           <FaCrown className="info-icon" />
           <p><strong>Unicorn Badges:</strong></p>
         </div>
         <div className="badges">
           {enrichedStudentInfo.unicornBadges.map((badge, index) => (
             <div key={index} className="badge-icon">
               <img src={badge.image} alt={badge.name} height="72" width="72" />
               <p><b>{badge.name}</b></p>
             </div>
           ))}
         </div>
       </div>
     </div>
   </div>
 );
};

export default StudentDetail;