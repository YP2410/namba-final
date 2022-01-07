import React from "react";
import { Route, Routes } from "react-router-dom";
import AdminSignInPage from "./components/pages/adminSignInPage/adminSignInPage";
import {useAppContext} from "./lib/contextLib";
import {AdminMainPage} from "./components/pages/adminMainPage/adminMainPage";
import NotFound from "./components/pages/notFoundPage/notFoundPage";

export default function RoutesInApp() {
    const {isAuthenticated} = useAppContext();
  return (
    <Routes>
        {isAuthenticated ? (<Route exact path="/" element={<AdminMainPage/>}/>)
            : (<Route exact path="/" element={<AdminSignInPage/>}/>)}
        <Route path="*" element={<NotFound/>}/>
    </Routes>
  );
}