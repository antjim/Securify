#!/bin/bash
# -*- ENCODING: UTF-8 -*-

echo "Ruta por defecto /home/ssl, pulsar intro para confirmar o agrega una nueva ruta dónde guardar los certificados: "
read "DIR"
if [ "$DIR" = "" ]; then
DIR=/home/ssl
mkdir /home/ssl
fi

echo " ---------- "

echo "Alias del almacén (intro para establecer por defecto como localhost): "
read "ALIAS"

echo " ---------- "

if [ "$ALIAS" = "" ]; then
ALIAS="localhost"
fi

echo " ---------- "

echo "Clave para el certificado (CUIDADO CON LAS CLAVES QUE SE SOLICITEN EN LA CREACIÓN DEL CERTIFICADO): "
read "CLAVE"

echo " ---------- "

echo "Duración en días del certificado (intro para establecer por defecto como 365 días): "
read "DIAS"

echo " ---------- "

if [ "$DIAS" = "" ]; then
DIAS=365
fi

echo " ---------- "



keytool -keystore $DIR/server.keystore.jks -alias $ALIAS -validity $DIAS -keyalg RSA -genkey

openssl req -new -x509 -keyout $DIR/ca-key -out $DIR/ca-cert -days $DIAS

keytool -J-Duser.language=en -keystore $DIR/server.truststore.jks -alias CARoot -import -file $DIR/ca-cert

keytool -J-Duser.language=en -keystore $DIR/client.truststore.jks -alias CARoot -import -file $DIR/ca-cert

keytool -keystore $DIR/server.keystore.jks -alias $ALIAS -certreq -file $DIR/cert-file

openssl x509 -req -CA $DIR/ca-cert -CAkey $DIR/ca-key -in $DIR/cert-file -out $DIR/cert-signed -days $DIAS -CAcreateserial -passin pass:$CLAVE

keytool -J-Duser.language=en -keystore $DIR/server.keystore.jks -alias CARoot -import -file $DIR/ca-cert

keytool -J-Duser.language=en -keystore $DIR/server.keystore.jks -alias $ALIAS -import -file $DIR/cert-signed

