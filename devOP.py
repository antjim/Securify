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
		if(pre=="s" or pre==''):
			preprocesado.Menu()

		while(menu):
			print("herramientas ...")
			contramedidas.Menu()
			break
				#print("Instalando JAVA - jre 1.8.0_171")
				#preprocesado.javaInstall()
				#print("[OK] Instalación de Java finalizada.")

	def validaPet(pet):
		res=True
		for i in pet:
			if( (i!="s") and (i != "n") and (i != '')):
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
			
			if(continuar=="s" or continuar==''):
				preprocesado.gestionaProcesado(java,maven)
			else:
				print("Procesado inicial cancelado.")

		else:
			print("Por favor use 's'/'INTRO' o 'n'  para seleccionar la correspondiente acción")
			print("Volviendo al menu principal ...")


	def gestionaProcesado(java,maven):
		if(java == "s"):
			print("Instalando Java JDK 1.8.0_171")
			preprocesado.javaInstall()
			print("[OK] Instalación Java finalizada")
		if(maven == "s"):
			print("Instalando Maven 3.5.3 ")
			preprocesado.mavenInstall()
			print("[OK] Instalación Maven finalizada")

	def javaInstall():
		os.system("mkdir /usr/java")
		#os.system("tar -zxvf  utilidades/jdk-8u171-linux-i586.tar.gz")
		os.system("cp -r utilidades/jdk1.8.0_171 /usr/java")
		os.system("cp utilidades/java.sh /etc/profile.d")
		os.system("source /etc/profile.d/java.sh")

	def mavenInstall():
		os.system("tar -zxvf utilidades/apache-maven-3.5.3-bin.tar.gz")
		os.system("mv apache-maven-3.5.3 /opt/apache-maven-3.5.3")
		os.system("cp utilidades/maven.sh /etc/profile.d")
		os.system("source /etc/profile.d/maven.sh")


class contramedidas:
	
	def Menu():
		obj=[]
		cert=input("¿Generar certificados? s/n: ")
		obj.append(cert)
		
		kerberos=input("¿Instalar servidor de Kerberos? s/n: ")
		obj.append(kerberos)
		
		ranger=input("¿Instalar Apache Ranger? s/n: ")
		obj.append(ranger)

		os.system("clear")
		print("Parámetros de configuración seleccionados: Certificados ["+cert+"]"+", "+"Kerberos ["+kerberos+"], Apache Ranger["+ranger+"]")
		continuar=input("¿Continuar con configuración seleccionada? s/n: ")

		obj.append(continuar)
		if(App.validaPet(obj)):
			if(continuar=="s" or continuar==''):
				contramedidas.gestionaContramedidas(cert,kerberos,ranger)
			else:
				print("Contramedidas canceladas.")
	
		else:
			print("[ERROR] Por favor use 's'/'INTRO' o 'n' para seleccionar la correspondiente acción")
			print("Volviendo al menu principal ...")


	def gestionaContramedidas(cert,kerberos,ranger):
		if(cert == "s" or cert==''):
			print("Generando certificados")
			contramedidas.Certificados()
			print("[OK] Generación de certificados finalizada")
		
		if(kerberos == "s" or kerberos==''):
			print("Instalando Kerberos ")
			contramedidas.Kerberos()
			print("[OK] Instalación del servidor Kerberos finalizada.")

		if(ranger == "s" or ranger==''):
			print("Instalando Apache Ranger ")
			contramedidas.Ranger()
			print("[OK] Instalación de Apacha Ranger finalizada")


	def Certificados():
		os.system("bash utilidades/cert.sh")

	def Kerberos():

		def systemK():
			try:
				subprocess.call(['apt-get'])
				os.system("apt-get -y install krb5-kdc krb5-admin-server")

			except OSError:
				try:
					subprocess.call(['yum'])
					os.system("yum -y install krb5-kdc krb5-admin-server")
				except OSError:
					print("[Error] Sistema operativo soportado para Debian, derivados y CentOS")
		systemK()

		#configuración ...
		
		# ---
	def Ranger():
		print("COOKING")



# -- fin clases --


if __name__== '__main__':
	app=App()
	app.run()

