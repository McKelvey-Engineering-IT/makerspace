import React, { useState, useMemo } from "react";
import CheckInTable from "./components/CheckInTable/CheckInTable";
import StudentDetail from "./components/StudentDetail/StudentDetail";
import Header from "./components/Header/Header";
import useApi from "./hooks/UseApi";
import "./App.css";

const App = () => {
  const [selectedStudentId, setSelectedStudentId] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortType, setSortType] = useState("lastSignIn");
  const [filter, setFilter] = useState("");
  
  const { data: checkIns = [], loading, error } = useApi({
    endpoint: `${process.env.REACT_APP_API_URL}/logins/check_logins`,
    useSSE: true
  });

  React.useEffect(() => {
    if (checkIns.length > 0 && !selectedStudentId) {
      setSelectedStudentId(checkIns[checkIns.length - 1].Email);
    }
  }, [checkIns, selectedStudentId]);

  const filteredAndSortedCheckIns = useMemo(() => {
    const filtered = checkIns.filter(checkIn => {

      const matchesSearch = searchTerm === "" || 
        checkIn.Name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        checkIn.Email.toLowerCase().includes(searchTerm.toLowerCase());
      
      if (!matchesSearch || !filter) return matchesSearch;
      
      const now = new Date();
      const signInDate = new Date(checkIn.SignInTime);
      const daysDiff = (now - signInDate) / (1000 * 60 * 60 * 24);
      
      return daysDiff <= (filter === "day" ? 1 : filter === "week" ? 7 : 30);
    });
    
    return [...filtered].sort((a, b) => {
      if (sortType === "name") return a.Name.localeCompare(b.Name);
      if (sortType === "studentId") return a.Email.localeCompare(b.Email);
      return new Date(b.SignInTime) - new Date(a.SignInTime);
    });
  }, [checkIns, searchTerm, filter, sortType]);

  if (error) return <div className="error">Error loading data</div>;

  return (
    <div className="app-container">
      <Header />
      <div className="main-content">
        <div className="left-panel">
          <div className="search-sort-filter-container">
            <h1>Member Check In</h1>
            <div className="search-bar">
              <input
                type="text"
                className="search-box"
                placeholder="Search by Name, Email"
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
              />
              <div className="controls-container">
                <div className="sort-control">
                  <select value={sortType} onChange={e => setSortType(e.target.value)}>
                    <option value="lastSignIn">Sort by: Last Sign In</option>
                    <option value="name">Sort by: Name</option>
                    <option value="studentId">Sort by: Email</option>
                  </select>
                </div>
                <div className="filter-control">
                  <select value={filter} onChange={e => setFilter(e.target.value)}>
                    <option value="">No Filter</option>
                    <option value="day">Filter: Last Day</option>
                    <option value="week">Filter: Last Week</option>
                    <option value="month">Filter: Last Month</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          {loading ? (
            <div className="loading">Loading...</div>
          ) : (
            <>
              <CheckInTable
                checkIns={filteredAndSortedCheckIns}
                onRowClick={setSelectedStudentId}
                studentId={selectedStudentId}
              />
              <p>Total Sign-ins: {filteredAndSortedCheckIns.length}</p>
            </>
          )}
        </div>

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