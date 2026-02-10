import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom"
import HomePage from './pages/HomePage'
import RegisterPage from './pages/RegisterPage'
import LoginPage from './pages/LoginPage'
import UsersPage from './pages/UsersPage'
import GenresPage from './pages/GenresPage'


export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<HomePage />}/>
        <Route path='/register' element={<RegisterPage />}/>
        <Route path='/login' element={<LoginPage />}/>
        <Route path='/users' element={<UsersPage />}/>
        <Route path='/genres' element={<GenresPage />}/>
      </Routes>
    </BrowserRouter>
  )
}

