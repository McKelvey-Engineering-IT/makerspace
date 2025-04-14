import React, { useContext, useEffect, useState } from "react";
import CheckInTable from "./components/CheckInTable/CheckInTable";
import StudentDetail from "./components/StudentDetail/StudentDetail";
import FilterBar from "./components/FilterBar/FilterBar";
import Header from "./components/Header/Header";
import ErrorBanner from "./components/ErrorBanner/ErrorBanner";
import { AppContext } from "./AppContext";
import "./App.css";

const App = () => {
  const [error, setError] = useState(null);
  const {
    selectedLog,
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

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const response = await fetch(
          `${process.env.REACT_APP_API_URL}/logins/historical?timeFilter=${filter}`
        );

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const firstLoad = await response.json();
        if (!firstLoad?.data) return;

        if (lastRecordSeen === null) lastRecordSeen = firstLoad.last_record;
        updateTotalRecords(firstLoad.data);
      } catch (error) {
        console.error("Failed to fetch initial data:", error);
        setError(new Date().toISOString());
      }
    };

    fetchInitialData();
  }, [filter]);

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
        setError(new Date().toISOString());
      }
    };

    fetchNewLogins();
    const intervalId = setInterval(fetchNewLogins, 10000);

    return () => clearInterval(intervalId);
  }, [lastRecordSeen]);

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
      {error && <ErrorBanner timestamp={error} />}
      <Header />
      <div className="main-content">
        <div className="left-panel">
          <h1>Member Check In</h1>
          <FilterBar />
          <CheckInTable />
        </div>
        <div className="right-panel">
          {selectedLog ? (
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
