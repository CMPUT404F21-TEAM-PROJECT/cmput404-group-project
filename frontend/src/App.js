import './App.css';
import React from 'react'
import ReactDom from 'react-dom'
import ProfileScreen from './pages/profileScreen';

function App() {

    return (
      <div className="App">
        <header className="App-header"></header>
        <body>
          {ReactDom.render(<ProfileScreen />)}
        </body>
      </div>
    )
}

export default App;
