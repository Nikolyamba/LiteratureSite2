import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"

export default GenrePage() {
    const { genre_id } = useParams()
    const [books, setBooks] = useState([])
    const [error, setError] = useState('')
    useEffect(() => {
        const fetchGenreBooks = async () => {
            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/api/genres/${genre_id}`
                )

                if (!response.ok) {
                    throw new Error("Такой жанр не найден")
                }

                const data = await response.json()
                setBooks(data)
            } catch (err) {
                setError(err.message)
            }
        }

        fetchGenreBooks()
    }, [genre_id])


    return (
        <div>
            <h1>Книги данного жанра</h1>
            <ul>
                {books.map(book => (
                    <li key={book.title}>
                        <img src={book.image}/>
                        <p>{book.title}</p>
                    </li>
                ))}
            </ul>
        </div>
    )
}