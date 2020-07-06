import React, {useEffect, useState} from "react";
import axios from 'axios'
import {useAuth0} from "@auth0/auth0-react";
import "../assets/style.css"
import CreateProduct from "./create_product";
import EditProduct from "./edit_product";
import SpecificProduct from "./get_specific_product";


const Product = (props) => {
    const {user, isAuthenticated} = useAuth0()
    const [title, setTitle] = useState("")
    const [description, setDescription] = useState("")
    const [price, setPrice] = useState("")
    const [image, setImage] = useState("")
    const [date, setDate] = useState()
    const [mobile, setMobile] = useState("")
    const [ownerUser, setOwnerUser] = useState()
    const [btn, setBtn] = useState(true)
    const [previewSource, setPreviewSource] = useState()

    useEffect(() => {
        if (props.match.path !== '/create') {
            axios.get('http://localhost:8080/api/products/' + props.match.params.id, {
                headers: {
                    Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
                },
            }).then(res => {
                setTitle(res.data.product.title)
                setDescription(res.data.product.description)
                setPrice(res.data.product.price)
                setImage(res.data.product.imageUrl)
                setDate(res.data.product.created.substring(0, 26))
                setOwnerUser(res.data.product.owner)
                setMobile(res.data.product.mobile)
            }).catch(err => console.log(err))
        }
    }, [props.match.params.id, props.match.path])

    const OnChangeTitle = (event) => {
        setTitle(event.target.value)
        setBtn(false)
    }
    const OnChangeDescription = (event) => {
        setDescription(event.target.value)
        setBtn(false)
    }
    const OnChangePrice = (event) => {
        setPrice(event.target.value)
        setBtn(false)
    }
    const OnChangeImage = (event) => {
        const file = event.target.files[0]
        const fsize = file.size;
        const file_size = Math.round((fsize / 1024));
        // The size of the file.
        if (file_size >= 500) {
            alert(
                "File too Big, please select a file less than 0.5mb");
            setBtn(true)
        } else {
            previewFile(file)
        }
        setBtn(false)

    }


    const OnChangeMobile = (event) => {
        setMobile(event.target.value)
        setBtn(false)
    }
    const OnSubmit = (event) => {
        event.preventDefault()
        const product = {
            title: title,
            description: description,
            price: price,
            imageUrl: previewSource,
            mobile: mobile
        }
        axios.post("http://localhost:8080/api/products?name=" + user.nickname, product, {
            headers: {
                Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
            },
        }).then(_ => window.location = '/').catch(err => {
                console.log(err.response.data)
            }
        )

    }
    const OnUpdate = (event) => {
        event.preventDefault()
        const product = {
            title: title,
            description: description,
            price: price,
            imageUrl: previewSource,
            mobile: mobile
        }
        axios.patch("http://localhost:8080/api/products/" + props.match.params.id, product, {
            headers: {
                Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
            },
        }).then(_ => setBtn(true)).catch(err => console.log(err.response.data))
        window.location = '/'
    }
    const deleteProduct = (id) => {
        axios.delete("http://localhost:8080/api/products/" + id, {
            headers: {
                Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
            },
        }).then(r => console.log(r)).catch(err => console.log(err.response.data))
    }

    const previewFile = (file) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onloadend = () => {
            setPreviewSource(reader.result)
        }
    }

    const create_update_product = () => {
        if (props.match.path === '/edit/:id') {
            return (
                <EditProduct OnChangeTitle={OnChangeTitle} OnChangeDescription={OnChangeDescription}
                             OnChangePrice={OnChangePrice} OnChangeImage={OnChangeImage}
                             OnChangeMobile={OnChangeMobile}
                             OnUpdate={OnUpdate} title={title} description={description} price={price}
                             image={image} date={date} mobile={mobile} ownerUser={ownerUser} btn={btn}
                             previewSource={previewSource}/>
            )
        } else if (props.match.path === '/products/:id') {
            return (
                <SpecificProduct user={user} title={title} description={description} price={price}
                                 image={image} date={date} mobile={mobile} ownerUser={ownerUser}
                                 deleteProduct={deleteProduct} id={props.match.params.id}/>
            )
        } else if (props.match.path === '/create') {
            return (
                <CreateProduct isAuthenticated={isAuthenticated} OnChangeTitle={OnChangeTitle}
                               OnChangeDescription={OnChangeDescription} OnChangePrice={OnChangePrice}
                               OnChangeImage={OnChangeImage} OnChangeMobile={OnChangeMobile} OnSubmit={OnSubmit}
                               previewSource={previewSource}/>
            )
        }
    }


    return (
        <div className="container">
            {create_update_product()}
        </div>
    )
}

export default Product