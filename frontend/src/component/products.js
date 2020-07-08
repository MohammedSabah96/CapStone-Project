import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import axios from 'axios'
import {useAuth0} from "@auth0/auth0-react";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faEdit, faTrash, faTimes, faPen} from '@fortawesome/free-solid-svg-icons'
import "../assets/styleBtn.css"

const Product = (props) => (
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

const Announcement = (props) => (
    <div className="row">
        <div className="col  mb-2 bg-warning text-dark d-flex justify-content-between">
            <label
                className="font-weight-bold  pt-1">{props.announcement.announcement}</label>
            {props.user.email === "admin@admin.com" && (
                <div className="pt-1">
                    <Link to={"/announcement/edit/" + props.announcement.id}>
                        <FontAwesomeIcon className="text-dark" icon={faPen}/>
                    </Link>
                    <button className="btn-warning border-0 ml-2"
                            onClick={() => props.deleteAnnouncement(props.announcement.id)}>
                        <FontAwesomeIcon icon={faTimes}/>
                    </button>
                </div>
            )}
        </div>
    </div>
)


const Products = (props) => {
    const TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxDMDl5czMzdGs4d1FuaGNiM0dyQyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlLXNoby5hdXRoMC5jb20vIiwic3ViIjoieWNLQ05MTHpPTmFQeE9XemZYczVQYUFPQ2xNanNNZDdAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vY29mZmUtc2hvLmF1dGgwLmNvbS9hcGkvdjIvIiwiaWF0IjoxNTk0MTM5MzUxLCJleHAiOjE1OTQyMjU3NTEsImF6cCI6InljS0NOTEx6T05hUHhPV3pmWHM1UGFBT0NsTWpzTWQ3Iiwic2NvcGUiOiJyZWFkOmNsaWVudF9ncmFudHMgY3JlYXRlOmNsaWVudF9ncmFudHMgZGVsZXRlOmNsaWVudF9ncmFudHMgdXBkYXRlOmNsaWVudF9ncmFudHMgcmVhZDp1c2VycyB1cGRhdGU6dXNlcnMgZGVsZXRlOnVzZXJzIGNyZWF0ZTp1c2VycyByZWFkOnVzZXJzX2FwcF9tZXRhZGF0YSB1cGRhdGU6dXNlcnNfYXBwX21ldGFkYXRhIGRlbGV0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgY3JlYXRlOnVzZXJzX2FwcF9tZXRhZGF0YSByZWFkOnVzZXJfY3VzdG9tX2Jsb2NrcyBjcmVhdGU6dXNlcl9jdXN0b21fYmxvY2tzIGRlbGV0ZTp1c2VyX2N1c3RvbV9ibG9ja3MgY3JlYXRlOnVzZXJfdGlja2V0cyByZWFkOmNsaWVudHMgdXBkYXRlOmNsaWVudHMgZGVsZXRlOmNsaWVudHMgY3JlYXRlOmNsaWVudHMgcmVhZDpjbGllbnRfa2V5cyB1cGRhdGU6Y2xpZW50X2tleXMgZGVsZXRlOmNsaWVudF9rZXlzIGNyZWF0ZTpjbGllbnRfa2V5cyByZWFkOmNvbm5lY3Rpb25zIHVwZGF0ZTpjb25uZWN0aW9ucyBkZWxldGU6Y29ubmVjdGlvbnMgY3JlYXRlOmNvbm5lY3Rpb25zIHJlYWQ6cmVzb3VyY2Vfc2VydmVycyB1cGRhdGU6cmVzb3VyY2Vfc2VydmVycyBkZWxldGU6cmVzb3VyY2Vfc2VydmVycyBjcmVhdGU6cmVzb3VyY2Vfc2VydmVycyByZWFkOmRldmljZV9jcmVkZW50aWFscyB1cGRhdGU6ZGV2aWNlX2NyZWRlbnRpYWxzIGRlbGV0ZTpkZXZpY2VfY3JlZGVudGlhbHMgY3JlYXRlOmRldmljZV9jcmVkZW50aWFscyByZWFkOnJ1bGVzIHVwZGF0ZTpydWxlcyBkZWxldGU6cnVsZXMgY3JlYXRlOnJ1bGVzIHJlYWQ6cnVsZXNfY29uZmlncyB1cGRhdGU6cnVsZXNfY29uZmlncyBkZWxldGU6cnVsZXNfY29uZmlncyByZWFkOmhvb2tzIHVwZGF0ZTpob29rcyBkZWxldGU6aG9va3MgY3JlYXRlOmhvb2tzIHJlYWQ6YWN0aW9ucyB1cGRhdGU6YWN0aW9ucyBkZWxldGU6YWN0aW9ucyBjcmVhdGU6YWN0aW9ucyByZWFkOmVtYWlsX3Byb3ZpZGVyIHVwZGF0ZTplbWFpbF9wcm92aWRlciBkZWxldGU6ZW1haWxfcHJvdmlkZXIgY3JlYXRlOmVtYWlsX3Byb3ZpZGVyIGJsYWNrbGlzdDp0b2tlbnMgcmVhZDpzdGF0cyByZWFkOnRlbmFudF9zZXR0aW5ncyB1cGRhdGU6dGVuYW50X3NldHRpbmdzIHJlYWQ6bG9ncyByZWFkOnNoaWVsZHMgY3JlYXRlOnNoaWVsZHMgdXBkYXRlOnNoaWVsZHMgZGVsZXRlOnNoaWVsZHMgcmVhZDphbm9tYWx5X2Jsb2NrcyBkZWxldGU6YW5vbWFseV9ibG9ja3MgdXBkYXRlOnRyaWdnZXJzIHJlYWQ6dHJpZ2dlcnMgcmVhZDpncmFudHMgZGVsZXRlOmdyYW50cyByZWFkOmd1YXJkaWFuX2ZhY3RvcnMgdXBkYXRlOmd1YXJkaWFuX2ZhY3RvcnMgcmVhZDpndWFyZGlhbl9lbnJvbGxtZW50cyBkZWxldGU6Z3VhcmRpYW5fZW5yb2xsbWVudHMgY3JlYXRlOmd1YXJkaWFuX2Vucm9sbG1lbnRfdGlja2V0cyByZWFkOnVzZXJfaWRwX3Rva2VucyBjcmVhdGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiBkZWxldGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiByZWFkOmN1c3RvbV9kb21haW5zIGRlbGV0ZTpjdXN0b21fZG9tYWlucyBjcmVhdGU6Y3VzdG9tX2RvbWFpbnMgdXBkYXRlOmN1c3RvbV9kb21haW5zIHJlYWQ6ZW1haWxfdGVtcGxhdGVzIGNyZWF0ZTplbWFpbF90ZW1wbGF0ZXMgdXBkYXRlOmVtYWlsX3RlbXBsYXRlcyByZWFkOm1mYV9wb2xpY2llcyB1cGRhdGU6bWZhX3BvbGljaWVzIHJlYWQ6cm9sZXMgY3JlYXRlOnJvbGVzIGRlbGV0ZTpyb2xlcyB1cGRhdGU6cm9sZXMgcmVhZDpwcm9tcHRzIHVwZGF0ZTpwcm9tcHRzIHJlYWQ6YnJhbmRpbmcgdXBkYXRlOmJyYW5kaW5nIGRlbGV0ZTpicmFuZGluZyByZWFkOmxvZ19zdHJlYW1zIGNyZWF0ZTpsb2dfc3RyZWFtcyBkZWxldGU6bG9nX3N0cmVhbXMgdXBkYXRlOmxvZ19zdHJlYW1zIGNyZWF0ZTpzaWduaW5nX2tleXMgcmVhZDpzaWduaW5nX2tleXMgdXBkYXRlOnNpZ25pbmdfa2V5cyByZWFkOmxpbWl0cyB1cGRhdGU6bGltaXRzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.TXjvcyuloEKxHccBjO94KKt7csN3VETAnx-eVOJv3286RJleRzjRfO4QEeM0vQBJcHaQqrG_U5u6yc9_BSbMEFNZNdEqT2p6uX4xjHHFi2St4EUBgHU1lhPSTd0QPcagxE-nUhCMCqrKNYFluu27uQw1rpKn2FjWH7-vDfP-tgvznwshGmzKov86bQ0ylkXpMboXXW8HkskOdYdeWJU-Az9FtrHHkpLL7PmIRqdyMPq5jxw-Zp4FUeTDFK4rExAvL7g0fvCnBM3NheLBGXgngEenIf7n4CsaXPCHWDeefoxZd0RDnM8oBw44k3t0XUaB-38GLH5setPKqAraneKoGQ"
    const [data, setData] = useState([])
    const [userData, setUserData] = useState([])
    const [state, setState] = useState(true)
    const {isAuthenticated, getAccessTokenSilently, user} = useAuth0();
    const [announcement, setAnnouncement] = useState([])
    useEffect(() => {
        if (props.match.path === "/") {
            axios.get("http://localhost:8080/api/products").then((res) => {
                setData(res.data.products)
                setAnnouncement(res.data.announcements)
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
            axios.get(`https://coffe-sho.auth0.com/api/v2/users/${user.sub}/roles`, {
                headers: {
                    Authorization: TOKEN,
                },
            }).then(res => {
                    if (!window.localStorage.getItem("access_token")) {
                        if (res.data.length === 0) {
                            axios.post(`https://coffe-sho.auth0.com/api/v2/users/${user.sub}/roles`, {"roles": ["rol_RYjEmBTUX3czmyAs"]}, {
                                headers: {
                                    Authorization: TOKEN,
                                },
                            }).then(_ => {
                                    getAccessTokenSilently().then(token => {
                                        window.localStorage.setItem("access_token", token)
                                    })
                                }
                            ).catch(res => console.log(res))
                        } else if (res.data[0].name === "admin") {
                            getAccessTokenSilently().then(token => {
                                window.localStorage.setItem("access_token", token)
                            })
                        } else if (res.data[0].name === "user") {
                            getAccessTokenSilently().then(token => {
                                window.localStorage.setItem("access_token", token)
                            })
                        }
                    }

                }
            ).catch(res => console.log(res))
        }
    }, [isAuthenticated, user.sub, getAccessTokenSilently, user.nickname, props.match.path])

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


    const deleteAnnouncement = (id) => {
        axios.delete("http://localhost:8080/api/announcement/" + id, {
            headers: {
                Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
            },
        }).then(res => console.log(res.data)).catch(err => console.log(err.response.data))
        setAnnouncement(announcement.filter(el => el.id !== id))
    }


    const announcementsList = () => {
        return announcement.map(currentAnnouncement => {
            return <Announcement announcement={currentAnnouncement} deleteAnnouncement={deleteAnnouncement}
                                 key={currentAnnouncement.id} user={user}/>
        })
    }


    return (
        <div className="container">
            {announcementsList()}
            {state ? productsList() :
                <div className="text-center mt-5">There is no Products Found, please add some.</div>}
        </div>
    );
}

export default Products