import './App.css';
import React from 'react'
import ReactDom from 'react-dom'
import ProfileScreen from './components/AccountDetails/profileScreen';
import Login from './components/LoginRegister/login';

function App() {
  var state = {token: null}

  function updateState (token) {
    state.token = token;
  }

  return (
    <div className='App'>
      <Login parentCallback={updateState}/>
      <ProfileScreen token={state.token}/>
    </div>
  )
}

export default App;
