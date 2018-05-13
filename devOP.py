#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#-----------------|
#autor: Antonio J.|
#-----------------|

import os
import subprocess
from subprocess import Popen,PIPE,STDOUT
import errno
import storm

# -- clases --

class App():

	def run(self,ro):
		menu=True

		preprocesado.Menu()

		while(menu):
			os.system("clear")
			contramedidas.Menu(ro)
			break

	def validaPet(pet):
		res=True
		for i in pet:
			if( (i!="s") and (i != "n") and (i != '') and (i != True) and (i != False) ):
				res=False
				break
		return res

	def System():
		
		try:
			subprocess.call('apt-get')
			os.system("clear")
			return True	#debian y derivados.

		except OSError:
			try:
				subprocess.call('yum')	#CentOS y derivados
				os.system("clear")
				return False
			except OSError:
				print("[Error] Sistema operativo soportado para Debian, derivados y CentOS")

	def logo():
		print(" __                      _  __       ")
		print("/ _\ ___  ___ _   _ _ __(_)/ _|_   _ ")
		print("\ \ / _ \/ __| | | | '__| | |_| | | |")
		print("_\ \  __/ (__| |_| | |  | |  _| |_| |")
		print("\__/\___|\___|\__,_|_|  |_|_|  \__, |")
		print("			       |___/")

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
					
						if(qm==''):
							preprocesado.mavenInstall()
						menu=False
						input("Presiona [ENTER] para continuar.")
					else:
						print("Procesado inicial cancelado.")
						q=input("¿Desea salid del menu preprocesado? s/n: ")
						if(q=="s" or q==''):
							menu=False

				else:
					print("Por favor use 's'/'INTRO' o 'n'  para seleccionar la correspondiente acción")
					print("Volviendo al menu preprocesado ...")
			else:
				menu=False


	def javaInstall(jdk,jre):
		s=App.System()

		if(s):
			if(jdk==''):
				os.system("apt-get -y install openjdk-8-jdk")
			elif(jre==''):
				os.system("apt-get -y install openjdk-8-jre")
		else:
			if(jdk==''):
				os.system("yum -y install java-1.8.0-openjdk-devel")
			elif(jre==''):
				os.system("yum -y install java-1.8.0-openjdk")

	def mavenInstall():
		s=App.System()
		
		if(s):
			os.system("apt-get -y install maven")
		else:
			os.system("yum -y install maven")

class herramientasBD:

	def Menu(ro):
		os.system("clear")
		App.logo()
		print(" ")
		print("===== Herramientas Big Data =====")
		print("1) Apache Storm")
		print("===================================")
		print("2) Volver al menu Contramedidas Generales")
		print("===================================")
		qm=input("Seleccionar una de las opciones: ")

		if(qm=="1"):
			storm.Storm().run(ro)

		else:
			contramedidas.Menu(ro)


