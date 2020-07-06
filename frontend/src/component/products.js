import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import axios from 'axios'
import {useAuth0} from "@auth0/auth0-react";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faEdit, faTrash} from '@fortawesome/free-solid-svg-icons'

const Product = props => (
    <div className="card-group d-inline-flex w-25">
        <div className="card overflow-hidden position-relative ">
            <img alt="product" className="d-inline-block" src={props.product.imageUrl} height={190}/>
            <div className="card-body">
                {props.isAuthenticated ? (
                    <Link to={"/products/" + props.product.id}><h5
                        className="card-title">Title: {props.product.title}</h5>
                    </Link>) : (<h5 className="card-title">Title: {props.product.title}</h5>)}
                <p className="card-text">Price: {props.product.price}</p>
                <p className="card-text">Owner: {props.product.owner}</p>
                <div className="card-text">
                    <small className="text-muted">Last Update: {props.product.created.substring(0, 26)}</small>
                </div>
                <div className="d-inline-block w-100 h-25">
                    {(props.user.email === 'admin@admin.com' &&
                        <div className="float-right">
                            <Link className="mr-1" to={"/edit/" + props.product.id}>
                                <FontAwesomeIcon size="lg" icon={faEdit}/>
                            </Link> |
                            <button className="bg-white ml-1 border-0 btn-link" onClick={() => {
                                props.deleteProduct(props.product.id)
                            }}>
                                <FontAwesomeIcon size="lg" icon={faTrash}/>
                            </button>
                        </div>) ||
                    (props.user.nickname === props.product.owner &&
                        <div className="float-right">
                            <Link className="mr-1" to={"/edit/" + props.product.id}>
                                <FontAwesomeIcon size="lg" icon={faEdit}/>
                            </Link> |
                            <button className="bg-white ml-1 border-0 btn-link" onClick={() => {
                                props.deleteProduct(props.product.id)
                            }}>
                                <FontAwesomeIcon size="lg" icon={faTrash}/>
                            </button>
                        </div>)}
                </div>
            </div>
        </div>
    </div>
)


const Products = (props) => {
    const [data, setData] = useState([])
    const [userData, setUserData] = useState([])
    const [state, setState] = useState(true)
    const {isAuthenticated, getAccessTokenSilently, user} = useAuth0();
    useEffect(() => {
        if (props.match.path === "/") {
            axios.get("http://localhost:8080/api/products").then((res) => {
                setData(res.data.products)
                setState(true)
            }).catch((err) => {
                setState(false)
                console.log(err.response.data)
            })
        } else if (props.match.path === "/my-products") {
            axios.get("http://localhost:8080/api/products/my-products?name=" + user.nickname, {
                headers: {
                    Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
                },
            }).then(res => {
                setUserData(res.data.products)
                setState(true)
            }).catch(err => {
                setState(false)
                console.log(err.response.data)
            })
        }
        if (isAuthenticated) {
            getAccessTokenSilently().then(token => window.localStorage.setItem("access_token", token))
        }
    }, [isAuthenticated, getAccessTokenSilently, user.nickname, props.match.path])

    const deleteProduct = (id) => {
        axios.delete("http://localhost:8080/api/products/" + id, {
            headers: {
                Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
            },
        }).then(res => console.log(res.data)).catch(err => console.log(err.response.data))
        setData(data.filter(el => el.id !== id))
        setUserData(userData.filter(el => el.id !== id))
    }
    const productsList = () => {
        if (props.match.path === "/") {
            return data.map(currentProduct => {
                return <Product product={currentProduct} deleteProduct={deleteProduct} key={currentProduct.id}
                                isAuthenticated={isAuthenticated} user={user}/>
            })
        } else if (props.match.path === "/my-products") {
            return userData.map(currentProduct => {
                return <Product product={currentProduct} deleteProduct={deleteProduct} key={currentProduct.id}
                                isAuthenticated={isAuthenticated} user={user}/>
            })
        }

    }

    return (
        <div className="container">
            {state ? productsList() :
                <div className="text-center mt-5">There is no Products Found, please add some.</div>}
        </div>
    );
}

export default Products