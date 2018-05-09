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
import devOP

class Storm():

	def run(self):
		menu=True
		os.system("clear")
		print(" ")
		
		global ro
		ro=PreEnt.gestionIn()

		rs=ro[0]
		rz=ro[1]

		PreEnt.preparaEnt(rs,rz)

		while(menu):
			os.system("clear")

			print(" ")
			print("===== Contramedidas Storm =====")
			print("1) Mejorar Integridad")
			print("2) Mejorar Autorización / Autenticación")
			print("3) Mejorar Anonimidad")
			print("===================================")
			print("4) Iniciar Storm")
			print("5) Volver a contramedidas generales")
			print("6) Salir")
			print("===================================")
			qm=input("Seleccionar una de las opciones: ")

			if(qm=="1"):
				Integridad.cfgSSL(rs)

			elif(qm=="2"):
				AtoAte.Menu(rs,rz)

			elif(qm=="4"):
				Storm.iniciaStorm(rs,rz)

			elif(qm=="5"):
				devOP.contramedidas.Menu()

			else:
				menu=False


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

	def confStorm(alm,rs):	#lectura del fichero de conf
		path=rs+"/conf/storm.yaml"

		for objeto in alm:

			f=open(path)
			g=open(path+".new","w")

			lineaf=f.readlines()
			f.close()

			f=open(path)
			linea=f.readline()

			while( linea != lineaf[-1] ):

				work=True

				if(objeto in linea):
					g.write(linea)
					g.write("\n")
					cadenas=alm[objeto]
					
					for cadena in cadenas:
						if(cadena == cadenas[-1]):
							g.write(" "+cadena+"\n")
							g.write("\n")
						else:
							g.write(" "+cadena+"\n")

					work=False

				elif(work):
					g.write(linea)

				linea=f.readline()
			
			f.close()
			g.close()

			cd="rm "+rs+"/conf/storm.yaml"
			cd2="mv "+rs+"/conf/storm.yaml.new "+rs+"/conf/storm.yaml"
			os.system(cd)
			os.system(cd2)

	def compruebaRuta(ruta):

		try:
			f=open(ruta+"/conf/storm.yaml")
			f.close()
			return False

		except:
			try:
				f=open(ruta+"/bin/zkServer.sh")
				f.close()
				return False
			except:
				print("No se encuentra la ruta: "+ruta)
				return True

	def iniciaStorm(rs,rz):
		cd=rz+"/bin/zkServer.sh start"
		cd2=rs+"/bin/storm nimbus & "+rs+"/bin/storm supervisor & "+rs+"/bin/storm ui &"
		os.system(cd)
		os.system(cd2)
		input("El sistema puede tardar 1 minuto aproximádamente en estar listo. Pulsa [Enter] para continuar.")

