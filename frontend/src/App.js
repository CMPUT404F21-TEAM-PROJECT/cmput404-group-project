import React, { useEffect } from "react";
import logo from './logo.svg';
import './App.css';
import requests from "./requests";
import FollowRequest from "./components/Followers/FollowRequest";

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
      <FollowRequest
        currentUser="ce2b9fb6-ab59-42b5-9173-f89704954f78"
        displayName="display name"
        profileImage="https://i.imgur.com/k7XVwpB.jpeg"
        id="21d21da7-dba1-45da-92e9-bc526be3831f"
      />
    </div>
  );
}

export default App;
