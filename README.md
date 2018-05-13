# Securify

Securify es un DevOP que trata que posee una automatización para la mejora de seguridad de herramientas usadas en Big Data. En este caso, sólo existe un caso específico, pero la idea es seguir creciendo para agilizar a cualquier personal de las TI.

## Requisitos

Para hacer uso de este script, es necesario tener instalado una versión de ***Python superior a la 3*** . Por otra parte, puede usarse en sistemas GNU/Linux como ***Debian (así como derivados) y CentOS (junto a sus derivados)*** . 

## Funcionalidades

EL script se encargará de detectar necesidades básicas para poder trabajar correctamente. Se podrá mejorar tres aspectos importantes de la seguridad en la infraestructura de Big Data: ***Integridad, Autorización / Autenticación y Anonimato***. Las configuraciones se realizan de manera general, sin entrar en detalle en la herramienta con la que se trabaje, exceptuando ***Apache Storm*** que podremos reforzar directamente alguno de los aspectos que se han mencionado anteriormente.

## Uso

Para hacer uso del script, simplemente será necesario ejecutar el siguiente comando desde consola con permisos de superusuario: `root$ python3 devOP.py`

En caso de que se use CentOS o algún tipo de sistema derivado, se puede usar un pequeño script que se encuentra en la carpeta de ***utilidades*** . Para usarse simplemente escribimos en una terminal con permisos de superusuario lo siguiente: `root$ bash python3.sh` . Una vez finalizado podemos comprobar que tenemos ***python3.6*** escribiendo `$ python3.6 -V` .

## Aspectos a tener en cuenta

Si se marca la opción de instalar Apache Ranger es posible que por un lado pueda quedarse la descarga pillada (en este caso simplemente tener paciencia) o llegue a fallar en alguno de los puntos, es algo relativo a la configuración, por ello no facilitamos la posibilidad de automatizar dicho proceso, puesto que en cada ejecución y en cada máquina, actua de una manera distinta, exceptuando errores claros. Esto ocurre tanto de manera general como en una herramienta concreta. 

Por tanto en caso de fallo volver a ejecutar en modo depuración desde el directorio ***dev/incubator-ranger*** , mediante el comando `root$ mvn clean compile package assembly:assembly install -X` . Para mayor información: 

https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.5.0+Installation#ApacheRanger0.5.0Installation-InstallationInstructions
