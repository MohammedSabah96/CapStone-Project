import React from "react";
import {useAuth0} from "@auth0/auth0-react";
import Announcement from "../component/announcement";

const Profile = (props) => {
        const {user, loginWithRedirect, logout, isAuthenticated, getAccessTokenSilently} = useAuth0();

        const parseJwt = (token) => {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));
            const payload = JSON.parse(jsonPayload)
            return payload.permissions.length === 0;
        }
        const getNewToken = () => {
            getAccessTokenSilently().then(token => {
                window.localStorage.setItem("access_token", token)
                window.location = '/profile'
            })
        }

        return (
            isAuthenticated ? user.email === "admin@admin.com" ? (
                    <div>
                        <Announcement path={props.match.path}/>
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
                    </div>
                ) : (
                    <div className="container text-center">
                        {parseJwt(window.localStorage.getItem("access_token")) && getNewToken()}
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
                    </div>)
                : (
                    <div>
                        <button className="btn btn-primary btn-lg" onClick={() => loginWithRedirect()}>Login</button>
                    </div>
                )
        );
    }
;

export default Profile
