import React, { useState, useEffect } from "react"
import { fetchUserData } from "./api"

export const UserContext = React.createContext({
    userId: null,
    isLoggedIn: false,
    login: () => {},
    logout: () => {},
})

const UserProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false)
    const [userId, setUserId] = useState(null)

    useEffect(() => {
        if (localStorage.getItem("access_token")) {
            setIsLoggedIn(true)
            fetchUserData().then((userData) => {
                if (userData) {
                    setUserId(userData.user_id)
                }
            })
        }
    }, [])

    const login = () => {
        setIsLoggedIn(true)
    }

    const logout = () => {
        setIsLoggedIn(false)
        localStorage.removeItem("access_token")
    }

    return (
        <UserContext.Provider value={{ isLoggedIn, login, logout, userId }}>
            {children}
        </UserContext.Provider>
    )
}

export default UserProvider
