import React, { useState } from "react";
import PropTypes from "prop-types";
import "./InfoSection.css";

const InfoSection = ({ title, icon: Icon, payload, isImage, defaultCollapsed = false }) => {
  const [collapsed, setCollapsed] = useState(defaultCollapsed || payload.length === 0);
  
  // Sort payload alphabetically by Narrative_Detail
  const sortedPayload = [...payload].sort((a, b) => {
    const aText = a.Narrative_Detail || '';
    const bText = b.Narrative_Detail || '';
    return aText.localeCompare(bText);
  });

  return (
    <div className="info-section">
      <div className="info-section-header" onClick={() => setCollapsed(!collapsed)}>
        <Icon className="info-icon" />
        <p>{title} ({payload.length})</p>
        <button className="collapse-toggle">{collapsed ? "+" : "-"}</button>
      </div>
      {!collapsed && (
        <div className="info-section-content">
          {Array.isArray(sortedPayload) && sortedPayload.length > 0 ? (
            <div className="info-grid">
              {sortedPayload.map((item, index) =>
                isImage && item.ImageURL ? (
                  <div key={index} className="info-item badge-hover">
                    <div className="badge-wrapper">
                      <img 
                        src={item.ImageURL} 
                        alt={item.Narrative_Detail} 
                        height="64" 
                        width="64" 
                        className="badge-image"
                      />
                      <p className="badge-title">
                        <b>{item.Narrative_Detail}</b>
                      </p>
                    </div>
                  </div>
                ) : (
                  <div key={index} className="info-item text-hover">
                    <p>{item.Narrative_Detail || `Item ${index + 1}`}</p>
                  </div>
                )
              )}
            </div>
          ) : (
            <p>No data available</p>
          )}
        </div>
      )}
    </div>
  );
};

export default InfoSection;