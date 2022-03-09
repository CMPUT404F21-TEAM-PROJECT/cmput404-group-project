import React, { useEffect, useState } from "react";
import './App.css';
import NavBar from "./components/NavBar.js";


import Login from "./components/LoginRegister/login";
import Register from "./components/LoginRegister/Register";
import Inbox from "./components/Inbox/Inbox";
import PublicPosts from "./components/Posts/PublicPosts";
import FriendsPage from "./components/Followers/FriendsPage";
import { BrowserRouter, BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import ProfileScreen from "./components/AccountDetails/profileScreen";
import NewPost from "./components/Posts/NewPost.js"

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
            <NavBar />
            <Inbox/>
          </div>
        </Route>
        <Route exact path="/profile">
          <div className="Profile">
            <NavBar />
            <ProfileScreen/>
          </div>
        </Route>
        <Route exact path="/friends">
          <div className="App">
            <NavBar />
            <FriendsPage/>
          </div>     
        </Route>   
        <Route exact path="/post">
          <div className="NewPost">
            <NavBar />
            <NewPost/>
          </div>
        </Route>
        <Route exact path="/public_posts">
          <div className="PublicPosts">
            <NavBar />
            <PublicPosts/>
          </div>
        </Route>
      </BrowserRouter>
    )
}

export default App;
