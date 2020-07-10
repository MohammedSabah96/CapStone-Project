import React from "react";
import Message from "./message";
import "../assets/style.css"
import {CircularProgressbar} from "react-circular-progressbar";

const EditProduct = (props) => (
    <div>
        {props.message ? <Message msg={props.message}/> : null}
        {props.isSubmit ? <div className="min-vh-100 card card-block">
            <CircularProgressbar className="w-50 center-block"
                                 value={props.uploadPercentageSubmit}
                                 text={`${props.uploadPercentageSubmit}%`}/></div> : null}
        <h3>Edit Product</h3>
        <form onSubmit={props.OnUpdate}>
            <div className="form-group">
                <label htmlFor="title">Title</label>
                <input type="text" id="title" value={props.title} onChange={props.OnChangeTitle}
                       className="form-control"
                       placeholder="Title" required/>
            </div>
            <div className="form-group">
                <label htmlFor="description">Description</label>
                <textarea className="form-control" value={props.description} id="description"
                          onChange={props.OnChangeDescription} rows="3"
                          placeholder="Description" required/>
            </div>
            <div className="form-group">
                <label htmlFor="price">Price</label>
                <input type="number" value={props.price.replace(/\$/g, '')} id="price"
                       onChange={props.OnChangePrice}
                       className="form-control"
                       placeholder="0$"
                       required/>
            </div>
            <div className="custom-file">
                {(props.previewSource && (
                        <img className="card mb-2" height="300px" src={props.previewSource} alt=""/>)
                ) || (props.image && (
                    <img className="card mb-2" height="300px" src={props.image} alt=""/>))
                }
                <input type="file" id="image" onChange={props.OnChangeImage} className="custom-file-input"/>
                <label className="custom-file-label" htmlFor="image">{props.fileName}</label>
            </div>
            <div style={{"visibility": "hidden"}} id="bar" className="progress">
                <div className="progress-bar" style={{"width": `${props.uploadPercentageImage}%`}}
                     role="progressbar">{props.uploadPercentageImage}</div>
            </div>
            <div className="form-group">
                <label htmlFor="mobile">Mobile Number</label>
                <input type="number" value={props.mobile} id="mobile" onChange={props.OnChangeMobile}
                       className="form-control"
                       required/>
            </div>
            <button disabled={props.btn} type="submit" className="btn btn-primary mt-2">Update Product</button>
        </form>
    </div>
)

export default EditProduct