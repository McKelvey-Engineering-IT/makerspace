import React, { useContext, useEffect, useRef } from "react";
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { styled } from '@mui/material/styles';
import Chip from "@mui/material/Chip";
import NotificationsIcon from "@mui/icons-material/Notifications";
import { AppContext } from "../../AppContext";
import "./ResultsNavigator.css";

const StyledFormControl = styled(FormControl)(({ theme }) => ({
  '& .MuiOutlinedInput-root': {
    borderRadius: '8px',
    transition: 'all 0.2s ease',
    '&:hover': {
      backgroundColor: 'rgba(0, 0, 0, 0.01)',
    },
  },
  '& .MuiOutlinedInput-notchedOutline': {
    borderColor: 'rgba(0, 0, 0, 0.15)',
  },
  '& .MuiSelect-select': {
    padding: '10px 14px',
  },
  '& .MuiInputLabel-outlined': {
    transform: 'translate(14px, 12px) scale(1)',
  },
  '& .MuiInputLabel-outlined.MuiInputLabel-shrink': {
    transform: 'translate(14px, -6px) scale(0.75)',
  },
}));

const ResultsNavigator = () => {
  const {
    totalPages,
    recordsPerPage,
    setRecordsPerPage,
    newRecords,
    setNewRecords,
    totalRecords,
    setTotalRecords,
    currentPage,
    setCurrentPage,
    recordsInView,
    setSortType,
    setNewRecordsUnread,
    setTotalPages,
    sortedRecords,
    soundAlertsEnabled
  } = useContext(AppContext);

  const audioRef = useRef(new Audio(process.env.PUBLIC_URL + "/alert.wav"));

  useEffect(() => {
    if (newRecords.length > 0 && soundAlertsEnabled) {
      audioRef.current.play().catch(err => console.log('Audio playback prevented:', err));
    }
  }, [newRecords.length, soundAlertsEnabled]);

  const pageOptions = Array.from({ length: totalPages }, (_, i) => i + 1);

  const handleRecordsPerPageChange = (e) => {
    const newRecordsPerPage = e.target.value;
    setRecordsPerPage(newRecordsPerPage);

    const newTotalPages = Math.ceil(sortedRecords.length / newRecordsPerPage);
    setTotalPages(newTotalPages);

    if (currentPage > newTotalPages) {
      setCurrentPage(newTotalPages > 0 ? newTotalPages : 1);
    } else {
      setCurrentPage(currentPage);
    }
  };

  const handlePageChange = (e) => {
    setCurrentPage(e.target.value);
  };

  const handleChipClick = () => {
    setNewRecordsUnread(() => newRecords.map((record) => record.LogID));
    setTotalRecords((prevTotalRecords) => [...newRecords, ...prevTotalRecords]);
    setSortType("lastSignIn"); 
    setNewRecords([]);
    setCurrentPage(1);
  };

  return (
    <div className="records-info">
      <div className="pagination-controls">
        <div className="dropdowns">
          <StyledFormControl>
            <InputLabel id="records-per-page-label">Results</InputLabel>
            <Select
              labelId="records-per-page-label"
              id="records-per-page"
              value={recordsPerPage}
              onChange={handleRecordsPerPageChange}
              label="Results"
              sx={{ minWidth: 100 }}
            >
              <MenuItem value={10}>10</MenuItem>
              <MenuItem value={20}>20</MenuItem>
              <MenuItem value={50}>50</MenuItem>
            </Select>
          </StyledFormControl>

          {totalPages > 1 && (
            <StyledFormControl>
              <InputLabel id="page-select-label">Page</InputLabel>
              <Select
                labelId="page-select-label"
                id="page-select"
                value={currentPage}
                onChange={handlePageChange}
                label="Page"
                sx={{ minWidth: 100 }}
              >
                {pageOptions.map((page) => (
                  <MenuItem key={page} value={page}>
                    {page}
                  </MenuItem>
                ))}
              </Select>
            </StyledFormControl>
          )}
        </div>

        {newRecords.length > 0 && (
          <Chip
            icon={<NotificationsIcon />}
            label={`${newRecords.length} new login${
              newRecords.length > 1 ? "s" : ""
            }. Click to view`}
            onClick={handleChipClick}
            color="primary"
            variant="outlined"
            className={`new-records-chip ${
              newRecords.length > 0 ? "pulse-animation" : ""
            }`}
          />
        )}

        <div className="records-count">
          Displaying {recordsInView.length} of {sortedRecords.length || totalRecords.length} records
        </div>
      </div>
    </div>
  );
};

export default ResultsNavigator;