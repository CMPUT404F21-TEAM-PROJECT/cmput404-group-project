import React, { useEffect, Component } from "react";
// import './App.css';
import {
    Button,
    TextField,
  } from "@mui/material";
import "../../styles/login-register.css";
import requests from "../../requests";
import { NavLink } from "react-router-dom";
  
class Register extends Component {
    state = {
          username: "",
          password: "",
          confirm_password: "",
      }

    handleRegister = async () => {
        console.log(this.state);
        if(this.state.password == this.state.confirm_password) {
            const response = await requests.post(`service/register/`, {
                username: this.state.username,
                password: this.state.password
            });
            alert(response);
        }
        else {
            console.log("Passwords Don't Match");
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
                Create a new account
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
                })}
            />
            <br/>
            <TextField
                className="text-input"
                size="small"
                type="text"
                type="password"
                label="Password"
                value={this.state.password}
                onChange={({ target }) =>
                this.setState({
                password: target.value
                })}
            />
            <br/>
            <TextField
                className="text-input"
                size="small"
                type="text"
                type="password"
                label="Confirm Password"
                value={this.state.confirm_password}
                onChange={({ target }) =>
                this.setState({
                confirm_password: target.value
                })}
            />
            <br/>
            <Button
                className="avonmore-button"
                disabled={this.state.loginBtnDisabled}
                color="primary"
                variant="contained"
                onClick={this.handleRegister}
                ref={node => (this.btn = node)}>
              Register
            </Button>
            </div>
            <NavLink style={{ textDecoration: 'none', position: 'relative', top: '30px' }} to="/">Have an account? Log in</NavLink>
          </div>
          </body>
        );
    }
}
export default Register;
