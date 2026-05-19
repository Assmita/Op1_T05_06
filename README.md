# DevOps Portfolio — TP07: CI/CD

![CI/CD Pipeline](https://github.com/Assmita/Op1_T05_06/actions/workflows/cicd.yml/badge.svg)

App de notas con pipeline CI/CD completo usando GitHub Actions.

## Pipeline

| Stage | Trigger | Qué hace |
| :--- | :--- | :--- |
| **lint** | todo push | flake8 en Python, yamllint en YAML |
| **test** | después de lint | pytest con reporte de cobertura |
| **build-push** | main y develop | docker buildx, push a Docker Hub |
| **deploy** | solo main | Ejecución nativa en **WSL local** mediante Runner Self-Hosted |

## Secrets requeridos en GitHub

Para que el flujo funcione correctamente, se deben configurar las siguientes variables de entorno en el repositorio de GitHub (*Settings > Secrets and variables > Actions*):

* **`DOCKERHUB_USERNAME`**: Tu usuario de Docker Hub.
* **`DOCKERHUB_TOKEN`**: Token de acceso seguro para la publicación de imágenes.

*(Nota: Los antiguos secrets de conexión por SSH ya no son requeridos, dado que el despliegue se realiza mediante un agente local automatizado).*

## Correr tests localmente

Para ejecutar el set de pruebas unitarias en el entorno local (WSL), corra la siguiente secuencia de comandos:

```bash
# Activar el entorno virtual e instalar dependencias
cd backend
pip install -r requirements.txt

# Ejecutar la suite de tests con reporte de cobertura analítico
pytest tests/ -v --cov=. --cov-report=term-missing
EOD
cat > README.md << 'EOF'
# DevOps Portfolio — TP07: CI/CD

![CI/CD Pipeline](https://github.com/Assmita/Op1_T05_06/actions/workflows/cicd.yml/badge.svg)

App de notas con pipeline CI/CD completo usando GitHub Actions.

## Pipeline

| Stage | Trigger | Qué hace |
| :--- | :--- | :--- |
| **lint** | todo push | flake8 en Python, yamllint en YAML |
| **test** | después de lint | pytest con reporte de cobertura |
| **build-push** | main y develop | docker buildx, push a Docker Hub |
| **deploy** | solo main | Ejecución nativa en **WSL local** mediante Runner Self-Hosted |

## Secrets requeridos en GitHub

Para que el flujo funcione correctamente, se deben configurar las siguientes variables de entorno en el repositorio de GitHub (*Settings > Secrets and variables > Actions*):

* **`DOCKERHUB_USERNAME`**: Tu usuario de Docker Hub.
* **`DOCKERHUB_TOKEN`**: Token de acceso seguro para la publicación de imágenes.

*(Nota: Los antiguos secrets de conexión por SSH ya no son requeridos, dado que el despliegue se realiza mediante un agente local automatizado).*

## Correr tests localmente

Para ejecutar el set de pruebas unitarias en el entorno local (WSL), corra la siguiente secuencia de comandos:

```bash
# Activar el entorno virtual e instalar dependencias
cd backend
pip install -r requirements.txt

# Ejecutar la suite de tests con reporte de cobertura analítico
pytest tests/ -v --cov=. --cov-report=term-missing
