import React, { useContext, useEffect, useRef } from "react";
import CheckInTable from "./components/CheckInTable/CheckInTable";
import StudentDetail from "./components/StudentDetail/StudentDetail";
import FilterBar from "./components/FilterBar/FilterBar";
import Header from "./components/Header/Header";
import useApi from "./hooks/useApi";
import { AppContext } from "./AppContext";
import "./App.css";

const App = () => {
  const {
    selectedStudent,
    updateTotalRecords,
    setNewRecords,
    sortType,
    filter,
    currentPage,
    setTotalRecords,
    setNewRecordsUnread,
    newRecords,
      } = useContext(AppContext);
  let lastRecordSeen = null;

  const { data: firstLoad } = useApi({
    endpoint: `${process.env.REACT_APP_API_URL}/logins/historical?timeFilter=${filter}`,
  });

  useEffect(() => {
    if (!firstLoad?.data) return;
    console.log("First load data:", firstLoad.data);

    if(lastRecordSeen === null) lastRecordSeen = firstLoad.last_record;

    updateTotalRecords(firstLoad.data);
  }, [firstLoad.data]);

  useEffect(() => {
    const fetchNewLogins = async () => {
      if (!lastRecordSeen) return;

      try {
        const response = await fetch(
          `${process.env.REACT_APP_API_URL}/logins/check_logins`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ start_id: lastRecordSeen }),
          }
        );

        if (!response.ok)
          throw new Error(`HTTP error! Status: ${response.status}`);

        const newLogins = await response.json();

        if (newLogins.data.length > 0) {
          setNewRecords((prevRecords) => {
            const existingIds = new Set(prevRecords.map(record => record.LogID));
            const uniqueNewLogins = newLogins.data.filter(record => !existingIds.has(record.LogID));
            return [...prevRecords, ...uniqueNewLogins];
          });
        }

        lastRecordSeen = newLogins.last_record;
      } catch (error) {
        console.error("Failed to fetch new logins:", error);
      }
    };

    fetchNewLogins();
    const intervalId = setInterval(fetchNewLogins, 10000);

    return () => clearInterval(intervalId);
  }, [firstLoad]);

  useEffect(() => {
    if (
      sortType === "lastSignIn" &&
      currentPage === 1 &&
      newRecords.length > 0
    ) {
      setNewRecordsUnread(() => newRecords.map((record) => record.LogID));
      setTotalRecords((prevRecords) => {
        const existingIds = new Set(prevRecords.map(record => record.LogID));
        const uniqueNewRecords = newRecords.filter(record => !existingIds.has(record.LogID));
        return [...uniqueNewRecords, ...prevRecords];
      });
      setNewRecords([]);
    }
  }, [newRecords]);

  return (
    <div className="app-container">
      <Header />
      <div className="main-content">
        <div className="left-panel">
          <h1>Member Check In</h1>
          <FilterBar />
          <CheckInTable />
        </div>
        <div className="right-panel">
          {selectedStudent ? (
            <StudentDetail />
          ) : (
            <p className="select-prompt">Select a member to view details</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
