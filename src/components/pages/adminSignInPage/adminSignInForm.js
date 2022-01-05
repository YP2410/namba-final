import React from "react";
import {APIBase} from "../../../constAttributes";


export class AdminSignInForm extends React.Component{
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
          <br></br>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}