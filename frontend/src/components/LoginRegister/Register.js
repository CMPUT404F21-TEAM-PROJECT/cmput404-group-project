import React, { useEffect, useState, Component } from "react";
import {
    Button,
    TextField,
    Alert,
    AlertTitle
  } from "@mui/material";
import "../../styles/login-register.css";
import requests from "../../requests";
import { NavLink } from "react-router-dom";
  
class Register extends Component {
    state = {
          username: "",
          password: "",
          confirm_password: "",
          registration_error: false,
          registration_success: false,
          error_messages: ""
      }

    validateRegister() {
        if (!this.state.username) {
            this.setState({registration_error: true})
            this.setState({registration_success: false})
            this.setState({error_messages: "Username is empty"})
            return false
        }
        if (!this.state.password) {
            this.setState({registration_error: true})
            this.setState({registration_success: false})
            this.setState({error_messages: "Password is Empty"})
            return false
        }
        if (!(this.state.password == this.state.confirm_password)) {
            this.setState({registration_error: true})
            this.setState({registration_success: false})
            this.setState({error_messages: "Passwords do not Match"})
            return false
        }
        return true;
    }

    handleRegister = async () => {
        if(this.validateRegister()) {
            try {
                const response = await requests.post(`register/`, {
                    username: this.state.username,
                    password: this.state.password
                });
                this.setState({registration_error: false})
                this.setState({registration_success: true})
            }
            catch {
                this.setState({registration_error: true})
                this.setState({registration_success: false})
                this.setState({error_messages: "Error occurred during registration"})
            }
        }
    }

  render() {
      return (
          <body className="background">
          <div className="login-form">
          {this.state.registration_success&&<Alert className="alert"  severity="success">
                <AlertTitle><strong>Account Successfully Created</strong></AlertTitle>
            </Alert>}
            {this.state.registration_error&&<Alert className="alert"  severity="error">
                <AlertTitle><strong>{this.state.error_messages}</strong></AlertTitle>
            </Alert>}
            <h1>
                Social Distributions
            </h1>
            <h3>
                Create a new account
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
            {/* {this.state.username_error&&<div>HI</div>} */}
            <br/>
            <Button
                disabled={this.state.loginBtnDisabled}
                color="primary"
                variant="contained"
                onClick={this.handleRegister}
                ref={node => (this.btn = node)}>
              Register
            </Button>
            <NavLink style={{ textDecoration: 'none', position: 'relative', top: '30px' }} to="/">Have an account? Log in</NavLink>
            </div>
          </div>
          </body>
        );
    }
}
export default Register;
