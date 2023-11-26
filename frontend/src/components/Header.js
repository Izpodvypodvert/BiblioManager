import React, { useContext } from "react"
import { Link, useLocation, useNavigate } from "react-router-dom"
import { UserContext } from "../utils/context"
import "./header.css"

export const Header = () => {
    const { isLoggedIn, logout } = useContext(UserContext)
    const location = useLocation()
    const navigate = useNavigate()
    let link

    const handleLogout = () => {
        logout()
        navigate("/login")
    }

    if (location.pathname === "/") {
        link = isLoggedIn ? (
            <button className="header-link" onClick={handleLogout}>
                Выйти
            </button>
        ) : (
            <Link to="/login" className="header-link">
                Войти
            </Link>
        )
    } else {
        link = (
            <Link to="/" className="header-link">
                На главную
            </Link>
        )
    }

    return (
        <header className="header">
            <div className="header-title">BiblioManager</div>
            <nav>
                <Link to="/my-books" className="header-link">
                    Мои книги
                </Link>
            </nav>
            <nav>{link}</nav>
        </header>
    )
}
