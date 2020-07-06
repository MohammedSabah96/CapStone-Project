import React from "react";
import {Link} from "react-router-dom";
import {useAuth0} from "@auth0/auth0-react";


const Navbar = () => {
    const {isAuthenticated} = useAuth0()
    return (
        <nav className="navbar navbar-dark bg-primary navbar-expand-lg">
            <Link to="/" className="navbar-brand">Products</Link>
            <Link to="/create" className="navbar-brand">CreateProduct</Link>
            <Link to="/profile" className="navbar-brand">Profile</Link>
            {isAuthenticated && (<Link to="/my-products" className="navbar-brand">My Products</Link>)}
        </nav>
    )
}

export default Navbar