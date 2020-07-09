import React, {useState} from "react";

const Message = ({msg}) => {
    const [isActive, setIsActive] = useState(true)
    const toggle = () => {
        setIsActive(false)
    }

    return (
        (isActive) ? <div id="alert" className="alert alert-info alert-dismissible fade show" role="alert">
            {msg}
            <button type="button" className="close" onClick={() => toggle()} data-dismiss="alert"
                    aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div> : null
    )
}


export default Message