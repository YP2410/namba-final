import './App.css';
import React, {useEffect, useState} from "react";
import Navbar from "react-bootstrap/Navbar";
import { AppContext } from "./lib/contextLib";
import RoutesInApp from "./RoutesInApp";


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
    useEffect(() => {
        // TODO: add a check for auth session
        //alert(isAuthenticated)
    }, [isAuthenticated]);

    return (
        <div className="App">
            <header className="App-header">
                <AppContext.Provider value={{isAuthenticated, userHasAuthenticated}}>
                    <RoutesInApp/>
                </AppContext.Provider>
            </header>
        </div>
  );
}

export default App;
