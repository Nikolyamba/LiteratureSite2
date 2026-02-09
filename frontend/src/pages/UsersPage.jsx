import { useEffect, useState } from "react";

export default function GetUsers() {
    const [users, setUsers] = useState([])
    const [error, setError] = useState('')

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/users');
                if (!response.status===200) throw new Error('Произошла ошибка на сервере');
                const data = await response.json();
                setUsers(data);
            } catch (err) {
                setError(err.message);
                alert(err.message)
            }
        };

        fetchUsers();
    }, []);

    return (
        <div>
            <h1>Пользователи нашего сайта</h1>
            <div>
                <ul>
                    {users.map(user => (
                        <li key = {user.id}>
                            <img src={user.image}/>
                            {user.login}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    )
}