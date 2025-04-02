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
    <div className="info-block badge-section">
      <div className="info-section-header" onClick={() => setCollapsed(!collapsed)}>
        <Icon className="info-icon" />
        <p>{title} ({payload.length})</p>
        <button className="collapse-toggle">{collapsed ? "+" : "-"}</button>
      </div>
      {!collapsed && (
        <div className="badges">
          {sortedPayload.map((item, index) => (
            <div key={index} className="badge-container">
              <div className="badge-text-static">
              {isImage && (
                  <img 
                    src={item.ImageURL} 
                    alt={item.Narrative_Title}
                    className="badge-image"
                  />
                )}
                <div className="badge-description">{item.Narrative_Detail}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default InfoSection;