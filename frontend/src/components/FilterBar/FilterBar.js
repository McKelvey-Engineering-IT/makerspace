import React, { useState, useContext } from "react";
import PropTypes from "prop-types";
import { AppContext } from "../../AppContext";
import ResultsNavigator from "../ResultsNavigator/ResultsNavigator";
import "./FilterBar.css";

const FilterBar = () => {
  const { filter, setFilter } = useContext(AppContext);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortType, setSortType] = useState("lastSignIn");

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSortChange = (event) => {
    console.log('test');
  };

  const handleFilterChange = (event) => {
    console.log('test');
  };

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