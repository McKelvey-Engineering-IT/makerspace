import React, { createContext, useState, useEffect } from 'react';

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [newRecords, setNewRecords] = useState([]);
  const [totalRecords, setTotalRecords] = useState([]);
  const [recordsInView, setRecordsInView] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [recordsPerPage, setRecordsPerPage] = useState(10);
  const [currentRecordCount, setCurrentRecordCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [filter, setFilter] = useState("day");
  const [lastCheckIn, setLastCheckIn] = useState(null);
  const [sortType, setSortType] = useState("lastSignIn");
  const [sortedRecords, setSortedRecords] = useState([]);
  const [newRecordsUnread, setNewRecordsUnread] = useState([]);
  const [soundAlertsEnabled, setSoundAlertsEnabled] = useState(false);  // Default to false

  const updateRecordsInView = () => {
    const start = (currentPage - 1) * recordsPerPage;
    const end = start + recordsPerPage;
    setRecordsInView(totalRecords.slice(start, end));
    setCurrentRecordCount(totalRecords.slice(start, end).length);
  };

  const updateCurrentPage = (page) => {
    setCurrentPage(page);
  }

  const updateTotalRecords = (records) => {
    setTotalRecords(records);
    setTotalPages(Math.ceil(records.length / recordsPerPage));
  };

  return (
    <AppContext.Provider
      value={{
        updateRecordsInView,
        updateCurrentPage,
        updateTotalRecords,
        newRecords,
        setNewRecords,
        totalRecords,
        setTotalRecords,
        recordsInView,
        setRecordsInView,
        selectedStudent,
        setSelectedStudent,
        recordsPerPage,
        setRecordsPerPage,
        currentRecordCount,
        setCurrentRecordCount,
        currentPage,
        setCurrentPage,
        totalPages,
        setTotalPages,
        filter,
        setFilter,
        lastCheckIn,
        setLastCheckIn,
        sortType,
        setSortType,
        sortedRecords,
        setSortedRecords,
        newRecordsUnread,
        setNewRecordsUnread,
        soundAlertsEnabled,
        setSoundAlertsEnabled
      }}
    >
      {children}
    </AppContext.Provider>
  );
};