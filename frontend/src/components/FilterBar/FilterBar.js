import React, { useState, useContext, useEffect, useCallback } from "react";
import { AppContext } from "../../AppContext";
import ResultsNavigator from "../ResultsNavigator/ResultsNavigator";
import "./FilterBar.css";

const FilterBar = () => {
  const {
    filter,
    setFilter,
    sortType,
    setSortType,
    setRecordsInView,
    totalRecords,
    setTotalRecords,
    setCurrentPage,
    updateTotalRecords,
    setSortedRecords,
  } = useContext(AppContext);

  const [searchTerm, setSearchTerm] = useState("");

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
    // Reset to first page when search changes
    setCurrentPage(1);
  };

  const handleSortChange = (event) => {
    setSortType(event.target.value);
    // Reset to first page when sort changes
    setCurrentPage(1);
  };

  const handleFilterChange = (event) => {
    setFilter(event.target.value);
    // Reset to first page when filter changes
    setCurrentPage(1);
  };

  // Define a single function to handle both filtering and sorting
  useEffect(() => {
    console.log("Processing records, totalRecords:", totalRecords.length);

    if (!totalRecords || totalRecords.length === 0) {
      console.log("No records to process");
      setRecordsInView([]);
      return;
    }
    console.log("Total records:", totalRecords.length);
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

    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase();
      processedRecords = processedRecords.filter(
        (record) =>
          record.Name?.toLowerCase().includes(term) ||
          record.Email?.toLowerCase().includes(term)
      );
      console.log("After search:", processedRecords.length);
    }

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
    console.log("Final processed records:", processedRecords.length);

    setSortedRecords(processedRecords);
    console.log("Set records in view:", processedRecords.length);
  }, [totalRecords]);

  return (
    <div className="filter-bar">
      <div className="filter-bar-content">
        <div className="search-container">
          <input
            type="text"
            className="search-box"
            placeholder="Search by Name or Email"
            value={searchTerm}
            onChange={handleSearchChange}
          />
        </div>
        <div className="dropdown-container">
          <div className="dropdown-wrapper">
            <label htmlFor="sort-dropdown">Sort by</label>
            <select
              id="sort-dropdown"
              value={sortType}
              onChange={handleSortChange}
              className="dropdown"
            >
              <option value="lastSignIn">Last Sign In</option>
              <option value="name">Name</option>
              <option value="studentId">Email</option>
            </select>
          </div>
          <div className="dropdown-wrapper">
            <label htmlFor="time-dropdown">Time period</label>
            <select
              id="time-dropdown"
              value={filter}
              onChange={handleFilterChange}
              className="dropdown"
            >
              <option value="day">Last Day</option>
              <option value="week">Last Week</option>
              <option value="month">Last Month</option>
              <option value="full">All Records</option>
            </select>
          </div>
        </div>
      </div>
      <ResultsNavigator />
    </div>
  );
};

export default FilterBar;
