import React, { useEffect } from "react";
import logo from './logo.svg';
import './App.css';
import requests from "./requests";

function App() {

  const fetchAuthors = async () => {
    // sends a GET request to http://${BACKEND_URL}:${BACKEND_PORT}/service/authors
    const response = await requests.get(`service/authors/`, {
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
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
