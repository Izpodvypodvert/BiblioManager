import React, { useContext } from "react"
import { UserContext } from "../utils/context"

export const useTableColumns = (handleBorrowBook) => {
    const { userId } = useContext(UserContext)
    return React.useMemo(
        () => [
            {
                Header: "Название",
                accessor: "title",
            },
            {
                Header: "Автор",
                accessor: "author",
            },
            {
                Header: "Год издания",
                accessor: "publication_year",
            },
            {
                Header: "Международный стандартный книжный номер",
                accessor: "ISBN",
            },
            {
                Header: "Зарезервировать книгу",
                Cell: ({ row }) => (
                    <button
                        onClick={async () =>
                            await handleBorrowBook(row.original.id)
                        }
                    >
                        Зарезервировать
                    </button>
                ),
            },
        ],
        []
    )
}
