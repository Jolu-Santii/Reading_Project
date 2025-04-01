import React, { useState } from "react";
import "./Ejercicios.css";

function Ejercicios() {
  const [progress, setProgress] = useState(0);
  const [page, setPage] = useState(0);
  const [showQuestion, setShowQuestion] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [isCompleted, setIsCompleted] = useState(false);
  const [showFinalButton, setShowFinalButton] = useState(false);

  const continuar = () => {
    if (!showQuestion) {
      setShowQuestion(true);
      setErrorMessage("");
    } else if (selectedAnswer !== null) {
      const isCorrect = contenido[page].opciones.find(
        (opcion) => opcion.texto === selectedAnswer
      )?.correcta;

      if (isCorrect) {
        if (page < contenido.length - 1) {
          setShowQuestion(false);
          setSelectedAnswer(null);
          setErrorMessage("");
          setProgress((prev) => prev + (100 / contenido.length));
          setPage((prev) => prev + 1);
        } else {
          setProgress(100);
          setShowFinalButton(true); // Mostrar botón FINALIZAR
        }
      } else {
        setErrorMessage("RESPUESTA INCORRECTA");
      }
    }
  };

  const finalizar = () => {
    setIsCompleted(true);
  };

  const regresar = () => {
    if (page > 0) {
      setPage((prev) => prev - 1);
      setProgress((prev) => Math.max(prev - (100 / contenido.length), 0));
      setShowQuestion(false);
      setSelectedAnswer(null);
      setErrorMessage("");
      setShowFinalButton(false);
    } else if (page === 0 && showQuestion) {
      // Si estamos en preguntas de la primera lectura
      setShowQuestion(false);
      setSelectedAnswer(null);
      setErrorMessage("");
      setProgress(0); // Reiniciamos a 0% si volvemos a la lectura
    }
  };

  return (
    <div className="Ejercicios">
      {isCompleted ? (
        <CompletionScreen 
          onRestart={() => {
            setProgress(0);
            setPage(0);
            setShowQuestion(false);
            setSelectedAnswer(null);
            setIsCompleted(false);
            setShowFinalButton(false);
          }}
          onReturnToMenu={() => window.location.reload()}
        />
      ) : (
        <>
          <Header progress={progress} showQuestion={showQuestion} />
          <Content
            page={page}
            showQuestion={showQuestion}
            selectedAnswer={selectedAnswer}
            setSelectedAnswer={setSelectedAnswer}
          />
          <Footer
            continuar={continuar}
            finalizar={finalizar}
            regresar={regresar}
            showQuestion={showQuestion}
            selectedAnswer={selectedAnswer}
            errorMessage={errorMessage}
            isLastPage={page === contenido.length - 1}
            showFinalButton={showFinalButton}
            page={page}  // Añade esta línea
          />
        </>
      )}
    </div>
  );
}

function CompletionScreen({ onRestart, onReturnToMenu }) {
  return (
    <div className="completion-screen">
      <h1>¡Felicidades!</h1>
      <p>Has terminado la lectura con éxito!</p>
      <div className="completion-buttons">
        <button className="completion-button -restart" onClick={onRestart}>
          Reiniciar lectura
        </button>
        <button className="completion-button -menu" onClick={onReturnToMenu}>
          Regresar al menú
        </button>
      </div>
    </div>
  );
}

function Header({ progress, showQuestion }) {
  return (
    <div className="header-ejercicios">
      <div className="progress-bar-ejercicios">
        <div className="progress-ejercicios" style={{ width: `${progress}%` }}>
          {progress}%
        </div>
      </div>
      <h3>{showQuestion ? "Responde a las preguntas" : "Lee con atención"}</h3>
    </div>
  );
}

