import React from "react";
import Message from "./message";
import "../assets/style.css"
import {CircularProgressbar} from "react-circular-progressbar";

const CreateProduct = (props) => (
    <div className="container">
        {props.message ? <Message msg={props.message}/> : null}
        {props.isSubmit ? <div className="min-vh-100 card card-block">
                <CircularProgressbar className="w-50 center-block"
                                     value={props.uploadPercentageSubmit}
                                     text={`${props.uploadPercentageSubmit}%`}/></div>
            :
            <div>
                <h3>Create Product</h3>
                {props.isAuthenticated ?
                    <form onSubmit={props.OnSubmit} encType="multipart/form-data">
                        <div className="form-group">
                            <label htmlFor="title">Title</label>
                            <input type="text" id="title" onChange={props.OnChangeTitle} className="form-control"
                                   placeholder="Title" required/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="description">Description</label>
                            <textarea className="form-control" id="description" onChange={props.OnChangeDescription}
                                      rows="3"
                                      placeholder="Description" required/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="price">Price</label>
                            <input type="number" id="price" onChange={props.OnChangePrice} className="form-control"
                                   placeholder="0$"
                                   required/>
                        </div>
                        <div className="custom-file">
                            {props.previewSource && (
                                <img className="card mb-2" height="300px" src={props.previewSource} alt=""/>)}
                            <input type="file" id="image" onChange={props.OnChangeImage} className="custom-file-input"
                                   required/>
                            <label className="custom-file-label" htmlFor="image">{props.fileName}</label>
                        </div>
                        <div style={{"visibility": "hidden"}} id="bar" className="progress">
                            <div className="progress-bar" style={{"width": `${props.uploadPercentageImage}%`}}
                                 role="progressbar">{props.uploadPercentageImage}</div>
                        </div>
                        <div className="form-group">
                            <label htmlFor="mobile">Mobile Number</label>
                            <input type="number" id="mobile" onChange={props.OnChangeMobile} className="form-control"
                                   required/>
                        </div>
                        <button type="submit" className="btn btn-primary mt-2">Create Product</button>
                    </form>
                    : <div className="Bold text-center border rounded-pill mt-lg-5">Please You need To Login
                        first</div>}</div>
        }


    </div>
)

export default CreateProduct;