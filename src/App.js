import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from "react";

function App() {
  console.log("init");
  const [currMessage, setCurrMessage] = useState(0);
  useEffect(() =>{
      fetch('http://localhost:5000/mes',
        {mode: "cors"})
          .then(res => res.json())
          .then(data => {
          console.log("hello");
          console.log(data)
        }).catch((e) => {
          console.log("failed to fetch");
          console.log(e);
    });
  },[]);
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p> The message is {currMessage}</p>
      </header>
    </div>
  );
}

export default App;
