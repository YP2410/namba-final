import './App.css';
import React, {useState} from "react";
import AdminSignInPage from "./components/pages/adminSignInPage/adminSignInPage";
import { AppContext } from "./lib/contextLib";

function App() {
    const [isAuthenticated, userHasAuthenticated] = useState(false);
    return (
    <div className="App">
        <header className="App-header">
            <AppContext.Provider value={{ isAuthenticated, userHasAuthenticated }}>
                {isAuthenticated ? (<h1> Is Logged In!!</h1>) : (<AdminSignInPage/>)}
                </AppContext.Provider>
        </header>
    </div>
  );
}

export default App;
