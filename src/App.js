import './App.css';
import React, {useState} from "react";
import AdminSignInPage from "./components/pages/adminSignInPage/adminSignInPage";
import {AdminMainPage} from "./components/pages/adminMainPage/adminMainPage";
import { AppContext } from "./lib/contextLib";

function App() {
    const [isAuthenticated, userHasAuthenticated] = useState(false);
    return (
    <div className="App">
        <header className="App-header">
            <AppContext.Provider value={{ isAuthenticated, userHasAuthenticated }}>
                {isAuthenticated ? (<AdminMainPage/>) : (<AdminSignInPage/>)}
                </AppContext.Provider>
        </header>
    </div>
  );
}

export default App;
