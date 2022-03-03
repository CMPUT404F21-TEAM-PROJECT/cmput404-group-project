import React, { useEffect, useState } from "react";
import './App.css';
import Login from "./components/LoginRegister/login";
import Register from "./components/LoginRegister/Register";
import Inbox from "./components/Inbox/Inbox";
import { BrowserRouter, BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import ProfileScreen from "./components/AccountDetails/profileScreen";

function App() {

    return (
      <BrowserRouter>
        <Route exact path="/">
          <div className="Login">
            <Login />
          </div>
        </Route>
        <Route exact path="/register">
          <div className="Register">
            <Register/>
          </div>
        </Route>
        <Route exact path="/inbox">
          <div className="Inbox">
            <Inbox/>
          </div>
        </Route>
        <Route exact path="/profile">
          <div className="Profile">
            <ProfileScreen/>
          </div>
        </Route>        
      </BrowserRouter>
    )
}

export default App;
