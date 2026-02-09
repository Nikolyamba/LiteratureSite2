import { useState } from "react"


export default function LoginPage() {
    const [login, setLogin] = useState("")
    const [password, setPassword] = useState("")

    const [message, setMessage] = useState("")
    const [error, setError] = useState("")

    const handleSumbit = async (e) => {
        e.preventDefault()

        try {
            const response = await fetch('http://127.0.0.1:8000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({login, password})
            });

            if (response.status === 200) {
                const data = await response.json()
                
                localStorage.setItem('access_token', data.access_token)
                localStorage.setItem('refresh_token', data.refresh_token)

                setMessage('Успешная авторизация!')
                setLogin("")
                setPassword("")
                alert('Вы успешно авторизовались!')
            }
            else {
                setError('Ошибка авторизации, неверный Login или пароль!')
                alert('Ошибка авторизации, неверный Login или пароль!')
            }
        }
        catch {
            setError('Произошла ошибка на сервере!')
            alert('Произошла ошибка на сервере!')
        }

    }

    return (
        <form onSubmit={handleSumbit}>
            <div>
                <h1>Авторизация</h1>

                <label htmlFor="login"><b>Login:</b></label>
                <input id="login" type="text" value={login} placeholder="Введите свой Login"
                name="login" required onChange={(e) => setLogin(e.target.value)}/>
                
                <label htmlFor="password"><b>Пароль:</b></label>
                <input id="password" type="password" value={password} placeholder="Введите свой пароль"
                name="password" required onChange={(e) => setPassword(e.target.value)}/>
            </div>
        </form>
    )
}