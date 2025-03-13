import React, {useContext} from "react";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Chip from "@mui/material/Chip";
import NotificationsIcon from "@mui/icons-material/Notifications";
import { AppContext } from "../../AppContext";
import "./ResultsNavigator.css";

const ResultsNavigator = ({}) => {
  const {totalPages, recordsPerPage, setRecordsPerPage, newRecords, totalRecords, currentPage, setCurrentPage, recordsInView } = useContext(AppContext);
  const pageOptions = Array.from({ length: totalPages }, (_, i) => i + 1);

  const handleRecordsPerPageChange = (e) => {
    setRecordsPerPage(e.target.value);
  };

  const handlePageChange = (e) => {
    setCurrentPage(e.target.value);
  };

  return (
    <div className="records-info">
      <div className="pagination-controls">
        <div className="dropdowns">
          <FormControl variant="outlined" className="records-per-page">
            <InputLabel id="records-per-page-label">Results</InputLabel>
            <Select
              labelId="records-per-page-label"
              id="records-per-page"
              value={recordsPerPage}
              onChange={handleRecordsPerPageChange}
              label="Results"
              sx={{ height: 40, width: 75 }}
            >
              <MenuItem value={10}>10</MenuItem>
              <MenuItem value={20}>20</MenuItem>
              <MenuItem value={50}>50</MenuItem>
            </Select>
          </FormControl>
          {totalPages > 1 && (
            <FormControl variant="outlined" className="page-select-dropdown">
              <InputLabel id="page-select-label">Page</InputLabel>
              <Select
                labelId="page-select-label"
                id="page-select"
                value={currentPage}
                onChange={handlePageChange}
                label="Page"
                sx={{ height: 40, width: 75 }}
              >
                {pageOptions.map((page) => (
                  <MenuItem key={page} value={page}>
                    {page}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          )}
        </div>

        {newRecords.length > 0 && (
          <Chip
          icon={<NotificationsIcon />}
          label={`${newRecords.length} new login${newRecords.length > 1 ? "s" : ""}. Click to view`}
          onClick={() => alert("test")}
          color="primary"
          variant="outlined"
          className={`new-records-chip ${newRecords.length > 0 ? "pulse-animation" : ""}`}
        />
        )}

        <div className="records-count">
          Displaying {recordsInView.length} of {totalRecords.length} records
        </div>
      </div>
    </div>
  );
};

export default ResultsNavigator;
