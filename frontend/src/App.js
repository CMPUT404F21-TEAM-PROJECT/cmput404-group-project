import './App.css';
import React from 'react'
import ReactDom from 'react-dom'
import ProfileScreen from './components/AccountDetails/profileScreen';
import Login from './components/LoginRegister/login';

function App() {
  var state = {cookie: null}

  function handleLogin(c) {
    console.log(c)
    state = {cookie: c}
  }

  return (
    <div className='App'>
      <Login parentCallback={handleLogin}/>
      <ProfileScreen cookie={state.cookie}/>
    </div>
  )
}

export default App;