class ayuda:

	def Menu(ro):
		while(True):
			os.system("clear")
			App.logo()
			print(" ")
			print("===================== Menú de Ayuda =====================")
			print("1) Sobre la Integridad")
			print("2) Sobre la Autorización / Autenticación")
			print("3) Sobre la Anonimidad")
			print("4) Sobre la fortificación de las herramientas Big Data")
			print("5) Inicio de una herramienta")
			print("=========================================================")
			print("6) Volver a Contramedidas generales")
			print("=========================================================")
			qm=input("Seleccionar una de las opciones: ")		
			
			if(qm=="1"):
				ayuda.Integridad()

			elif(qm=="2"):
				ayuda.AutoAuten()

			elif(qm=="3"):
				ayuda.Anonimidad()

			elif(qm=="4"):
				ayuda.BigData()

			elif(qm=="5"):
				ayuda.Inicio()

			else:
				contramedidas.Menu(ro)


	def Integridad():
		os.system("clear")
		print(" ")
		cadena="En esta sección podrás hacer uso de distintas herramientas que te permitirán mejorar"
		s=" la integridad tanto de manera general como focalizada a alguna de las herramientas."
		s1=" Con ello se mejorará la veracidad de la información con la que se trabaja."
		s2=" Dicha sección contará con una configuración de certificados SSL que aseguren lo anteriormente mencionado.\n\n"
		s3=" Para usarse únicamente es necesario usar en el menú de contramedidas generales o el menú"
		s4=" de herramientas Big Data la tecla '1'. A continuación sólo tendremos que usar las claves"
		cadena+=s+s1+s2+s3+s4+" que creamos oportunas, así como dónde querámos guardar dichos certificados."
		print(format(cadena))
		print(" ")
		input("Pulsa [ENTER] para continuar")

	def AutoAuten():
		os.system("clear")
		print(" ")
		c="En esta sección se mejorará dos aspectos: la Autorización y la Autenticación. Para ello "
		c=c+"se podrá hacer uso de dos herramientas a elegir tanto en medidas generales como en el apartado"
		c=c+"de herramietnas Big Data, estas son kerberos y Apache Ranger.\n\n"
		c=c+"Si se pretende instalar/configurar Kerberos, desde la sección general, se realizará un preconfigurado "
		c=c+"que permite el uso de Kerberos para más tarde hacerse uso. En caso de hacerse desde la sección de"
		c=c+" las herramientas, se configurará de manera más especifica para la configuración de dicha herramienta. \n\n"
		c=c+"Si hablamos de Ranger, únicamente se realizará una descarga de la última versión y compilación, la "
		c=c+"integración de la herramienta se debe hacer aparte."
		print(format(c))
		print(" ")
		input("Pulsa [ENTER] para continuar")

	def Anonimidad():
		os.system("clear")
		print(" ")
		c="En esta sección se hará uso de la herramientas Kerberos para establecer el anonimato en "
		c=c+"la herramienta Big Data deseada o de manera general, mediante un preconfigurado. "
		print(format(c))
		print(" ")
		input("Pulsa [ENTER] para continuar")

	def BigData():
		os.system("clear")
		print(" ")
		c="En esta sección se podrán elegir una de las herramientas de las que aparecen en "
		c=c+"el menú de herramientas de Big Data. Una vez se seleccione se podrán elegir 3 "
		c=c+"principales funciones que mejorarán la seguridad de dicha herramienta: Integridad"
		c=c+", Autorización / Autenticación y por último el Anonimato."
		print(format(c))
		print(" ")
		input("Pulsa [ENTER] para continuar")

	def Inicio():
		os.system("clear")
		print(" ")
		c="Esta sección se encuentra exclusivamente en el apartado de cada herramienta con "
		c=c+"ello se pretende iniciar la herramienta para ofrecer una mera comodidad y no "
		c=c+"tener que recurrir a terminales extras para arrancarlas."
		print(format(c))
		print(" ")
		input("Pulsa [ENTER] para continuar")