class PreEnt:	#prepararemos directorios o descargaremos storm & zookeeper.

	def gestionIn():
	
		s=input("¿Tiene Apache Storm instalado? s/n: ")
		zk=input("¿Tiene ZooKeeper instalado? s/n: ")

		obj=[]
		obj.append(s)
		obj.append(zk)

		if(Storm.validaPet(obj)):
			if(s == 's' or s==''):
				os.system("clear")
				rs=input("Indique ruta dónde se encuentre Apache Storm: ")

				if( Storm.compruebaRuta(rs)):
					PreEnt.gestionIn()

			elif(s=='n'):
				print("Descargando versión apache-storm-1.2.1")
				os.system("wget http://apache.claz.org/storm/apache-storm-1.2.1/apache-storm-1.2.1.tar.gz")
				os.system("tar -zxvf apache-storm-1.2.1.tar.gz")
				os.system("rm apache-storm-1.2.1.tar.gz")
				os.system("clear")
				rs=input("Indique ruta dónde desee guardar Apache Storm (por defecto /usr/apache-storm-1.2.1): ")

				if(rs==''):
					rs="/usr/apache-storm-1.2.1"

				cd="mv apache-storm-1.2.1 "+rs
				os.system(cd)

			if(zk=='s' or zk==''):
				os.system("clear")
				rz=input("Indique ruta dónde se encuentre ZooKeeper: ")

				if(Storm.compruebaRuta(rz) ):
					PreEnt.gestionIn()

			elif(zk=='n'):
				print("Descargando zookeeper-3.4.10")
				os.system("wget http://apache.claz.org/zookeeper/zookeeper-3.4.10/zookeeper-3.4.10.tar.gz")
				os.system("tar -zxvf zookeeper-3.4.10.tar.gz")
				os.system("clear")
				os.system("rm zookeeper-3.4.10.tar.gz")
				rz=input("Indique ruta dónde desee guardar Apache ZooKeeper (por defecto /usr/zookeeper-3.4.10): ")

				if(rz==''):
					rz="/usr/zookeeper-3.4.10"

				cd="mv zookeeper-3.4.10 "+rz
				os.system(cd)


			ro=[]
			ro.append(rs)
			ro.append(rz)

			return ro

		else:
			print("Por favor use 's'/'INTRO' o 'n'  para seleccionar la correspondiente acción")
			PreEnt.gestionIn()

	def preparaEnt(rs,rz):	#prepara la configuración inicial de Storm y ZooKeeper

		#configuración Storm
		path=rs+"/conf/storm.yaml"
		pathz=rz+"/conf/"

		def entStorm(path):

			f=open(path,"r")
			g=open(path+".new","w")

			lineaf=f.readlines()
			f.close()

			f=open(path)
			linea=f.readline()

			w2=False
			activa=False

			while(linea != lineaf[-1]):
				work=True

				if("storm.zookeeper.servers" in linea):
					if("#" in linea):
						cadena=linea[1:len(linea)]
						g.write(cadena)
					else:
						g.write(linea)

					w2=True
					work=False
					linea=f.readline()

				if( ("-" in linea) and (work==True) and (w2) ):
					if( ("#" in linea) and (activa==False) ):
						cadena="      - 'localhost' "+"\n"
						g.write(cadena)
						activa=True
					else:
						g.write(linea)

					linea=f.readline()

					if(linea != '-'):
						w2=False

				if("nimbus.seeds: " in linea):
					if("#" in linea):
						cadena=" nimbus.seeds: ['localhost']"+"\n"
						g.write(cadena)
					else:
						g.write(linea)

					linea=f.readline()

				if(work):
					g.write(linea)
					linea=f.readline()

			f.close()
			g.close()

			cd="rm "+path
			cd2="mv "+path+".new"+" "+path
			os.system(cd)
			os.system(cd2)


		def entZk(path):
			path2=path+"zoo_sample.cfg"
			try:
				f=open(path2,"r")
				f.close()
				cd="mv "+path2+" "+path+"zoo.cfg"
				os.system(cd)
			except:
				pass
				#el fichero ya estaba modificado

		entStorm(path)
		entZk(pathz)


class Integridad:	#opciones de integridad para Storm

	def cfgSSL(rs):
		os.system("clear")
		print(" ")
		print("Se crearán unos certificados específicos para Storm."+"\n")
		input("Pulsa [ENTER] para continuar.")
		os.system("clear")
		#devOP.contramedidas.Certificados()

		os.system(" ========= ")
		input("Creación de certificados finalizado, pulsa [ENTER] para continuar."+"\n")

		ssP=input("Ruta ssl (por defecto /home/ssl): ")
		if(ssP == ''):
			ssP="/home/ssl"

		claveAlm=input("Introduzca la clave usada para el almacén de certificados: ")
		clavePr=input("Introduzca la clave privada usada en los certificados: ")
		claveTr=input("Introduzca la clave usada para generar los certificados 'truststore': ")

		alm={}	#La clave privada es la que se solicita en el bash, la otra es del almacén
		
		#ui
		alm["nimbus.seeds: "]=["ui.https.want.client.auth: true",
		"ui.https.port: 8080",
		'ui.https.keystore.type: "jks"',
		"ui.https.keystore.path: "+'"'+ssP+"/server.keystore.jks"+'"',
		"ui.https.keystore.password: "+'"'+claveAlm+'"',
		"ui.https.key.password: "+'"'+clavePr+'"',
		"ui.https.truststore.path: "+'"'+ssP+"/server.truststore.jks"+'"',
		"ui.https.truststore.password: "+'"'+claveTr+'"',
		'ui.https.truststore.type: "jks"']	
		
		#drpc
		alm[' ui.https.truststore.type: ']=["drpc.https.port: 3774",
		'drpc.https.keystore.type: "jks"',
		"drpc.https.keystore.path: "+'"'+claveAlm+'"',
		"drpc.https.keystore.password: "+'"'+clavePr+'"']		

		Storm.confStorm(alm,rs)

