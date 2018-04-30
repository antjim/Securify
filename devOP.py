#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------|
#autor: Antonio J.|
#-----------------|

import os
import subprocess
from subprocess import Popen,PIPE,STDOUT
import errno

# -- clases --

class App():

	def run(self):
		menu=True

		pre=input("¿Desea realizar el procesado? s/n: ")
		if(pre=="s"):
			preprocesado.Menu()

		while(menu):
			print("herramientas ...")
			break
				#print("Instalando JAVA - jre 1.8.0_171")
				#preprocesado.javaInstall()
				#print("[OK] Instalación de Java finalizada.")

	def validaPet(pet):
		res=True
		for i in pet:
			if( (i!="s") and (i != "n") ):
				res=False
				break
		return res



class preprocesado:

	def Menu():
		obj=[]
		java=input("¿instalar java con sus respectivas variables? s/n: ")
		obj.append(java)
		maven=input("¿Descargar maven y configurarlo? s/n: ")
		obj.append(maven)
		
		os.system("clear")
		print("Parámetros de configuración seleccionados: Java ["+java+"]"+", "+"Maven ["+maven+"]")
		continuar=input("¿Continuar con configuración seleccionada? s/n: ")
		
		obj.append(continuar)
		if(App.validaPet(obj)):
			
			if(continuar=="s"):
				preprocesado.gestionaProcesado(java,maven)
			else:
				print("Procesado inicial cancelado.")

		else:
			print("Por favor use 's' o 'n' para seleccionar la correspondiente acción")
			print("Volviendo al menu principal ...")


	def gestionaProcesado(java,maven):
		if(java == "s"):
			print("Instalando Java")
			preprocesado.javaInstall()
			print("[OK] Instalación Java finalizada")
		if(maven == "s"):
			print("Instalando Maven ... ")
			preprocesado.mavenInstall()
			print("[OK] Instalación Maven finalizada")

	def javaInstall():
		os.system("mkdir /usr/java")
		os.system("tar -zxvf  utilidades/jre-10.0.1_linux-x64_bin.tar.gz")
		os.system("mv jre-10.0.1 /usr/java")
		os.system("export JAVA_HOME=/usr/java/jre-10.0.1")
		os.system("export PATH=$PATH:/usr/java/jre-10.0.1/bin")


	def mavenInstall():
		os.system("tar -zxvf utilidades/apache-maven-3.5.3-bin.tar.gz")
		os.system("mv apache-maven-3.5.3 /opt/apache-maven-3.5.3")
		m1="export MAVEN_HOME=/opt/apache-maven-3.5.3"
		m2="export M2_HOME=/opt/apache-maven-3.5.3"
		m3="export PATH=$PATH:$M2_HOME/bin"

# -- fin clases --


if __name__== '__main__':
	app=App()
	app.run()

