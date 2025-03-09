import React, { useState, useEffect } from "react";
import CheckInTable from "./CheckInTable";
import StudentDetail from "./StudentDetail";
import Header from "./Header";
import "./App.css";

const App = () => {
  let firstLogin = true;
  const [checkIns, setCheckIns] = useState([]);
  const [selectedStudentId, setSelectedStudentId] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortType, setSortType] = useState("lastSignIn");
  const [filter, setFilter] = useState("");

  useEffect(() => {
    const eventSource = new EventSource(
      "http://localhost:8001/logins/check_logins"
    );

    eventSource.addEventListener("message", (e) => {
      try {
        if (e.data == "[DONE]") eventSource.close();
        else {
          const messageObject = JSON.parse(e.data);
          setCheckIns(messageObject.data);

          if (messageObject.data.length > 0 && firstLogin) {
            firstLogin = false;
            let final_entry = messageObject.data.length;

            setSelectedStudentId(messageObject.data[final_entry - 1].email);
          }
        }
      } catch (error) {
        console.log(error);
      }
    });

    eventSource.onerror = (error) => {
      console.error("SSE Error:", error);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSort = (e) => {
    setSortType(e.target.value);
  };

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  const handleRowClick = (studentId) => {
    setSelectedStudentId(studentId);
  };

  const applyFilters = (data) => {
    const now = new Date();
    return data.filter((checkIn) => {
      const signInDate = new Date(checkIn.signInTime);
      if (filter === "day" && (now - signInDate) / (1000 * 60 * 60 * 24) > 1) {
        return false;
      }
      if (filter === "week" && (now - signInDate) / (1000 * 60 * 60 * 24) > 7) {
        return false;
      }
      if (
        filter === "month" &&
        (now - signInDate) / (1000 * 60 * 60 * 24) > 30
      ) {
        return false;
      }
      return true;
    });
  };
  //sort check in tables
  const getSortedCheckIns = (data) => {
    return data.sort((a, b) => {
      if (sortType === "name") {
        return a.name.localeCompare(b.name);
      } else if (sortType === "studentId") {
        return a.email.localeCompare(b.studentId);
      } else {
        return new Date(b.signInTime) - new Date(a.signInTime);
      }
    });
  };
  //filter
  const filteredAndSortedCheckIns = getSortedCheckIns(
    applyFilters(
      checkIns.filter(
        (checkIn) =>
          checkIn.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          checkIn.email.includes(searchTerm.toLowerCase())
      )
    )
  );

  return (
    <div className="app-container">
      <Header />
      {/* <h1 value = "2b" >Member Check In</h1> */}
      <div className="main-content">
        {/* left side CheckInTable */}
        <div className="left-panel">
          <div className="search-sort-filter-container">
            <h1 value="2b">Member Check In</h1>
            <div className="search-bar">
              <input
                type="text"
                className="search-box"
                placeholder="Search by Name, Email"
                value={searchTerm}
                onChange={handleSearch}
              />
              {/* sort */}
              <div className="controls-container">
                <div className="sort-control">
                  <select value={sortType} onChange={handleSort}>
                    <option value="lastSignIn">Sort by: Last Sign In</option>
                    <option value="name">Sort by: Name</option>
                    <option value="studentId">Sort by: Email</option>
                  </select>
                </div>
                {/* filter */}
                <div className="filter-control">
                  <select value={filter} onChange={handleFilterChange}>
                    <option value="">No Filter</option>
                    <option value="day">Filter: Last Day</option>
                    <option value="week">Filter: Last Week</option>
                    <option value="month">Filter: Last Month</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          {/* check in table */}
          <CheckInTable
            checkIns={filteredAndSortedCheckIns}
            onRowClick={handleRowClick}
            studentId={selectedStudentId}
          />
          <p>
            Total Number of Sign-ins in Selected Time Range:{" "}
            {filteredAndSortedCheckIns.length}
          </p>
        </div>

        {/* right side StudentDetail */}
        <div className="right-panel">
          {selectedStudentId ? (
            <StudentDetail studentId={selectedStudentId} />
          ) : (
            <p>Select a student to view details</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
