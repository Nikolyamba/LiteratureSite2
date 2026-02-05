import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div className="page-container">
      <h1>Добро пожаловать на мой литературный сайт!</h1>

      <p>
        Данный пет проект посвящён моему другому реальному проекту,
        который я делал год назад. Основное — посмотреть,
        как я изменился за этот год.
      </p>  

    <Link to="/literatures">
        <button>Литература</button>
    </Link>
    <Link to="/authors">
        <button>Авторы</button>
    </Link>
    <Link to="/genres">
        <button>Жанры</button>
    </Link>
    <Link to="/users">
        <button>Пользователи</button>
    </Link>
    <Link to="/register">
        <button>Регистрация</button>
    </Link>
    </div>
  )
}