import { useState, useEffect, useRef } from "react";

const useApi = ({ endpoint, method = "GET", useSSE = false, body = null }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(!useSSE);
  const [error, setError] = useState(null);
  const eventSourceRef = useRef(null);

  useEffect(() => {
    if (!endpoint) return;

    setError(null);

    if (useSSE) {
      const eventSource = new EventSource(endpoint);
      eventSourceRef.current = eventSource;

      eventSource.addEventListener("message", (e) => {
        try {
          if (e.data === "[DONE]") {
            eventSource.close();
          } else {
            const newData = JSON.parse(e.data);
            setData((prevData) => newData.data); // Append new records
          }
        } catch (err) {
          setError(err);
        }
      });

      eventSource.addEventListener("error", (e) => {
        setError(new Error("EventSource connection failed"));
        eventSource.close();
      });

      return () => eventSource.close();
    } else {
      const fetchData = async () => {
        try {
          setLoading(true);
          const response = await fetch(endpoint, {
            method,
            headers: { "Content-Type": "application/json" },
            body: body ? JSON.stringify(body) : null,
          });

          if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

          const result = await response.json();
          setData(result.data || []);
        } catch (err) {
          setError(err);
        } finally {
          setLoading(false);
        }
      };

      fetchData();
    }
  }, [endpoint, method, useSSE, body]);

  return { data, loading, error };
};

export default useApi;
