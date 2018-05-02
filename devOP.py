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
			input("Presiona [Enter] para continuar")

		while(menu):
			os.system("clear")
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

	def System():
		
		try:
			os.popen('apt-get').read()
			return True	#debian y derivados.

		except OSError:
			try:
				os.popen('yum').read()	#CentOS y derivados
				return False
			except OSError:
				print("[Error] Sistema operativo soportado para Debian, derivados y CentOS")



class preprocesado:

	def Menu():
		menu=True
		
		while(menu):
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
				obj=[]
				if(continuar=="s" or continuar==''):
					preprocesado.gestionaProcesado(java,maven)
					menu=False
				else:
					print("Procesado inicial cancelado.")
					q=input("¿Desea salid del menu preprocesado? s/n: ")
					if(q=="s" or q==''):
						menu=False

			else:
				print("Por favor use 's'/'INTRO' o 'n'  para seleccionar la correspondiente acción")
				print("Volviendo al menu preprocesado ...")


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
		menu=True

		while(menu):
			print(" ")
			print("1) Mejorar Integridad")
			print("2) Mejorar Autorización / Autenticación")
			print("3) Mejorar Anonimidad")
			print("4) Salir")
			print(" ")
			qm=input("Seleccionar una de las opciones: ")
			
			if(qm=="1"):
				contramedidas.gestionIntegridad()

			elif(qm=="2"):
				contramedidas.gestionAu()
		
			elif(qm=="3"):
				contramedidas.gestionAn()

			else:
				menu=False


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

	def Kerberos():	#COOKING

		def systemK():
			try:
				subprocess.call(['apt-get','install','krb5-kdc','krb5-admin-server'])
				#os.system("apt-get -y install krb5-kdc krb5-admin-server")

			except OSError:
				try:
					subprocess.call(['yum','-y','install','krb5-kdc','krb5-admin-server'])
					#os.system("yum -y install krb5-kdc krb5-admin-server")
				except OSError:
					print("[Error] Sistema operativo soportado para Debian, derivados y CentOS")
		systemK()

		#configuración ...
		
		# ---
	def Ranger():

		def entornoRangerC():
			#ideal tratamiento recogidos en un log ...
			os.system("yum -y install gcc")
			
			#mysql
			os.system("wget https://dev.mysql.com/get/mysql80-community-release-el7-1.noarch.rpm")
			os.system("yum repolist all | grep mysql")
			os.system("yum repolist enabled | grep mysql")
			os.system("sudo yum -y install mysql-community-server")
			os.system("service mysqld start")
			#fin mysql ---

		def entornoRangerD():
			os.system("apt-get -y install gcc")
			os.system("apt-get -y install mysql-server")

		def compilaRanger():
			os.system("mkdir dev")
			os.system("git clone https://github.com/apache/incubator-ranger.git")
			os.system("mv incubator-ranger dev")
			#interesante comprobar mvn antes??
			os.system("cd dev/incubator-ranger && mvn clean compile package assembly:assembly install")


		print("PREPARANDO ENTORNO")
		entorno=App.System()

		if(entorno):
			entornoRangerD()
		
		elif(entorno==False):
			entornoRangerC()

		print("COMPILANDO APACHE RANGER")

		compilaRanger()

		print("INSTALANDO RANGER")


	def gestionIntegridad():
		obj=[]
		cert=input("¿Generar certificados? s/n: ")
		obj.append(cert)

		os.system("clear")
		print("Parámetros de configuración seleccionados: Certificados ["+cert+"]")
		continuar=input("¿Continuar con configuración seleccionada? s/n: ")

		obj.append(continuar)
		if(App.validaPet(obj)):

			if(continuar=="s" or continuar==''):
				contramedidas.gestionaContramedidas(cert,'n','n')	#evitar replicas constantes.
			else:
				print("Parametros de Integridad canceladas.")
				q=input("¿Salir del menu de integridad? s/n: ")

				if(q=="n"):
					contramedidas.gestionIntegridad()

		else:
			print("[ERROR] Por favor use 's'/'INTRO' o 'n' para seleccionar la correspondiente acción")
			print("Volviendo al menu principal ...")


	def gestionAu():
		obj=[]
		kerberos=input("¿Instalar servidor de Kerberos? s/n: ")
		obj.append(kerberos)

		ranger=input("¿Instalar Apache Ranger? s/n: ")
		obj.append(ranger)

		os.system("clear")
		print("Parámetros de configuración seleccionados: Kerberos ["+kerberos+"], Apache Ranger["+ranger+"]")
		continuar=input("¿Continuar con configuración seleccionada? s/n: ")

		obj.append(continuar)
		if(App.validaPet(obj)):
			if(continuar=="s" or continuar==''):
				contramedidas.gestionaContramedidas('n',kerberos,ranger)
			else:
				print("Contramedidas de Autorización / Autenticación canceladas.")

		else:
			print("[ERROR] Por favor use 's'/'INTRO' o 'n' para seleccionar la correspondiente acción")
			print("Volviendo al menu principal ...")


	def gestionAn():
		obj=[]
		kerberos=input("¿Instalar servidor de Kerberos? s/n: ")
		obj.append(kerberos)

		os.system("clear")
		print("Parámetros de configuración seleccionados: Kerberos ["+kerberos+"]")
		continuar=input("¿Continuar con configuración seleccionada? s/n: ")

		if(App.validaPet(obj)):
			if(continuar=="s" or continuar==''):
				contramedidas.gestionaContramedidas('n',kerberos,'n')
			else:
				print("Contramedidas de anonimato canceladas.")

		else:
			print("[ERROR] Por favor use 's'/'INTRO' o 'n' para seleccionar la correspondiente acción")
			print("Volviendo al menu principal ...")


# -- fin clases --


if __name__== '__main__':
	app=App()
	app.run()

