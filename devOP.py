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
		
	#	pre=input("¿Desea realizar el procesado? s/n: ")
		#if(pre=="s" or pre==''):
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
			if( (i!="s") and (i != "n") and (i != '') and (i != True) and (i != False) ):
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
			s=App.System()

			if(s):
				qjk=os.popen("dpkg -l | grep openjdk-8-jdk").read()
				qje=os.popen("dpkg -l | grep openjdk-8-jre").read()
				qm=os.popen("dpkg -l | grep maven").read()

			else:
				qjk=os.popen("rpm -qa | grep java-1.8.0-openjdk").read()
				qje=os.popen("rpm -qa | grep  java-1.8.0-openjdk").read()
				qm=os.popen("rpm -qa | grep maven").read()

			obj={}
			obj["Java - JDK"]= qjk==''
			obj["Java - JRE"]= qje==''
			obj["Apache Maven"]= qm==''	#False -> el paquete existe / True -> el paquete no está instalado
			
			if(True in obj.values()):
				l=[]
				cont=1
				for i in obj:
					if(obj[i]):
						l.append(i)
						cont+=1

				if(cont>1):
					print("Paquetes necesarios: ",l)
					continuar=input("Desea instalar los paquetes necesarios? s/n: ")
				else:
					print("Paquete necesario: "+l[0])
					continuar=input("¿Desea instalar el paquete necesario? s/n: ")
		
			obj2=[]
			obj2.append(continuar)
			if(App.validaPet(obj2)):
				obj2=[]
				if(continuar=="s" or continuar==''):
					preprocesado.javaInstall(qjk,qje)
					
					if(qm):
						preprocesado.mavenInstall()
					menu=False
				else:
					print("Procesado inicial cancelado.")
					q=input("¿Desea salid del menu preprocesado? s/n: ")
					if(q=="s" or q==''):
						menu=False

			else:
				print("Por favor use 's'/'INTRO' o 'n'  para seleccionar la correspondiente acción")
				print("Volviendo al menu preprocesado ...")



	def javaInstall(jdk,jre):
		s=App.System()

		if(s):
			if(jdk):
				os.system("apt-get -y install openjdk-8-jdk")
			elif(jre):
				os.system("apt-get -y install openjdk-8-jre")
		else:
			if(jdk):
				os.system("yum install java-1.8.0-openjdk-devel")
			elif(jre):
				os.system("yum -y install java-1.8.0-openjdk")
		
		#os.system("mkdir /usr/java")
		#os.system("cp -r utilidades/jdk1.8.0_171 /usr/java")
		#os.system("cp utilidades/java.sh /etc/profile.d")
		#os.system("source /etc/profile.d/java.sh")

	def mavenInstall():
		s=App.System()
		
		if(s):
			os.system("apt-get -y install maven")
		else:
			os.system("yum -y install maven")

		#os.system("tar -zxvf utilidades/apache-maven-3.5.3-bin.tar.gz")
		#os.system("mv apache-maven-3.5.3 /opt/apache-maven-3.5.3")
		#os.system("cp utilidades/maven.sh /etc/profile.d")
		#os.system("source /etc/profile.d/maven.sh")


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

