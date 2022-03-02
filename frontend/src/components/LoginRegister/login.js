import React, { useEffect, Component } from "react";
// import './App.css';
import {
    Button,
    TextField,
  } from "@mui/material";
import "../../styles/login-register.css";
import requests from "../../requests";
import ProfileScreen from "../AccountDetails/profileScreen";
import {useHstory, Redirect, NavLink } from "react-router-dom";
  
class Login extends Component {
    state = {
          username: "",
          password: "",
          successful_login: false
      }
    handleLogin = async () => {
        console.log(this.state);
        try {
            const response = await requests.post(`service/login/`, {
                username: this.state.username,
                password: this.state.password
            }, {WithCredentials: true});
            localStorage.setItem('access_token', response.data);
            requests.defaults.headers['Authorization'] = 'JWT ' + localStorage.getItem('access_token');
            console.log(response.data);
            this.setState({successful_login: true})
        }
        catch(error) {
            console.log(error);
        }
    }

    verifyLogin = (e) => {
        console.log(this.successful_login)
        if (!this.successful_login) {
            e.preventDefault();
        }
    }

  render() {
      return (
          <body class="background">
          <div className="form">
            <h1>
                Social Distributions
            </h1>
            <h3>
                Please Log in to Continue
            </h3>
            <div className="wrapper">
            <TextField
                className="text-input"
                size="small"
                type="text"
                label="Username"
                value={this.state.username}
                onChange={({ target }) =>
                this.setState({
                username: target.value
                })
            }
            />
            <br/>
            <TextField
                className="text-input"
                size="small"
                type="text"
                label="Password"
                type="password"
                value={this.state.password}
                onChange={({ target }) =>
                    this.setState({
                    password: target.value
                    })
                }
            />
            <br/>
            <Button
                disabled={this.state.loginBtnDisabled}
                variant="contained"
                onClick={this.handleLogin}
                ref={node => (this.btn = node)}>
              Login
            </Button>
            {this.state.successful_login && <Redirect to="/inbox" />}
            </div>
            <NavLink style={{ textDecoration: 'none', position: 'relative', top: '20px' }} to="/register">Don't have an account? Sign Up</NavLink>
          </div>
          </body>
        );
    }
}

export default Login;
