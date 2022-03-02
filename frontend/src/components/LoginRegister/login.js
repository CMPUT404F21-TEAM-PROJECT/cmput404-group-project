import React, { useEffect, Component } from "react";
// import './App.css';
import requests from "../../requests";
import ProfileScreen from "../AccountDetails/profileScreen";

// class Login extends Component() {

//   const fetchAuthors = async () => {
//     // sends a GET request to http://${BACKEND_URL}:${BACKEND_PORT}/service/authors
//     const response = await requests.get(`service/authors/`, {
//       // uncommenting below will send request to /authors?page=2&size=2
//       // params: {
//       //   page: 2,
//       //   size: 2
//       // },
//     });

//     console.log(response)
//     console.log('hi from fetchAuthors')
//   };

  // Send the request once on loadup
//   useEffect(() => {
//     fetchAuthors();
//   }, []);
  
  
class Login extends Component {

    state = {
        credentials: {username: '', password: ''}
    }
    login = async () => {
        console.log(this.state.credentials);
        const response = await requests.post(`service/login/`, {
            username: this.state.credentials.username,
            password: this.state.credentials.password,
        }, {withCredentials: true});
        alert(response);
        this.props.parentCallback(response.data.token);
    }

    inputChanged = event => {
        const cred = this.state.credentials;
        cred[event.target.name] = event.target.value;
        this.setState({credentials: cred});
    }

  render() {
      return (
          <div className="LoginScreen">
            <h1>
              Login
            </h1>
            <label>
                Username: <input type="text" name="username" 
                value={this.state.credentials.username}
                onChange = {this.inputChanged}/>
            </label>
            <br/>
            <label>
                Password: <input type="password" name="password"
                value={this.state.credentials.password}
                onChange = {this.inputChanged}/>
            </label>
            <br/>
            <button onClick={this.login}>Login</button>
          </div>
        );
    }
}

export default Login;
