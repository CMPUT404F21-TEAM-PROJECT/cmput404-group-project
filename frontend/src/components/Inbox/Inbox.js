import React, { useEffect, Component } from "react";
// import './App.css';
import "../../styles/inbox.css";
import requests from "../../requests";
import { Redirect, NavLink } from "react-router-dom";
  
class Inbox extends Component {
  render() {
      return (
          <div className="App">
            <h1>
                Successfully Logged In
            </h1>
          </div>
        );
    }
}

export default Inbox;
