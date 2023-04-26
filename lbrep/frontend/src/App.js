import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import './App.css'

//Screens
import HomeScreen from './Screens/HomeScreen'
import ListingsScreen from './Screens/ListingsScreen'
import LoginScreen from './Screens/LoginScreen'

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<HomeScreen />} />
        <Route path='/login' element={<LoginScreen />} />
        <Route path='/listings' element={<LoginScreen />} />
      </Routes>
    </Router>
  )
}

export default App
