import './App.css';
import Button from "react-bootstrap/Button";
import './index.css'
import React, {useEffect, useState} from "react";
import { AppContext } from "./lib/contextLib";
import RoutesInApp from "./RoutesInApp";
import httpClient from "./httpClient";
import {APIBase} from "./constAttributes";
import { useNavigate } from "react-router-dom";


/*          not sure if to add yet, need to think if necessary and looks good...

<Navbar collapseOnSelect bg="light" expand="md" className="mb-3">
                    <Navbar.Brand className="font-weight-bold text-muted">
                        Namba Final Project :-)
                    </Navbar.Brand>
                    <Navbar.Toggle/>
                </Navbar>
*/

function App() {
    const [isAuthenticated, userHasAuthenticated] = useState(false);
    const [isAuthenticating, userIsAuthenticating] = useState(false);
    const navigate = useNavigate();

    function logOut(){
        httpClient.get(APIBase + "/logout").then(r => console.log(r));
        userHasAuthenticated(false);
        let path = `/`;
        navigate(path);
    }

    useEffect(() => {
        // TODO: add a check for auth session
        //alert(isAuthenticated)
        if (!isAuthenticating) {
            userIsAuthenticating(true)
            httpClient.get(APIBase + "/cookie")
                .then(res => {
                    // console.log(res);
                    // console.log(res['data']);
                    // console.log(res['data']['result']);
                    if (res['data']['result'] !== null) {
                        userHasAuthenticated(true)
                    }
                    userIsAuthenticating(false)
                });
        }
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <Button className="logout-btn" onClick={ () => logOut()}>
                    LOGOUT
                </Button>
                <AppContext.Provider value={{isAuthenticated, userHasAuthenticated, isAuthenticating, userIsAuthenticating}}>
                    <RoutesInApp/>
                </AppContext.Provider>
            </header>
        </div>
  );
}

export default App;
