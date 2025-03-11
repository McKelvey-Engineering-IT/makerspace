import React, { useState, useMemo } from "react";
import CheckInTable from "./components/CheckInTable/CheckInTable";
import StudentDetail from "./components/StudentDetail/StudentDetail";
import Header from "./components/Header/Header";
import useApi from "./hooks/useApi";
import "./App.css";

const App = () => {
  const [selectedStudentId, setSelectedStudentId] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortType, setSortType] = useState("lastSignIn");
  const [filter, setFilter] = useState("");
  
  const { data: checkIns = [] } = useApi({
    endpoint: `${process.env.REACT_APP_API_URL}/logins/check_logins`,
    useSSE: true,
  });
  
  if (!selectedStudentId && checkIns.length) {
    setSelectedStudentId(checkIns[checkIns.length - 1].Email);
  }

  const filteredAndSortedCheckIns = useMemo(() => {
    const now = new Date();
    return checkIns
      .filter(({ Name, Email, SignInTime }) => {
        const matchesSearch =
          Name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          Email.includes(searchTerm.toLowerCase());
        if (!matchesSearch) return false;
        if (!filter) return true;
        const daysDiff = (now - new Date(SignInTime)) / 86400000;
        return filter === "day" ? daysDiff <= 1 : filter === "week" ? daysDiff <= 7 : daysDiff <= 30;
      })
      .sort((a, b) =>
        sortType === "name" ? a.Name.localeCompare(b.Name) :
        sortType === "studentId" ? a.Email.localeCompare(b.Email) :
        new Date(b.SignInTime) - new Date(a.SignInTime)
      );
  }, [checkIns, searchTerm, filter, sortType]);

  return (
    <div className="app-container">
      <Header />
      <div className="main-content">
        <div className="left-panel">
          <div className="search-sort-filter-container">
            <h1>Member Check In</h1>
            <input type="text" className="search-box" placeholder="Search by Name, Email" value={searchTerm} onChange={e => setSearchTerm(e.target.value)} />
            <div className="controls-container">
              <select value={sortType} onChange={e => setSortType(e.target.value)}>
                <option value="lastSignIn">Sort by: Last Sign In</option>
                <option value="name">Sort by: Name</option>
                <option value="studentId">Sort by: Email</option>
              </select>
              <select value={filter} onChange={e => setFilter(e.target.value)}>
                <option value="">No Filter</option>
                <option value="day">Filter: Last Day</option>
                <option value="week">Filter: Last Week</option>
                <option value="month">Filter: Last Month</option>
              </select>
            </div>
          </div>
          <CheckInTable checkIns={filteredAndSortedCheckIns} onRowClick={setSelectedStudentId} studentId={selectedStudentId} />
          <p>Total Sign-ins: {filteredAndSortedCheckIns.length}</p>
        </div>
        <div className="right-panel">
          {selectedStudentId ? <StudentDetail studentId={selectedStudentId} /> : <p>Select a student to view details</p>}
        </div>
      </div>
    </div>
  );
};

export default App;
