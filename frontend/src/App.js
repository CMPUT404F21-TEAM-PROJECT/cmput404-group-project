import React, { useEffect } from "react";
import logo from './logo.svg';
import './App.css';
import requests from "./requests";
import NavBar from "./components/NavBar.js";

function App() {

  const fetchAuthors = async () => {
    // sends a GET request to http://${BACKEND_URL}:${BACKEND_PORT}/service/authors
    const response = await requests.get("service/authors/", {
      // uncommenting below will send request to /authors?page=2&size=2
      // params: {
      //   page: 2,
      //   size: 2
      // },
    });

    console.log(response)
    console.log('hi from fetchAuthors')
  };

  // Send the request once on loadup
  useEffect(() => {
    fetchAuthors();
  }, []);
  
  

  return (
    <div className="App">
      <NavBar />
    </div>
  );
}

export default App;
