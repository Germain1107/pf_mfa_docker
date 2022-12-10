# pf_mfa_docker
Proyecto final de sistemas operativos. creación de entornos de desarrollo con contenedores

# Ejecutar
## generar container de docker
~~~
docker build . --tag germainalvarado/proyecto_final:v1.0.0

~~~~
## Ejecutar aplicacion de flask en Docker
~~~~
docker run -d -p 5000:5000 germainalvarado/proyecto_final:v1.0.0
~~~
# abrir el navegador
<a href="http://127.0.0.1:5000/"> Aplicacion enlace </a>
