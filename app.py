"""!
@file app.py
@brief API de gestión de alumnos "Sistema Alumnos" (actividad OCY1102).
"""
import os

from flask import Flask, jsonify, request

## Aplicación Flask principal; sobre ella se registran las rutas de la API.
app = Flask(__name__)

## Base de datos en memoria con los alumnos (solo para fines de la actividad).
ALUMNOS = [
    {"id": 1, "nombre": "Ana Pérez", "carrera": "Ingeniería en Informática", "promedio": 6.1},
    {"id": 2, "nombre": "Benjamín Rojas", "carrera": "Ingeniería en Ciberseguridad", "promedio": 5.4},
    {"id": 3, "nombre": "Camila Soto", "carrera": "Analista Programador", "promedio": 6.8},
]

## Versión de la aplicación. La inyecta el pipeline con APP_VERSION (ver Jenkinsfile) y sirve para la trazabilidad.
VERSION = os.environ.get("APP_VERSION", "dev")


@app.route('/hello')
def hello():
    """!
    @brief Saluda al usuario.

    El nombre no es un argumento de la función: se lee del parámetro
    de consulta name de la URL (por ejemplo /hello?name=Ana).

    @return Texto con el mensaje de saludo.
    """
    name = request.args.get('name')
    return f"Hello, {name}!"


@app.route('/health')
def health():
    """!
    @brief Informa el estado de la aplicación.

    Lo usa la prueba de humo del despliegue para saber si la app responde.

    @return JSON con el campo estado en "ok".
    """
    return jsonify({"estado": "ok"})


@app.route('/version')
def version():
    """!
    @brief Informa qué versión de la aplicación está desplegada.

    Es el punto de partida de la trazabilidad: la versión tiene la forma
    1.0.N+commit, donde N es el número de build de Jenkins.

    @return JSON con el nombre de la aplicación y su versión.
    """
    return jsonify({"aplicacion": "Sistema Alumnos", "version": VERSION})


@app.route('/alumnos')
def listar_alumnos():
    """!
    @brief Lista todos los alumnos registrados.
    @return JSON con la lista completa de alumnos.
    """
    return jsonify(ALUMNOS)


@app.route('/alumnos/<int:alumno_id>')
def obtener_alumno(alumno_id):
    """!
    @brief Obtiene un alumno por su identificador.
    @param alumno_id Identificador numérico del alumno.
    @return JSON con el alumno, o error 404 si no existe.
    """
    for alumno in ALUMNOS:
        if alumno["id"] == alumno_id:
            return jsonify(alumno)
    return jsonify({"error": "Alumno no encontrado"}), 404


@app.route('/alumnos', methods=['POST'])
def crear_alumno():
    """!
    @brief Crea un alumno nuevo a partir del JSON recibido.

    El cuerpo de la petición debe traer nombre (obligatorio), promedio
    (número entre 1.0 y 7.0) y, de forma opcional, carrera. El id se
    asigna automáticamente.

    @return JSON con el alumno creado y código 201, o error 400 si los datos no son válidos.
    """
    datos = request.get_json(silent=True) or {}
    nombre = str(datos.get("nombre", "")).strip()
    promedio = datos.get("promedio")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400
    if not isinstance(promedio, (int, float)) or not 1.0 <= promedio <= 7.0:
        return jsonify({"error": "El 'promedio' debe ser un número entre 1.0 y 7.0"}), 400

    nuevo = {
        "id": max(a["id"] for a in ALUMNOS) + 1,
        "nombre": nombre,
        "carrera": str(datos.get("carrera", "Sin carrera")),
        "promedio": promedio,
    }
    ALUMNOS.append(nuevo)
    return jsonify(nuevo), 201


def main():
    """!
    @brief Inicia el servidor de desarrollo de Flask.

    Solo se usa al ejecutar el archivo directamente; el despliegue de
    prueba arranca la aplicación con flask run.
    """
    app.run(debug=True)


if __name__ == '__main__':
    main()
