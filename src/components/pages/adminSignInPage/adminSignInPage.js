import {AdminSignInForm} from "./adminSignInForm";

export const AdminSignInPage = () => {
    return(
        <>
            <div className={"adminSignInPage"}>
                <header className="App-header">
                <h1>Admin page</h1>
                <AdminSignInForm/>
                </header>
            </div>
        </>
    )
}