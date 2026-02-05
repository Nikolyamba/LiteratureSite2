import { useState } from "react"

export default function RegisterPage() {
    const [email, setEmail] = useState("")
    const [login, setLogin] = useState("")
    const [password, setPassword] = useState("")
    const [message, setMessage] = useState("")
    const [error, setError] = useState("")

    const handleSumbit = async (e) => {
        e.preventDefault()
        
        try {
            const response = await fetch('http://127.0.0.1:8000/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, login, password }),
            });
            const data = await response.json()
            
            if (response.status === 200) {
                setMessage('Регистрация прошла успешно! Сейчас вас перекинет на страницу авторизации')
                alert(data)
                setEmail("")
                setLogin("")
                setPassword("")
            } else {
                setError(data.detail || 'Возникла ошибка при регистрации!')
                alert('Возникла ошибка при регистрации')
            }
        } catch {
            setError("Ошибка: 500. Сервер не отвечает")
            alert("Error")
        }
    }

    return (
        <form onSubmit={handleSumbit}> 
            <div className="registerPage">
                <h1>Страница регистрации!</h1>

                <label htmlFor="email"><b>Email:</b></label>
                <input id="email" type="text" value={email}
                    placeholder="введите email" name="email"
                    onChange={(e) => setEmail(e.target.value)} required /> 

                <label htmlFor="login"><b>Login:</b></label>
                <input id="login" type="text" value={login}
                    placeholder="введите login" name="login"
                    onChange={(e) => setLogin(e.target.value)} required />

                <label htmlFor="password"><b>Пароль:</b></label>
                <input id="password" type="password" value={password}
                    placeholder="введите пароль" name="password"
                    onChange={(e) => setPassword(e.target.value)} required />

                <button type="submit">Отправить!</button>
            </div>
        </form>
    )
}