import React, { useEffect, useState } from "react";
import './App.css';
import requests from "./requests";
import Login from "./components/LoginRegister/Login";
import Register from "./components/LoginRegister/Register";
import Inbox from "./components/Inbox/Inbox";
import { BrowserRouter, BrowserRouter as Router, Route, Switch } from 'react-router-dom'

function App() {

    return (
      <BrowserRouter>
        <Route exact path="/">
          <div className="Login">
            <Login />
          </div>
        </Route>
        <Route exact path="/register">
          <div className="App">
            <Register/>
          </div>
        </Route>
        <Route exact path="/inbox">
          <div className="App">
            <Inbox/>
          </div>
        </Route>
      </BrowserRouter>
    )
}

export default App;
