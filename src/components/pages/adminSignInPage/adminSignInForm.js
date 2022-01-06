import React, {useState} from "react";
import {APIBase} from "../../../constAttributes";
import {useAppContext} from "../../../lib/contextLib";


export const SignInForm = () => {
    const { userHasAuthenticated } = useAppContext();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    function handleSubmit(event) {
        event.preventDefault();
        //alert("submitted")
        fetch(APIBase + "/auth_admin/" + username + "/" + password, {method: 'POST', mode: "cors"})
            .then(res => res.json())
            .then(data => {
                //console.log(data);
                if (data.result === true){
                    console.log("auth is true");
                    userHasAuthenticated(true);
                }
            });
    }

    return(
        <div className = "SignInForm">
            <form onSubmit={handleSubmit}>
                <label>
                    Name:
                    <input name="username" type="username" className="form-control" placeholder="Enter username" value={username}
                           onChange={(e) => setUsername(e.target.value)}/>
                </label>
                <br></br>
                <label>
                    Password:
                    <input name="password" type="password" className="form-control" placeholder="Enter password" value={password}
                           onChange={(e) => setPassword(e.target.value)}/>
                </label>
                <br></br>
                <button type="submit" value="Submit" > Submit</button>
            </form>
        </div>
    );
}


/*export class AdminSignInForm extends React.Component{
    constructor(props) {
    super(props);
    this.username = {username: ''};
    this.password = {password: ''};

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
        event.preventDefault();
        *//*fetch(APIBase + "/add_admin/" + this.state.username + "/" + this.state.password, {method: 'POST', mode: "cors"})
            .then(res => res.json())
            .then(data => {
                console.log(data);
            });*/
        /*fetch(APIBase + "/auth_admin/" + this.state.username + "/" + this.state.password, {method: 'POST', mode: "cors"})
            .then(res => res.json())
            .then(data => {
                console.log(data);
                if (data.result === true){
                    console.log("auth is true");
                }
            });
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
          <br></br>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}*/