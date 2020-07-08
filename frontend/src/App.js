import React from 'react';
import {BrowserRouter as Router, Route, Switch} from "react-router-dom"
import "bootstrap/dist/css/bootstrap.min.css"
import Navbar from "./component/navbar"
import Products from "./component/products";
import Product from "./component/product";
import Profile from "./auth/profile";
import {useAuth0} from "@auth0/auth0-react";
import Loading from "./component/Loading";
import Announcement from "./component/announcement";

function App() {
    const {isLoading, error} = useAuth0();
    if (error) {
        return <div>Oops... {error.message}</div>;
    }
    if (isLoading) {
        return <Loading/>;
    }
    return (
        <Router>
            <div className="container">
                <Navbar/>
                <br/>
                <Switch>
                    <Route path="/" exact component={Products}/>
                    <Route path="/edit/:id" component={Product}/>
                    <Route path="/announcement/edit/:id" component={Announcement}/>
                    <Route path="/products/:id" component={Product}/>
                    <Route path="/create" component={Product}/>
                    <Route path="/profile" component={Profile}/>
                    <Route path="/my-products" component={Products}/>
                </Switch>
            </div>
        </Router>
    );
}

export default App;
