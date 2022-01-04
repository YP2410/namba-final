import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from "react";

const APIBase = "http://localhost:5000"


class NameForm extends React.Component{
    constructor(props) {
    super(props);
    this.username = {username: ''};
    this.password = {password: ''}

    this.handleChangeUser = this.handleChangeUser.bind(this);
    this.handleChangePassword = this.handleChangePassword.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  handleChangeUser(event) {
        this.setState({username: event.target.value});
  }
  handleChangePassword(event) {
        this.setState({password: event.target.value});
  }

  handleSubmit(event) {
        //alert('A name was submitted: ' + this.state.username);
        //alert('A password was submitted: ' + this.state.password);
        event.preventDefault();
        /*fetch(APIBase + "/add_admin/" + this.state.username + "/" + this.state.password, {method: 'POST', mode: "cors"})
            .then(res => res.json())
            .then(data => {
                console.log(data);
            });*/
        fetch(APIBase + "/auth_admin/" + this.state.username + "/" + this.state.password, {method: 'POST', mode: "cors"})
            .then(res => res.json())
            .then(data => {
                console.log(data);
            })

  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Name:
            <input name="username" type="username" className="form-control" placeholder="Enter username"
                   onChange={this.handleChangeUser}/>
        </label>
          <br></br>
          <label>
          Password:
            <input name="password" type="password" className="form-control" placeholder="Enter password"
                   onChange={this.handleChangePassword}/>
        </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}



function App() {
  //console.log("init");
  const [currMessage, setCurrMessage] = useState(0);
  useEffect(() =>{
      fetch('http://localhost:5000/mes',
        {mode: "cors"})
          .then(res => res.json())
          .then(data => {
          //console.log("hello");
          //console.log(data);
          setCurrMessage(data.message);
        }).catch((e) => {
          //console.log("failed to fetch");
          //console.log(e);
    });
  },[]);

    function handleSubmit(e) {
        e.preventDefault();
        //console.log(e.username);
        //console.log("clicked submit")
    }

    return (
    <div className="App">
      <header className="App-header">
          <h1>Admin page</h1>
          <NameForm/>
          <form onSubmit={handleSubmit}>
              <h3>Sign In</h3>
              <div className="form-group">
                    <label>Username</label>
                    <input name="username" type="username" className="form-control" placeholder="Enter username" />
              </div>

              <div className="form-group">
                  <label>Password</label>
                  <input name="password" type="password" className="form-control" placeholder="Enter password" />
              </div>

              <button type="submit" className="btn btn-primary btn-block">Submit</button>
          </form>

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
