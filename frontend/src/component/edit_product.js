import React from "react";

const EditProduct = (props) => (
    <div>
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
            <div className="form-group">
                <label htmlFor="image">Image</label>
                {(props.previewSource && (
                        <img className="card mb-2" height="300px" src={props.previewSource} alt=""/>)
                ) || (props.image && (
                    <img className="card mb-2" height="300px" src={props.image} alt=""/>))
                }
                <input type="file" id="image" onChange={props.OnChangeImage} className="form-control"/>
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