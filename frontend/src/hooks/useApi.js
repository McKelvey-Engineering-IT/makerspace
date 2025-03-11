import { useState, useEffect, useRef } from "react";

const useApi = ({ endpoint, method = "GET", useSSE = false, body = null }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const eventSourceRef = useRef(null);
  
  useEffect(() => {
    if (!endpoint) return;
    
    setLoading(true);
    setError(null);
    
    if (useSSE) {
      const eventSource = new EventSource(endpoint);
      eventSourceRef.current = eventSource;
      
      eventSource.addEventListener("message", (e) => {
        try {
          if (e.data === "[DONE]") {
            eventSource.close();
          } else {
            setData(JSON.parse(e.data));
          }
        } catch (err) {
          setError(err);
        }
      });
      
      eventSource.addEventListener("error", (e) => {
        setError(new Error("EventSource connection failed"));
        setLoading(false);
      });
      
      return () => {
        eventSource.close();
      };
    } else {
      const fetchData = async () => {
        try {
          const response = await fetch(endpoint, {
            method,
            headers: {
              "Content-Type": "application/json",
            },
            body: body ? JSON.stringify(body) : null,
          });
          
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          
          const result = await response.json();
          setData(result);
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