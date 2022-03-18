import React, { useEffect, Component } from "react";
// import './App.css';
import {
    Button,
    TextField,
    Alert,
    AlertTitle
  } from "@mui/material";
import "../../styles/login-register.css";
import requests from "../../requests";
import ProfileScreen from "../AccountDetails/profileScreen";
import {useHstory, Redirect, NavLink } from "react-router-dom";
  
class Login extends Component {
    state = {
          username: "",
          password: "",
          successful_login: false,
          error_login: false,
          error_messages: ""
      }

    validateLogin() {
        if (!this.state.username) {
            this.setState({error_login: true})
            this.setState({error_messages: "Username is empty"})
            return false
        }
        if (!this.state.password) {
            this.setState({error_login: true})
            this.setState({error_messages: "Password is Empty"})
            return false
        }
        return true;
    }
    handleLogin = async () => {
        if (this.validateLogin()) {
            try {
                const response = await requests.post(`login/`, {
                    username: this.state.username,
                    password: this.state.password
                }, {WithCredentials: true});
                localStorage.setItem('access_token', response.data);
                requests.defaults.headers['Authorization'] = localStorage.getItem('access_token');
                this.setState({successful_login: true})
            }
            catch {
                this.setState({error_login: true})
                this.setState({error_messages: "Username or password was incorrect"})
            }
        }
    }

  render() {
      return (
          <body className="background">
          <div className="login-form">
          {this.state.error_login&&<Alert className="alert"  severity="error">
                <AlertTitle><strong>{this.state.error_messages}</strong></AlertTitle>
            </Alert>}
            <h1>
                Social Distributions
            </h1>
            <h3>
                Please Log in to Continue
            </h3>
            <div className="login-wrapper">
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
