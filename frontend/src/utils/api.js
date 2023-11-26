export const fetchBooks = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/books/")
        if (!response.ok) {
            throw new Error("Network response was not ok")
        }
        const data = await response.json()
        return data
    } catch (error) {
        console.error("Error fetching data:", error)
        return []
    }
}

export const login = async (username, password) => {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/token/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        })

        if (!response.ok) {
            throw new Error("Проблема при получении токена")
        }

        const data = await response.json()

        localStorage.setItem("access_token", data.access)
    } catch (error) {
        console.error("Ошибка входа:", error)
    }
}

export const borrowBook = async (bookId, setMessage) => {
    try {
        const response = await fetch(
            `http://127.0.0.1:8000/api/v1/borrow-book/${bookId}/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem(
                        "access_token"
                    )}`,
                },
            }
        )

        if (response.ok) {
            setMessage("Книга успешно зарезервирована")
        } else {
            setMessage("Достигнут лимит по числу зарезервированных книг!")
        }
    } catch (error) {
        setMessage("Ошибка сети при резервировании книги")
    }
}

export const fetchUserData = () => {
    return fetch("http://127.0.0.1:8000/api/v1/me/", {
        headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
    })
        .then((response) => {
            if (response.ok) {
                return response.json()
            } else {
                localStorage.removeItem("access_token")
                throw new Error("Ошибка при запросе данных пользователя")
            }
        })
        .then((data) => {
            return data //
        })
        .catch((error) => {
            localStorage.removeItem("access_token")
            console.error("Ошибка при получении данных пользователя:", error)
        })
}

export const fetchUserLoanedBooks = async () => {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/v1/user-book-loans/",
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem(
                        "access_token"
                    )}`,
                },
            }
        )
        if (!response.ok) {
            throw new Error("Ошибка сети")
        }
        const data = await response.json()
        return data
    } catch (error) {
        console.error("Ошибка при извлечении данных:", error)
        return []
    }
}

export const returnBook = async (bookId, setMessage) => {
    try {
        const response = await fetch(
            `http://127.0.0.1:8000/api/v1/return-book/${bookId}/`,
            {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem(
                        "access_token"
                    )}`,
                },
            }
        )

        if (response.ok) {
            setMessage("Книга успешно возвращена")
        } else {
            setMessage("Ошибка при возврате книги")
        }
    } catch (error) {
        setMessage("Ошибка сети при возврате книги")
    }
}

export const register = async (username, email, password, setMessage) => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/v1/register/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, email, password }),
        })

        if (response.ok) {
            setMessage("Пользователь успешно зарегестрирован")
        } else {
            setMessage("Ошибка при регистрации пользователя")
        }
    } catch (error) {
        setMessage("Ошибка сети")
    }
}
