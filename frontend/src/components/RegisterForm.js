import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import "./registerform.css"

const RegisterForm = ({ onRegister }) => {
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [error, setError] = useState("")
    const navigate = useNavigate()
    const handleSubmit = (event) => {
        event.preventDefault()
        if (password !== confirmPassword) {
            setError("Пароли не совпадают.")
            return
        }
        setError("")
        onRegister(username, email, password, confirmPassword)
        navigate("/login")
    }

    return (
        <div className="register-container">
            <h2>Регистрация</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="username">Имя пользователя:</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Пароль:</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="confirm-password">
                        Подтвердите пароль:
                    </label>
                    <input
                        type="password"
                        id="confirm-password"
                        name="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <div className="error-message">{error}</div>}
                <button type="submit">Зарегистрироваться</button>
            </form>
        </div>
    )
}

export default RegisterForm
