import React, {useEffect, useState} from "react";
import axios from 'axios'
import {useAuth0} from "@auth0/auth0-react";
import "../assets/style.css"
import CreateProduct from "./create_product";
import EditProduct from "./edit_product";
import SpecificProduct from "./get_specific_product";
import Loading from "./Loading";
import 'react-circular-progressbar/dist/styles.css';


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
    const [loading, setLoading] = useState(false)
    const [message, setMessage] = useState("")
    const [fileName, setFileName] = useState("Choose an Image")
    const [uploadPercentageImage, setUploadPercentageImage] = useState(0)
    const [uploadPercentageSubmit, setUploadPercentageSubmit] = useState(0)
    const [imageUrl, setImageUrl] = useState("")
    const [imageId, setImageId] = useState("")
    const [deleteImage, setDeleteImage] = useState("")
    const [isSubmit, setIsSubmit] = useState(false)

    useEffect(() => {
        if (props.match.path !== '/create') {
            setLoading(true)
            axios.get('http://localhost:8080/api/products/' + props.match.params.id, {
                headers: {
                    Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
                },
            }).then(res => {
                setTitle(res.data.product.title)
                setDescription(res.data.product.description)
                setPrice(res.data.product.price)
                setImage(res.data.product.imageUrl)
                setFileName(res.data.product.imageName)
                setDate(res.data.product.created.substring(0, 26))
                setOwnerUser(res.data.product.owner)
                setMobile(res.data.product.mobile)
                setLoading(false)
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
        if (deleteImage) {
            axios.post(`https://api.cloudinary.com/v1_1/devstore-capstone/delete_by_token`, {token: deleteImage}, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(res => console.log(res)).catch(err => console.log(err.response))
        }
        const file = event.target.files[0]
        setFileName(file.name)
        const fsize = file.size;
        const file_size = Math.round((fsize / 1024));
        // The size of the file.
        if (file_size >= 1000) {
            alert(
                "File too Big, please select a file less than 1mb");
            setFileName("")
            setPreviewSource("")
            setBtn(true)
        } else {
            document.getElementById("bar").style.visibility = "visible";
            previewFile(file)
            const formData = new FormData()
            formData.append('file', file)
            formData.append('upload_preset', 'devstore-capstone')
            axios.post("https://api.cloudinary.com/v1_1/devstore-capstone/image/upload", formData, {
                onUploadProgress: progressEvent => {
                    setUploadPercentageImage(parseInt(Math.round((progressEvent.loaded * 100) / progressEvent.total)))
                    setTimeout(() => setUploadPercentageImage(0), 10000)
                }
            }).then(res => {
                setDeleteImage(res.data.delete_token)
                setImageUrl(res.data.secure_url)
                setImageId(res.data.public_id)
                window.addEventListener("beforeunload", function (event) {
                    console.log(deleteImage)
                    axios.post(`https://api.cloudinary.com/v1_1/devstore-capstone/delete_by_token`, {token: res.data.delete_token}, {
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    }).then(res => console.log(res)).catch(err => console.log(err.response))

                });
            }).catch(res => console.log(res.response))
        }
        setBtn(false)

    }
    const OnChangeMobile = (event) => {
        setMobile(event.target.value)
        setBtn(false)
    }
    const OnSubmit = (event) => {
        setIsSubmit(true)
        event.preventDefault()
        const product = {
            title: title,
            description: description,
            price: price,
            imageUrl: imageUrl,
            imageId: imageId,
            imageName: fileName,
            mobile: mobile
        }
        axios.post("http://localhost:8080/api/products?name=" + user.nickname, product, {
            headers: {
                Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
            },
            onUploadProgress: progressEvent => {
                setUploadPercentageSubmit(parseInt(Math.round((progressEvent.loaded * 100) / progressEvent.total)))
                setTimeout(() => setUploadPercentageSubmit(0), 10000)
            }
        }).then(res => {
            if (res.status === 200) {
                setMessage("The Product was Created Successfully")
                setIsSubmit(false)
            }
        }).catch(err => {
                setIsSubmit(false)
                if (err.response.status === 422) {
                    setMessage("please You need to have a unique title product")
                } else {
                    setMessage("something went wrong with the server")
                }
            }
        )
        setFileName("")
        setPreviewSource("")
        setDeleteImage("")
    }
    const OnUpdate = (event) => {
        setIsSubmit(true)
        event.preventDefault()
        const product = {
            title: title,
            description: description,
            price: price,
            imageUrl: imageUrl,
            imageId: imageId,
            imageName: fileName,
            mobile: mobile
        }
        axios.patch("http://localhost:8080/api/products/" + props.match.params.id, product, {
            headers: {
                Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
            },
            onUploadProgress: progressEvent => {
                setUploadPercentageSubmit(parseInt(Math.round((progressEvent.loaded * 100) / progressEvent.total)))
                setTimeout(() => setUploadPercentageSubmit(0), 10000)
            }
        }).then(res => {
                if (res.status === 200) {
                    setMessage("The Product was Updated Successfully")
                    setIsSubmit(false)
                }
            }
        ).catch(err => {
            setIsSubmit(false)
            if (err.response.status === 404) {
                setMessage("The Product does not exists")
            } else {
                setMessage("something went wrong with the server")
            }
        })
    }
    const deleteProduct = (id) => {
        axios.delete("http://localhost:8080/api/products/" + id, {
            headers: {
                Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
            },
        }).then(res => {
            if (res.status === 200) {
                setMessage("The Product was Deleted Successfully")
            }
            setLoading(false)
        }).catch(err => {
            if (err.response.status === 404) {
                setMessage("The Product does not exists")
            } else {
                setMessage("something went wrong with the server")
            }
        })
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
                             previewSource={previewSource} fileName={fileName}
                             uploadPercentageImage={uploadPercentageImage}
                             message={message} isSubmit={isSubmit} uploadPercentageSubmit={uploadPercentageSubmit}/>
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
                               previewSource={previewSource} fileName={fileName}
                               uploadPercentageImage={uploadPercentageImage}
                               message={message} isSubmit={isSubmit} uploadPercentageSubmit={uploadPercentageSubmit}/>
            )
        }
    }

    return (
        <div className="container">
            {loading ? <Loading/> : create_update_product()}
        </div>
    )
}

export default Product