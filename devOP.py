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

# -- clases --

class App():

	def run(self):
		menu=True

		preprocesado.Menu()

		while(menu):
			os.system("clear")
			contramedidas.Menu()
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
			print("Instalando Kerberos ","\n")
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
				print("** En caso de aparecer un cuadro para escribir el reino recomendamos usar la tecla 'ESC' para que el sistema se encargue por si mismo. **","\n")
				input("Pulsa [ENTER] para continuar.")
				subprocess.call(['apt-get','-y','install','krb5-kdc','krb5-admin-server'])
				os.system("clear")
				return True
		
			except OSError:
				try:
					subprocess.call(['yum','-y','install','krb5-kdc','krb5-admin-server'])
					os.system("clear")
					return False

				except OSError:
					print("[Error] Sistema operativo soportado para Debian, derivados y CentOS")
		

		#configuración ...
		def trataLinea(linea):
			res=''
			for i in range (len(linea)):
				if(linea[i]=="="):
					res+=linea[i]
					break
				else:
					res+=linea[i]
			return res

		def confKC():		#configuración para CentOS | COOKING
			#/etc/krb5.conf
		
			reino=input("Indique nombre del dominio ([ENTER] para establecer por defecto localhost): ")
			if(reino==''):
				reino="localhost"	

			#reinoK=input("")
			#reinoA=input("")
			url=reino.lower()

			f=open("/etc/krb5.conf")
			g=open("/etc/krb5.conf.new","w")
			lineaf=f.readlines()
			f.close()

			f=open("/etc/krb5.conf")
			linea=f.readline()
			
			while(linea!=lineaf[-1]):
				
				work=False

				if("[realms]" in linea):
					g.write(linea)
					g.write(" "+reino+" = {"+"\n")
					g.write(" kdc = "+url+"\n")
					g.write(" admin_server = "+url+"\n")
					work=True

				if("[domain_realm]" in linea):
					g.write(linea)
					g.write("."+url+" = "+reino+"\n")
					g.write(url+" = "+reino+"\n")
					work=True

				if("default_realm"):
					g.write(linea)
					c=trataLinea(linea)
					g.write(c+" "+reino)
					work=True

				if(work==False):
					g.write(linea)

				linea=f.readline()

			f.close()
			g.close()

			#/var/kerberos/krb5kdc/kdc.conf

			f=open("/var/kerberos/krb5kdc/kdc.conf")
			lineaf=f.readlines()
			f.close()

			f=open("/var/kerberos/krb5kdc/kdc.conf")
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

			#/var/kerberos/krb5kdc/kadm5.acl
			os.system("rm /var/kerberos/krb5kdc/kadm5.acl")
			f=open("/var/kerberos/krb5kdc/kadm5.acl","w")
			f.write("*/admin@"+reino+"	*")

			#gestionFinal
			os.system("rm /etc/krb5.conf")
			os.system("mv /etc/krb5.conf.new /etc/krb5.conf")

			os.system("rm /var/kerberos/krb5kdc/kdc.conf")
			os.system("mv /var/kerberos/krb5kdc/kdc.conf.new /var/kerberos/krb5kdc/kdc.conf")

			op="kadmin -q 'addprinc -randkey root/admin@'"+reino
			os.system(op)

			os.system("systemctl start krb5kdc.service")
			os.system("systemctl start kadmin.service")
			os.system("systemctl enable krb5kdc.service")
			os.system("systemctl enable kadmin.service")



		def confKD():		#configuración para Debian
			#/etc/krb5.conf

			reino=input("Indique nombre del dominio ([ENTER] para establecer por defecto localhost): ")
			if(reino==''):
				reino="localhost"	
			#reinoK=input("")
			#reinoA=input("")
			url=reino.lower()

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
					g.write("\t\t"+"kdc = krb5."+url+"\n")
					g.write("\t\t"+"admin_server = krb5."+url+"\n")
					g.write("\t"+"}"+"\n")
					work=True

				if("[domain_realm]" in linea):
					g.write(linea)
					g.write("\n\t"+"."+url+" = "+reino)
					g.write("\n\t"+url+ " = "+ reino+"\n")
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
				os.system(" '*/admin *' >> /etc/krb5kdc/kadm5.acl")

			os.system("/etc/init.d/krb5-kdc restart")
			os.system("/etc/init.d/krb5-admin-server restart")


		# ----- llamadas -----
		s=systemK()

		if(s):
			confKD()
		else:
			confKC()

		# ---
	def Ranger():

		def entornoRangerC():		#BUGS EN MYSQL
			#ideal tratamiento recogidos en un log ...
			os.system("yum -y install gcc")
			
			#mysql
			s=subprocess.call(['rpm -qa | grep wget'], shell= True)

			if(s==1):
				os.system("yum -y install wget")

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
			#os.system("cd dev/incubator-ranger && mvn clean")
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

