import React from "react"

export const useUserTableColumns = (handleReturnBook) => {
    return React.useMemo(
        () => [
            {
                Header: "Название",
                accessor: "book_title",
            },
            {
                Header: "Автор",
                accessor: "book_author",
            },
            {
                Header: "Дата до которой нужно вернуть книгу",
                accessor: "return_date",
            },
            {
                Header: "Забрали из библиотеки",
                accessor: "is_picked_up",
                Cell: ({ value }) => (value ? "Да" : "Нет"),
            },
            {
                Header: "Вернуть Книгу",
                Cell: ({ row }) => (
                    <button
                        onClick={async () =>
                            await handleReturnBook(row.original.book_id)
                        }
                    >
                        Вернуть
                    </button>
                ),
            },
        ],
        []
    )
}