class contramedidas:
	
	def Menu(ro):	#ro es la ruta de storm

		while(True):
			os.system("clear")
			App.logo()
			print(" ")
			print("===== Contramedidas Generales =====")
			print("1) Mejorar Integridad")
			print("2) Mejorar Autorización / Autenticación")
			print("3) Mejorar Anonimidad")
			print("===================================")
			print("4) Mejorar Seguridad de herramientas Big Data")
			print("5) Ayuda")
			print("6) Salir")
			print("===================================")
			qm=input("Seleccionar una de las opciones: ")
			
			if(qm=="1"):
				contramedidas.gestionIntegridad()

			elif(qm=="2"):
				contramedidas.gestionAu()
		
			elif(qm=="3"):
				contramedidas.gestionAn()

			elif(qm=="4"):
				herramientasBD.Menu(ro)

			elif(qm=="5"):
				ayuda.Menu(ro)

			else:
				break


	def gestionaContramedidas(cert,kerberos,ranger):
		if(cert == "s" or cert==''):
			print("Generando certificados")
			contramedidas.Certificados()
			print("[OK] Generación de certificados finalizada")
		
		if(kerberos == "s" or kerberos==''):
			print("Instalando Kerberos "+"\n")
			contramedidas.Kerberos()
			print("[OK] Instalación del servidor Kerberos finalizada.")

		if(ranger == "s" or ranger==''):
			print("Instalando Apache Ranger ")
			contramedidas.Ranger()
			#print("[OK] Instalación de Apacha Ranger finalizada")


	def Certificados():
		os.system("bash utilidades/cert.sh")

	def Kerberos():	

		def systemK():
			#4 estados - 0: debian y no instalado | 1: debian e instalado | 2: centos y no inst | 3: centos e instalado

			try:
				print("** En caso de aparecer un cuadro para escribir el reino recomendamos usar la tecla 'ESC' para que el sistema se encargue por si mismo. **","\n")
				input("Pulsa [ENTER] para continuar.")

				subprocess.call(['apt-get'])

				kdc=os.popen("dpkg -l | grep krb5-kdc").read()
				adser=os.popen("dpkg -l | grep krb5-admin").read()

				if(kdc=='' or adser==''):

					subprocess.call(['apt-get','-y','install','krb5-kdc','krb5-admin-server'])
					os.system("clear")
					return 0
				else:
					os.system("clear")
					return 1
		
			except OSError:
				try:
					subprocess.call(['yum'])

					works=os.popen("rpm -qa | grep krb5-workstation").read()
					adser=os.popen("rpm -qa | grep krb5-server").read()

					if(works=='' or adser==''):

						subprocess.call(["yum -y install krb5-server krb5-workstation pam_krb5 krb5-libs"],shell=True)
						os.system("clear")
						return 2
					else:
						os.system("clear")
						return 3

				except OSError:
					print("[Error] Sistema operativo soportado para Debian, derivados y CentOS")
		

		#configuración ...
		def trataLinea(linea):
			res=''
			for i in range (len(linea)):

				if(linea[i]!="#"):

					if(linea[i]=="="):
						res+=linea[i]
						break
					else:
						res+=linea[i]
			return res

		def confKC(nuevo):		#configuración para CentOS | COOKING - BUGS
			#/etc/krb5.conf
		
			reino=input("Indique nombre del dominio ([ENTER] para establecer por defecto localhost): ")
			if(reino==''):
				reino="localhost"	

			url=os.popen("hostname -f").read()
			url=url[0:len(url)-1]

			f=open("/etc/krb5.conf")
			g=open("/etc/krb5.conf.new","w")
			lineaf=f.readlines()
			f.close()

			f=open("/etc/krb5.conf")
			linea=f.readline()

			input("ANTES DE PROCESAR")
			
			while(linea!=lineaf[-1]):
				
				work=False

				if("[realms]" in linea):
					g.write(linea)
					g.write(" "+reino+" = {"+"\n")
					g.write(" kdc = "+url+"\n")
					g.write(" admin_server = "+url+"\n")
					g.write(" }\n")
					work=True

				if("[domain_realm]" in linea):
					g.write(linea)
					g.write(" ."+url+" = "+reino+"\n")
					g.write(" "+url+" = "+reino+"\n")
					work=True

				if("default_realm" in linea):
					c=trataLinea(linea)
					g.write(c+" "+reino+"\n")
					work=True

				if(work==False):
					g.write(linea)

				linea=f.readline()

			g.write(linea)
			f.close()
			g.close()

			#/var/kerberos/krb5kdc/kdc.conf

			f=open("/var/kerberos/krb5kdc/kdc.conf")
			lineaf=f.readlines()
			f.close()

			f=open("/var/kerberos/krb5kdc/kdc.conf")
			linea=f.readline()
			g=open("/var/kerberos/krb5kdc/kdc.conf.new","w")

			while(linea!=lineaf[-1]):
				work=False

				if("[realms]" in linea):
					g.write(linea)
					g.write("    "+reino+" = {"+"\n")
					linea=f.readline()
					work=True

				if(work==False):
					g.write(linea)

				linea=f.readline()

			g.write(linea)
			f.close()
			g.close()

			#creación bd
			if(nuevo):
				os.system("create -r -s "+reino)

			#/var/kerberos/krb5kdc/kadm5.acl
			os.system("rm /var/kerberos/krb5kdc/kadm5.acl")
			f=open("/var/kerberos/krb5kdc/kadm5.acl","w")
			f.write("* /admin@"+reino+"	*")
			f.close()

			#gestionFinal
			os.system("rm /etc/krb5.conf")
			os.system("mv /etc/krb5.conf.new /etc/krb5.conf")

			os.system("rm /var/kerberos/krb5kdc/kdc.conf")
			os.system("mv /var/kerberos/krb5kdc/kdc.conf.new /var/kerberos/krb5kdc/kdc.conf")

			#op="kadmin -q 'addprinc -randkey root/admin@'"+reino
			#os.system(op)

			#input("STOP")

			os.system("systemctl start krb5kdc kadmin")
			os.system("systemctl start kadmin.service")
			os.system("systemctl enable krb5kdc kadmin")
			os.system("systemctl enable kadmin.service")



		def confKD(nuevo):		#configuración para Debian
			#/etc/krb5.conf

			reino=input("Indique nombre del dominio ([ENTER] para establecer por defecto localhost): ")
			if(reino==''):
				reino="localhost"	

			url=os.popen("hostname -f").read()
			url=url[0:len(url)-1]

			g=open("/etc/krb5.conf.new","w")
			f=open("/etc/krb5.conf","r")
			lineaf=f.readlines()
			f.close()

			f=open("/etc/krb5.conf","r")
			linea=f.readline()

			while(linea!=lineaf[-1]):

				work=False

				if("default_realm" in linea):
					cadena=trataLinea(linea)
					g.write(cadena+" "+reino+"\n")	#reino que pone el propio usuario
					work=True

				if("[realms]" in linea):	#kdc y admin_server = ... pueden ir separados, pero aquí trabajarán en la misma máquina.
					g.write(linea)
					
					g.write("\t"+reino+" = {"+"\n")
					g.write("\t\t"+"kdc = "+url+"\n")
					g.write("\t\t"+"admin_server = "+url+"\n")
					g.write("\t"+"}"+"\n")
					work=True

				if("[domain_realm]" in linea):
					g.write(linea)
					g.write("\t"+"."+url+" = "+reino+"\n")
					g.write("\t"+url+ " = "+ reino+"\n")
					work=True
				
				if(work==False):	#de esta manera no replicamos las líneas escritas
					g.write(linea)
				
				linea=f.readline()

			g.write(linea)
			f.close()
			g.close()
			#----------

			#/etc/krb5kdc/kdc.conf
			f=open("/etc/krb5kdc/kdc.conf","r")
			lineaf=f.readlines()
			f.close()

			f=open("/etc/krb5kdc/kdc.conf","r")
			g=open("/etc/krb5kdc/kdc.conf.new","w")
			linea=f.readline()


			while(linea!=lineaf[-1]):
				work=False

				if("[realms]" in linea):
					g.write(linea)
					g.write("    "+reino+" = {"+"\n")
					linea=f.readline()
					work=True

				if(work==False):
					g.write(linea)

				linea=f.readline()

			g.write(linea)
			f.close()
			g.close()

			#gestionFinal
			os.system("rm /etc/krb5.conf")
			os.system("mv /etc/krb5.conf.new /etc/krb5.conf")

			os.system("rm /etc/krb5kdc/kdc.conf")
			os.system("mv /etc/krb5kdc/kdc.conf.new /etc/krb5kdc/kdc.conf")

			try:
				if(nuevo):
					subprocess.call(["krb5_newrealm"],shell=True)
					os.system("sudo dpkg-reconfigure krb5-kdc")

			except OSError:
				print("Error instalando krb5_newrealm")

			try:
				f=open("/etc/krb5kdc/kadm5.acl","r")
				g=open("/etc/krb5kdc/kadm5.acl.new","w")
				lineaf=f.readlines()

				c=lineaf[-1]
				c=c[1:len(c)]

				for i in lineaf:
					if(i==lineaf[-1]):
						g.write(c)
					else:
						g.write(i)

				f.close()
				g.close()

				os.system("rm /etc/krb5kdc/kadm5.acl")
				os.system("mv /etc/krb5kdc/kadm5.acl.new /etc/krb5kdc/kadm5.acl")

			except:
				print("No existe kadm5.acl")
				os.system(" '*root/admin *' >> /etc/krb5kdc/kadm5.acl")

			os.system("/etc/init.d/krb5-kdc restart")
			os.system("/etc/init.d/krb5-admin-server restart")


		# ----- llamadas -----
		s=systemK()

		if(s<2):	#gestión para no volver a escribir krb5_newrealm - sino fallaría
			if(s==0):
				confKD(True)
			else:
				confKD(False)
		else:
			if(s==2):
				confKC(True)
			else:
				confKC(False)

		# ---
	def Ranger():

		def entornoRangerC():		
			#ideal tratamiento recogidos en un log ...
			os.system("yum -y install gcc")
			
			#mysql
			s=subprocess.call(['rpm -qa | grep wget'], shell= True)

			if(s==1):
				os.system("yum -y install wget")

			os.system("wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm")
			os.system("rpm -ivh mysql-community-release-el7-5.noarch.rpm")
			os.system("yum -y update")
			os.system("yum -y install mysql-server")
			os.system("systemctl start mysql")
			#fin mysql ---

		def entornoRangerD():
			os.system("apt-get -y install gcc")
			os.system("apt-get -y install mysql-server")

			os.system("clear")

		def compilaRanger():
			os.system("mkdir dev")
			os.system("git clone https://github.com/apache/incubator-ranger.git")
			os.system("mv incubator-ranger dev")
			os.system("bash utilidades/maven.sh")


			os.system("cd dev/incubator-ranger && mvn clean compile package assembly:assembly install")
			print(" ")
			input(" Pulse [ENTER] para continuar.")
			
			def comp(debugg):	#REVISAR

				if(debugg):
				
					err=os.popen("cd dev/incubator-ranger && mvn clean compile package assembly:assembly install -X").read()
					
					if(err==''):
						q=input("Parece que hubo algún tipo de problema, ¿desea volver a ejecutar en modo depuración? s/n: ")

						if(q=='s' or q==''):
							comp(True)
				else:
					err=os.popen("cd dev/incubator-ranger && mvn clean compile package assembly:assembly install").read()

					if(err==''):
						q=input("Parece que hubo algún tipo de problema, ¿desea volver a ejecutar en modo depuración? s/n: ")

						if(q=='s' or q==''):
							comp(True)

			#comp(False)


		entorno=App.System()

		if(entorno):
			entornoRangerD()
		
		elif(entorno==False):
			entornoRangerC()

		print("COMPILANDO APACHE RANGER")

		compilaRanger()

		#print("INSTALANDO RANGER")


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
	app.run([])

