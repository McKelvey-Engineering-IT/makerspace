import React, { useContext, useEffect } from "react";
import CheckInTable from "./components/CheckInTable/CheckInTable";
import StudentDetail from "./components/StudentDetail/StudentDetail";
import FilterBar from "./components/FilterBar/FilterBar";
import Header from "./components/Header/Header";
import useApi from "./hooks/useApi";
import { AppContext } from "./AppContext";
import "./App.css";

const App = () => {
  const { selectedStudentId, updateTotalRecords, setNewRecords, lastCheckIn, setLastCheckIn, filter } = useContext(AppContext);

  const { data: firstLoad } = useApi({
    endpoint: `${process.env.REACT_APP_API_URL}/logins/historical?timeFilter=${filter}`
  });

  useEffect(() => {
    if (firstLoad.data) {
      updateTotalRecords(firstLoad.data);
      setLastCheckIn(firstLoad.last_checkin);
    }
  }, [firstLoad, updateTotalRecords, setLastCheckIn]);

  useEffect(() => {
    const fetchNewLogins = async () => {
      console.log('trying here');
      if (!lastCheckIn) return;
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/logins/check_logins`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ start_time: lastCheckIn })
        });

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const newLogins = await response.json();
        console.log('here is the new logins', newLogins);
        if (newLogins.data.length > 0) {
          console.log('also here')
          setLastCheckIn(newLogins.last_checkin);
          setNewRecords(newLogins.data);
        }
      } catch (error) {
        console.error("Failed to fetch new logins:", error);
      }
    };

    const intervalId = setInterval(fetchNewLogins, 10000); 

    return () => clearInterval(intervalId); 
  }, [lastCheckIn, setNewRecords, setLastCheckIn]);

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
          {selectedStudentId ? (
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
