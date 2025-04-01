import { useState } from 'react'
import './App.css'
import Ejercicios from './Ejercicios'

function App() {
  const [count, setCount] = useState(0)
  const [bubbleText] = useState("¿Qué haremos hoy aventurero?")
  const [showExercises, setShowExercises] = useState(false)

  return (
    <>
      {!showExercises ? (
        <div className="main-container">
          <nav className="nav-superior">
            <ul className="ul-menu">
              <li>
                <a className="active">
                  <img className="logo" src="book_1.png" alt="Logo"></img>
                  <span className="link-text">
                    Apoya a la Lectura Infántil
                  </span>
                </a>
              </li>
              <li>
                <a>
                  <span className="link-text"></span>
                </a>
              </li>
              <li>
                <a>
                  <img src="boy.png" alt="boy" className="user-icon" />
                </a>
              </li>
            </ul>
          </nav>

          <div className="button-container" role="group" aria-label="Action Buttons">
            <button className="button -green" aria-label="Tareas"> 
              <img src="homework.png" alt="homework" className="button-icon"/>
              Tareas
            </button>
            
            <button className="button -blue" aria-label="Entregados">
              <img src="check.png" alt="completed" className="button-icon"/>
              Completado
            </button>
                
            <button className="button -salmon" aria-label="Reporte">
              <img src="sign.png" alt="report" className="button-icon" />
              Reporte
            </button>
          </div>

          <div className="students-container">
            <img src="/globo_3.png" alt="Globo" className="g3" />
            <img src="/globo_4.png" alt="Globo" className="g4"/>
            <img src="/globo_5.png" alt="Globo" className="g5" />
            <img src="/globo_3.png" alt="Globo" className="g32" />
            <img src="/globo_9.png" alt="Globo" className="g8" />
            <img src="/globo_8.png" alt="Globo" className="g9" />

            <div className="center-image-container">
              <img 
                src="/globotexto.png"
                alt="Libro abierto" 
                className="center-image"
              />
              <div className="image-text">{bubbleText}</div>
            </div>
            <img src="/students_boy.png" alt="Niño" className="student boy" />
            <img src="/students_girl.png" alt="Niña" className="student girl" />
          </div>

          {/* Sección de actividades */}
          <div className="activities-container">
            <h2 className="activities-title">Actividades</h2>
            
            <div className="activities-list">
              <div className="activity-item">
                <span className="activity-name">Lectura uno</span>
                <div className="activity-buttons">
                  <button className="status-button">Incompleto</button>
                  <button 
                    className="go-button"
                    onClick={() => setShowExercises(true)}
                  >
                    Ir
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        ) : (
          <div className="exercises-fullscreen">
            <Ejercicios />
            <button 
              className="close-exercises" 
              onClick={() => setShowExercises(false)}
              aria-label="Cerrar ejercicios"
            >
              ×
            </button>
          </div>
      )}
    </>
  )
}
export default App