const contenido = [
  {
    titulo: "Mi gato Misi",
    texto: `Éste es mi gato.<br />
            Mi gato se llama Misi.<br />
            Misi es muy curioso.<br />
            Él es de color naranja.<br />
            A Misi le gusta trepar árboles.`,
    imagen: "/pngtree-cat-cartoon-doodle-kawaii-anime-coloring-page-cute-illustration-drawing-clipart-png-image_13361054.png",
    pregunta: "¿Qué le gusta a Misi?",
    opciones: [
      { texto: "Nadar", imagen: "/descargar (3).jpeg", correcta: false },
      { texto: "Trepar", imagen: "/Arbol.jpeg", correcta: true },
      { texto: "Comer", imagen: "/descargar (2).jpeg", correcta: false },
      { texto: "Cavar", imagen: "/descargar (4).jpeg", correcta: false },
    ],
  },
  {
    titulo: "Mi perro Rex",
    texto: `Este es mi perro.<br />
            Se llama Rex.<br />
            Rex es muy juguetón.<br />
            Él tiene el pelaje de color marrón.<br />
            A Rex le gusta correr y jugar con pelotas.`,
    imagen: "/perro.jpeg",
    pregunta: "¿Qué le gusta hacer a Rex?",
    opciones: [
      { texto: "Nadar", imagen: "/nadaperro.jpeg", correcta: false },
      { texto: "Correr", imagen: "/perro corriendo.jpeg", correcta: true },
      { texto: "Comer", imagen: "/perro comiendo.jpeg", correcta: false },
      { texto: "Dormir", imagen: "/perro durmiendo.jpeg", correcta: false },
    ],
  },
];

function Content({ page, showQuestion, selectedAnswer, setSelectedAnswer }) {
  return (
    <div className="content-ejercicios">
      {!showQuestion ? (
        <TextContent page={page} />
      ) : (
        <Question
          pregunta={contenido[page].pregunta}
          opciones={contenido[page].opciones}
          selectedAnswer={selectedAnswer}
          setSelectedAnswer={setSelectedAnswer}
        />
      )}
    </div>
  );
}

function TextContent({ page }) {
  return (
    <>
      <img
        src={contenido[page].imagen}
        alt={contenido[page].titulo}
        className="image-ejercicios"
      />
      <div className="text-box-ejercicios">
        <h3>{contenido[page].titulo}</h3>
        <p dangerouslySetInnerHTML={{ __html: contenido[page].texto }} />
      </div>
    </>
  );
}

function Question({ pregunta, opciones, selectedAnswer, setSelectedAnswer }) {
  return (
    <div className="question-box-ejercicios">
      <h3>{pregunta}</h3>
      <div className="options-ejercicios">
        {opciones.map((opcion, index) => (
          <button
            key={index}
            className={`option-ejercicios ${selectedAnswer === opcion.texto ? "selected" : ""}`}
            onClick={() => setSelectedAnswer(opcion.texto)}
          >
            <img src={opcion.imagen} alt={opcion.texto} className="option-image-ejercicios" />
            <p>{opcion.texto}</p>
          </button>
        ))}
      </div>
    </div>
  );
}

function Footer({ continuar, finalizar, regresar, showQuestion, selectedAnswer, errorMessage, isLastPage, showFinalButton, page }) {
  const getButtonText = () => {
    if (!showQuestion) return "CONTINUAR";
    return isLastPage ? (showFinalButton ? "FINALIZAR" : "VERIFICAR") : "VERIFICAR";
  };

  const shouldShowBackButton = page > 0 || (page === 0 && showQuestion);

  return (
    <div className="footer-ejercicios">
      {shouldShowBackButton && (
        <button 
          className="button-ejercicios" 
          onClick={regresar}
        >
          REGRESAR
        </button>
      )}
      
      {!shouldShowBackButton && <div></div>} {/* Espacio vacío para mantener el layout */}
      
      {errorMessage && (
        <p className="error-message-ejercicios">
          {errorMessage}
        </p>
      )}
      
      <button
        className="button-ejercicios"
        onClick={showFinalButton ? finalizar : continuar}
        disabled={showQuestion && selectedAnswer === null}
      >
        {getButtonText()}
      </button>
    </div>
  );
}
export default Ejercicios;