# Mundo de Letras

![Static Badge](https://img.shields.io/badge/licence-BUAP-blue?style=for-the-badge&link=https://buap.mx/)
![Static Badge](https://img.shields.io/badge/release%20date-Enero%202025-blue?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/status-en%20desarrollo-green?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/stable%20version-%20-green?style=for-the-badge)


## 🎯 Objetivo
Facilitar el desarrollo de competencias lectoras mediante ejercicios personalizados, retroalimentación inteligente y seguimiento de progreso.


## ✨ Características
Fomenta el análisis de textos: Identificación de ideas principales, vocabulario clave y estructura argumental.

Gamificación: Logros y recompensas para motivar el aprendizaje.

Panel de estadísticas: Visualización del progreso en tiempo real.


## Tecnologías Utilizadas

- Python
- SQLite


## Compilar la aplicación

### Requisitos previos
1. Instalar las dependecias de Python:
```python
pip install -r requirements.txt
```

#### Compilar la aplicación:
2. Usando PyInstaller y el archivo *mundo_de_letras.spec* se puede usar el script *build.bat* para que la compilación se haga de manera automática:
```
./build.bat
```

### Resultado
Este script, no solo compila la aplicación en un archivo ejecutable de Windows, sino que tambien copia todo el directorio de archivos requeridos por la aplicación, como: las imagenes de los ejecicios, los ejercicios, etc.


## Estructura de la aplicación
- `main.py`: Punto de entrada de la aplicación.
- `recursos/`: Contiene imagenes y recursos ajenos a las lecturas.
- `ImagenesLecturas/`: Contiene las imagenes de las lecturas.
- `lista_ejercicios/`: Contiene un archivo JSON con la información de los datos de cada ejercicio.
- `preguntas/`: Contiene la base de datos SQLite con los ejercicios, preguntas y sus respuestas.
- `respuestas/`: Almacena las respuestas de los ejercicios.
- `reporte/`: Contiene el reporte del desempeño del usuario en PDF.

- - -

## Miembros
![Static Badge](https://img.shields.io/badge/Prior%20Hernandez%20Reychel--blue?style=for-the-badge&link=https://github.com/reychel) 
![Static Badge](https://img.shields.io/badge/Rojas%20Flores%20Jose%20D.--blue?style=for-the-badge&link=https://github.com/rojas)
![Static Badge](https://img.shields.io/badge/Rodriguez%20Maldonado%20Jose%20Antonio--blue?style=for-the-badge&link=https://github.com/rodriguezmldo)
![Static Badge](https://img.shields.io/badge/Santiago%20Ibanez%20Jose%20Luis--blue?style=for-the-badge&link=https://github.com/Jolu-Santii) 
![Static Badge](https://img.shields.io/badge/Salinas%20Gil%20Diego--blue?style=for-the-badge&link=https://github.com/rojas)
![Static Badge](https://img.shields.io/badge/Lara%20Paez%20Cristobal%20R.--blue?style=for-the-badge&link=https://github.com/CRIZZxR-110100)