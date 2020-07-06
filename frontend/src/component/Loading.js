import React from "react";
import loading from "../assets/loading.svg";
import "../assets/style.css"

const Loading = () => (
    <div className="spinner min-vh-100 card card-block">
        <img className="w-25 center-block" src={loading}
             alt="Loading"/>
    </div>
);

export default Loading;
