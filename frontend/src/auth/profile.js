import React from "react";
import {useAuth0} from "@auth0/auth0-react";

const Profile = () => {
    const {user, loginWithRedirect, logout, isAuthenticated} = useAuth0();
    return (
        isAuthenticated ? (
            <div className="container text-center">
                <h2 className="mt-5">Name: {user.nickname}</h2>
                <p className="mb-5">Email: {user.email}</p>
                <div><textarea rows="9" cols="150"
                               defaultValue={window.localStorage.getItem("access_token")}/>
                </div>
                <button className="btn btn-primary btn-lg" onClick={() => {
                    logout();
                    window.localStorage.setItem("access_token", "")
                }}>Logout
                </button>
            </div>
        ) : (
            <div>
                <button className="btn btn-primary btn-lg" onClick={() => loginWithRedirect()}>Login</button>
            </div>
        )
    );
};

export default Profile
