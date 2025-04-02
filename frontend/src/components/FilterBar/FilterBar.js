import React, { useState, useContext, useEffect } from "react";
import { AppContext } from "../../AppContext";
import ResultsNavigator from "../ResultsNavigator/ResultsNavigator";
import "./FilterBar.css";
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { styled } from '@mui/material/styles';

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
  width: '180px',  // Increased from minWidth: 140
  margin: '0 10px',  // Add some spacing between dropdowns
  '& .MuiSelect-select': {
    padding: '10px 14px',
  },
}));

const FilterBar = () => {
  const {
    filter,
    setFilter,
    sortType,
    setSortType,
    setRecordsInView,
    totalRecords,
    setCurrentPage,
    sortedRecords,
    setSortedRecords,
    currentPage,
    recordsPerPage,
    setTotalPages, 
    recordsInView,
    membershipYear,
    setMembershipYear
  } = useContext(AppContext);

  const [searchTerm, setSearchTerm] = useState("");

  const currentYear = new Date().getFullYear();
  const years = Array.from(
    { length: 3 },
    (_, i) => String(currentYear - 2 + i) 
  );

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
    setCurrentPage(1);
  };

  const handleSortChange = (event) => {
    setSortType(event.target.value);
    setCurrentPage(1);
  };

  const handleFilterChange = (event) => {
    setFilter(event.target.value);
    setCurrentPage(1);
  };

  const handleYearChange = (event) => {
    setMembershipYear(event.target.value);
  };

  useEffect(() => {
    console.log("Processing records, totalRecords:", totalRecords?.length);

    if (!totalRecords || totalRecords.length === 0) {
      console.log("No records to process");
      setSortedRecords([]);
      return;
    }
    
    // First apply time-based filtering
    const now = new Date();
    let processedRecords = totalRecords.filter((record) => {
      const signInTime = new Date(record.SignInTime);
      if (filter === "day") {
        return now - signInTime <= 24 * 60 * 60 * 1000;
      } else if (filter === "week") {
        return now - signInTime <= 7 * 24 * 60 * 60 * 1000;
      } else if (filter === "month") {
        return now - signInTime <= 30 * 24 * 60 * 60 * 1000;
      } else {
        return true;
      }
    });
    
    console.log("After filtering by time:", processedRecords.length);
    
    // Apply search term filter
    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase();
      processedRecords = processedRecords.filter(
        (record) =>
          record.Name?.toLowerCase().includes(term) ||
          record.Email?.toLowerCase().includes(term)
      );
      console.log("After search:", processedRecords.length);
    }
    
    // Apply sorting
    processedRecords.sort((a, b) => {
      if (sortType === "lastSignIn") {
        return new Date(b.SignInTime) - new Date(a.SignInTime);
      } else if (sortType === "name") {
        return a.Name?.localeCompare(b.Name || "");
      } else if (sortType === "studentId") {
        return a.Email?.localeCompare(b.Email || "");
      }
      return 0;
    });
    console.log("hereeeeeeee");
    console.log("Final processed records:", processedRecords.length);
    setSortedRecords(processedRecords);
  }, [totalRecords, filter, searchTerm, sortType]);

  // Handle pagination separately
  useEffect(() => {
    if (!sortedRecords || sortedRecords.length === 0) {
      setRecordsInView([]);
      setTotalPages(1);
      return;
    }
    console.log('herrrreerrererere 134353')
    console.log(sortedRecords)
    // Calculate total pages
    const calculatedTotalPages = Math.ceil(sortedRecords.length / recordsPerPage);
    setTotalPages(calculatedTotalPages);
    
    // Ensure current page is valid
    if (currentPage > calculatedTotalPages && calculatedTotalPages > 0) {
      setCurrentPage(calculatedTotalPages);
      return; // Let the next effect cycle handle the pagination
    }

    // Apply pagination
    const startIndex = (currentPage - 1) * recordsPerPage;
    const endIndex = startIndex + recordsPerPage;
    const paginatedRecords = sortedRecords.slice(startIndex, endIndex);
    
    setRecordsInView(paginatedRecords);
    console.log(recordsInView)
    console.log(`Showing records ${startIndex + 1}-${Math.min(endIndex, sortedRecords.length)} of ${sortedRecords.length}`);
  }, [currentPage, sortedRecords, setCurrentPage, recordsPerPage]);

  return (
    <div className="filter-bar">
      <div className="filter-bar-content">
        <div className="top-controls">
          <input
            type="text"
            className="search-box"
            placeholder="Search name/email..."
            value={searchTerm}
            onChange={handleSearchChange}
          />
        </div>
        <div className="dropdown-container">
          <StyledFormControl>
            <InputLabel id="sort-label">Sort by</InputLabel>
            <Select
              labelId="sort-label"
              id="sort-dropdown"
              value={sortType}
              onChange={handleSortChange}
              label="Sort by"
            >
              <MenuItem value="lastSignIn">Last Sign In</MenuItem>
              <MenuItem value="name">Name</MenuItem>
              <MenuItem value="studentId">Email</MenuItem>
            </Select>
          </StyledFormControl>
          
          <StyledFormControl>
            <InputLabel id="time-label">Time Period</InputLabel>
            <Select
              labelId="time-label"
              id="time-dropdown"
              value={filter}
              onChange={handleFilterChange}
              label="Time Period"
            >
              <MenuItem value="day">Last Day</MenuItem>
              <MenuItem value="week">Last Week</MenuItem>
              <MenuItem value="month">Last Month</MenuItem>
              <MenuItem value="full">All Records</MenuItem>
            </Select>
          </StyledFormControl>

          {/* <StyledFormControl>
            <InputLabel id="membership-year-label">Membership Year</InputLabel>
            <Select
              labelId="membership-year-label"
              id="membership-year"
              value={membershipYear}
              onChange={handleYearChange}
              label="Membership Year"
              sx={{ minWidth: 140 }}
            >
              <MenuItem value="all">All Years</MenuItem>
              {years.map(year => (
                <MenuItem key={year} value={year}>{year}</MenuItem>
              ))}
            </Select>
          </StyledFormControl> */}
        </div>
      </div>
      <ResultsNavigator />
    </div>
  );
};

export default FilterBar;