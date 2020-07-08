import React, {useEffect, useState} from "react";
import axios from "axios";
import Loading from "./Loading";

const Announcement = (props) => {
    const [announcement, setAnnouncement] = useState()
    const [loading, setLoading] = useState(false)
    useEffect(() => {
        if (props.path !== "/profile") {
            setLoading(true)
            axios.get("http://localhost:8080/api/announcement/" + props.match.params.id, {
                headers: {
                    Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
                },
            }).then(res => {
                setAnnouncement(res.data.announcement.announcement)
                setLoading(false)
            }).catch(err => {
                    console.log(err.response.data)
                }
            )
        }
    }, [props.path])
    const OnChangeAnnouncement = (event) => {
        setAnnouncement(event.target.value)
    }
    const createAnnouncement = (event) => {
        event.preventDefault()
        const AD = {
            'announcement': announcement
        }
        axios.post('http://localhost:8080/api/announcement', AD, {
            headers: {
                Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
            },
        }).then(res => console.log(res)).catch(err => {
                console.log(err.response.data)
            }
        )
        const ad = document.getElementById('ad')
        ad.value = ""

    }

    const updateAnnouncement = (event) => {
        event.preventDefault()
        const AD = {
            'announcement': announcement
        }
        axios.patch('http://localhost:8080/api/announcement/' + props.match.params.id, AD, {
            headers: {
                Authorization: `Bearer ${window.localStorage.getItem("access_token")}`,
            },
        }).then(res => window.location = '/').catch(err => {
                console.log(err.response.data)
            }
        )
    }

    const create_update_announcement = () => {
        if (props.path === "/profile") {
            return (
                <form onSubmit={createAnnouncement} className="form-inline mb-2">
                    <div className="form-group w-75">
                        <input id="ad" className="form-control form-control-lg w-100" type="text"
                               placeholder="Create Announcement" onChange={OnChangeAnnouncement} required/>
                    </div>
                    <button type="submit" className="btn btn-primary btn-lg w-25">Add Announcement</button>
                </form>
            )
        } else if (props.match.path === "/announcement/edit/:id") {
            return (
                <form onSubmit={updateAnnouncement} className="form-inline mb-2">
                    <div className="form-group w-75">
                        <input id="ad" className="form-control form-control-lg w-100"
                               type="text" value={announcement || ""}
                               onChange={OnChangeAnnouncement} required/>
                    </div>
                    <button type="submit" className="btn btn-primary btn-lg w-25">Update Announcement</button>
                </form>
            )
        }
    }


    return (
        <div className="container">
            {loading ? <Loading/> : create_update_announcement()}
        </div>
    )
}

export default Announcement