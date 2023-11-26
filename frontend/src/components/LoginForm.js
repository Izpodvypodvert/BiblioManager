import React, { useContext, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { UserContext } from "../utils/context"
import "./loginform.css"

const LoginForm = ({ onLogin }) => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const { login } = useContext(UserContext)

    const navigate = useNavigate()

    const handleSubmit = (event) => {
        event.preventDefault()
        onLogin(username, password)
        navigate("/")
        login()
    }

    return (
        <div className="login-container">
            <h2>Вход в систему</h2>
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
                <button type="submit">Войти</button>
            </form>
            <div className="register-link">
                Ещё не зарегистрированы?{" "}
                <Link to="/register">Зарегистрироваться</Link>.
            </div>
        </div>
    )
}

export default LoginForm
