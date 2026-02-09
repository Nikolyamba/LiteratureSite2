import { useEffect, useState } from "react";

export default function GetAllGenres() {
    const [genres, setGenres] = useState([])
    const [error, setError] = useState('')

    useEffect(() => {
        const fetchGenres = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/genres')
                if (!response.status===200) throw new Error('Произошла ошибка на сервере!')
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
            
        </div>
    )

}
