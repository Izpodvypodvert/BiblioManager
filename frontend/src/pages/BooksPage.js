import React, { useState, useEffect, useContext } from "react"
import { fetchBooks, borrowBook } from "../utils/api"
import { useTableColumns } from "../components/TableColumns"
import { Table } from "../components/Table"
import { UserContext } from "../utils/context"
import Message from "../components/Message"

const BooksPage = () => {
    const [books, setBooks] = useState([])
    const [message, setMessage] = useState("")
    const { isLoggedIn } = useContext(UserContext)

    useEffect(() => {
        const getBooks = async () => {
            const data = await fetchBooks()
            setBooks(data)
        }
        getBooks()
    }, [])

    const handleBorrowBook = async (bookId) => {
        if (!isLoggedIn) {
            alert("Для резервирования книги необходимо войти в систему.")
            return
        }
        await borrowBook(bookId, setMessage)
        const updatedBooks = await fetchBooks()
        setBooks(updatedBooks)
    }

    const columns = useTableColumns(handleBorrowBook)

    return (
        <div>
            <Message text={message} />
            <Table columns={columns} data={books} />
        </div>
    )
}

export default BooksPage
