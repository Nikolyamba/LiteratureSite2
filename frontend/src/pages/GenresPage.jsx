import { useEffect, useState } from "react";

export default function GenresPage() {
    const [genres, setGenres] = useState([])
    const [error, setError] = useState('')

    useEffect(() => {
        const fetchGenres = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/genres')
                if (!(response.status===200)) throw new Error('Произошла ошибка на сервере!')
                const data = await response.json()
                setGenres(data)
            }
            catch (err){
                setError(err.message)
                alert(err.message)
            }
        }
        fetchGenres()
    }, [])

    return (
        <div>
            <h1>Жанры литературы</h1>
            <div>
                <ul>
                    {genres.map((genre) => 
                    <li key={genre.id}>
                        <img src={genre.image}/>
                        {genre.genre_name}
                    </li>
                    )}
                </ul>
            </div>
        </div>
    )

}
