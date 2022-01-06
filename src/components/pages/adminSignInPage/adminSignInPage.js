import React, {useState} from 'react';
import {AdminSignInForm} from "./adminSignInForm";
import {SignInForm} from "./adminSignInForm";

const AdminSignInPage = () => {
    return(
                <header className="App-header">
                <h1>Admin page</h1>
                <SignInForm/>
                </header>
    )
}

export default AdminSignInPage;