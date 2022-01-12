import React from "react";
import { Route, Routes } from "react-router-dom";
import AdminSignInPage from "./components/pages/adminSignInPage/adminSignInPage";
import {useAppContext} from "./lib/contextLib";
import {AdminMainPage} from "./components/pages/adminMainPage/adminMainPage";
import CreatePollPage from "./components/pages/createPollPage/createPollPage";
import NotFound from "./components/pages/notFoundPage/notFoundPage";
import AddAdminPage from "./components/pages/addAdminPage/addAdminPage";
import {PollsResultsPage} from "./components/pages/pollsResultsPage/pollsResultsPage";
import {UsersPage} from "./components/pages/usersPage/usersPage";

export default function RoutesInApp() {
    const {isAuthenticated} = useAppContext();
  return (
    <Routes>
        {isAuthenticated ? (<Route exact path="/" element={<AdminMainPage/>}/>)
            : (<Route exact path="/" element={<AdminSignInPage/>}/>)}
        <Route exact path="/main" element={<AdminMainPage/>}/>
        <Route exact path="/createPoll" element={<CreatePollPage/>}/>
        <Route exact path="/pollsResults" element={<PollsResultsPage/>}/>
        <Route exact path="/usersPage" element={<UsersPage/>}/>
        <Route exact path="/addAdmin" element={<AddAdminPage/>}/>
        <Route path="*" element={<NotFound/>}/>
    </Routes>
  );
}