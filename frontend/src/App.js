import React, { useEffect, useState } from "react";
import './App.css';
import NavBar from "./components/NavBar.js";


import Login from "./components/LoginRegister/login";
import Register from "./components/LoginRegister/Register";
import Inbox from "./components/Inbox/Inbox";
import Post from "./components/Inbox/Post";
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
            <Post author= {{displayName: "authorname"}}
            title="title"
            contentType="application/base64"
            content= "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/1200px-Image_created_with_a_mobile_phone.png"
            description= "description"
            post= {{id: "0402b818-b38e-4379-afbf-06bf376b2056"}}
            currentUser="5594ed47-e52a-4862-8dc8-ecc11305bd71"/>
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
      </BrowserRouter>
    )
}

export default App;