class AtoAte:	#opciones para mejorar Autorización y Autenticación

	def Kerberos(rs,rz):	#COOKING
		
		devOP.contramedidas.Kerberos()	#realiza la preconfiguración e instalación

		# *** hay que crear usuarios y exportar los keytabs

		#modificación fichero zookeeper zoo.cnf - agregando Kerberos



		#generación storm_jaas ***
		cd="touch "+rs+"/conf/storm_jaas.conf"
		os.system(cd)
		f=open(rs+"/conf/storm_jaas.conf","w")

		f.write("StormServer {"+"\n")
		f.write("   com.sun.security.auth.module.Krb5LoginModule required \n")
		f.write("	useKeyTab=true \n")
		f.write('	keyTab="/home/tfg/Descargas/zookeeper-3.4.10/conf/keytabs/nimbus.keytab" \n')	#agregar ruta keytab
		f.write("	storeKey=true \n")
		f.write("	useTicketCache=false \n")
		f.write('	principal="storm/nimbus";\n')
		f.write("}; \n")

		f.write("StormClient { \n")
		f.write("	com.sun.security.auth.module.Krb5LoginModule required")
		f.write("	useKeyTab=true")
		f.write('	keyTab="/home/tfg/Descargas/zookeeper-3.4.10/conf/keytabs/storm.keytab" \n')	#agregar ruta keytab
		f.write("	storeKey=true \n")
		f.write("	useTicketCache=false \n")
		f.write('	serviceName="storm" \n')
		f.write('	principal="storm"; \n')
		f.write("}; \n")

		f.write("Client { \n")
		f.write("	com.sun.security.auth.module.Krb5LoginModule required \n")
		f.write("	useKeyTab=true \n")
		f.write('	keyTab="/home/tfg/Descargas/zookeeper-3.4.10/conf/keytabs/storm.keytab" \n')	#agregar ruta keytab
		f.write("	storeKey=true \n")
		f.write("	useTicketCache=false \n")
		f.write('	serviceName="zookeeper" \n')
		f.write('	principal="storm"; \n')
		f.write("}; \n")

		f.close()

		#generación zk_jaas	***
		cd="touch "+rs+"/conf/zk_jaas.conf"
		os.system(cd)
		f=open(rs+"/conf/zk_jaas.conf","w")

		f.write("Server { \n")
		f.write("	com.sun.security.auth.module.Krb5LoginModule required \n")
		f.write("	useKeyTab=true \n")
		f.write('	keyTab="/home/tfg/Descargas/zookeeper-3.4.10/conf/keytabs/zookeeper.keytab" \n')
		f.write("	storeKey=true \n")
		f.write("	useTicketCache=false \n")
		f.write('	serviceName="zookeeper" \n')
		f.write('	principal="zookeeper/localhost"; \n')
		f.write("}; \n")

		f.close()


	def Menu(rs,rz):

		obj=[]

		kerberos=input("¿Instalar y configurar kerberos? s/n: ")
		ranger=input("¿Compilar e instalar Apache Ranger? s/n: ")
		
		obj.append(kerberos)
		obj.append(ranger)

		os.system("clear")
		print("Parámetros de configuración seleccionados: Kerberos ["+kerberos+"], Apache Ranger["+ranger+"]")
		contniuar=input("¿Continuar con configuración seleccionada? s/n: ")

		obj.append(continuar)
		if(Storm.validaPet(obj)):
			if(kerberos=='' or kerberos=='s'):
				Kerberos(rs,rz)	#instala y preconfigura kerberos

			if(ranger=='' or ranger=='s'):
				devOP.contramedidas.Ranger()	#compila ranger
		else:
			print("[ERROR] Por favor use 's'/'INTRO' o 'n' para seleccionar la correspondiente acción")
			print("Volviendo al menu principal ...")
			AtoAte.Menu()

if __name__== '__main__':
	storm=Storm()
	storm.run() 