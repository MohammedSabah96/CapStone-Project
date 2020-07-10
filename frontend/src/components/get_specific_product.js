import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faEdit, faTrash} from "@fortawesome/free-solid-svg-icons";

const SpecificProduct = (props) => (
    <div className="card min-vh-100 card-block w-100">
        <img src={props.image} height="800px" className="card w-100" alt="img"/>
        <div className="card-body text-center">
            <h5 className="card-title">Title: {props.title}</h5>
            <p className="card-text">Description: {props.description}</p>
            <p className="card-text">Price: {props.price}</p>
            <p className="card-text">Owner: {props.ownerUser}</p>
            <p className="card-text">Mobile Number: {props.mobile}</p>
            <p className="card-text"><small className="text-muted">Last Update: {props.date} </small></p>
            {(props.user.email === 'admin@admin.com' &&
                <div>
                    <a className="mr-1" href={"/edit/" + props.id}>
                        <FontAwesomeIcon size="lg" icon={faEdit}/>
                    </a> |
                    <a className="ml-2" href="/" onClick={() => {
                        props.deleteProduct(props.id)
                    }}>
                        <FontAwesomeIcon size="lg" icon={faTrash}/>
                    </a>
                </div>) ||
            (props.user.nickname === props.ownerUser &&
                <div>
                    <a className="mr-1" href={"/edit/" + props.id}>
                        <FontAwesomeIcon size="lg" icon={faEdit}/>
                    </a> |
                    <a className="ml-2" href="/" onClick={() => {
                        props.deleteProduct(props.id)
                    }}>
                        <FontAwesomeIcon size="lg" icon={faTrash}/>
                    </a>
                </div>)
            }
        </div>
    </div>
)

export default SpecificProduct