import React from "react"
import { BrowserRouter, Route, Routes } from "react-router-dom"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import BooksPage from "./pages/BooksPage"
import UserBooksPage from "./pages/UserBooksPage"
import { Header } from "./components/Header"
import UserProvider from "./utils/context"

function App() {
    return (
        <UserProvider>
            <BrowserRouter>
                <Header />
                <Routes>
                    <Route exact path="/" element={<BooksPage />} />
                    <Route path="/my-books" element={<UserBooksPage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                </Routes>
            </BrowserRouter>
        </UserProvider>
    )
}

export default App
