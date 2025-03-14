import React from "react";
import PropTypes from "prop-types";
import "./StudentDetail.css";

const InfoSection = ({ title, icon: Icon, payload, isImage }) => {
  return (
    <div className="info-block badge-section">
      <div className="info-block-header">
        <Icon className="info-icon" />
        <p>
          <strong>{title}:</strong>
        </p>
      </div>
      <div className="badges">
        {payload.map((item, index) => (
          <div key={index} className="badge-icon">
            {isImage ? (
              <>
                <img src={item.ImageURL} height="72" width="72" />
                <p>
                  <b>{item.Narrative_Detail}</b>
                </p>
              </>
            ) : (
              <p>
                <b>{item.toUpperCase()}</b>
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

InfoSection.propTypes = {
  title: PropTypes.string.isRequired,
  icon: PropTypes.elementType.isRequired,
  payload: PropTypes.array.isRequired,
  isImage: PropTypes.bool,
};

InfoSection.defaultProps = {
  isImage: false,
};

export default InfoSection;