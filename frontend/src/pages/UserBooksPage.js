import React, { useState, useEffect } from "react"
import { fetchUserLoanedBooks, returnBook } from "../utils/api"
import { useUserTableColumns } from "../components/UserTableColumns"
import { Table } from "../components/Table"
import Message from "../components/Message"

const UserBooksPage = () => {
    const [books, setBooks] = useState([])
    const [message, setMessage] = useState("")

    useEffect(() => {
        const getBooks = async () => {
            const data = await fetchUserLoanedBooks()
            setBooks(data)
        }
        getBooks()
    }, [])

    const handleReturnBook = async (bookId) => {
        await returnBook(bookId, setMessage)
        const updatedBooks = await fetchUserLoanedBooks()
        setBooks(updatedBooks)
    }
    const columns = useUserTableColumns(handleReturnBook)

    return (
        <>
            <Message text={message} />
            <Table columns={columns} data={books} />
        </>
    )
}

export default UserBooksPage
