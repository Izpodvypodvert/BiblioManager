import React, { useState } from "react"
import RegisterForm from "../components/RegisterForm"
import { register } from "../utils/api"

const RegisterPage = () => {
    const [message, setMessage] = useState("")
    const handleRegister = async (
        username,
        email,
        password,
        confirmPassword
    ) => {
        console.log("Register:", username, email, password, confirmPassword)
        await register(username, email, password, setMessage)
    }

    return (
        <div>
            {message && <div className="message">{message}</div>}
            <RegisterForm onRegister={handleRegister} />
        </div>
    )
}

export default RegisterPage
