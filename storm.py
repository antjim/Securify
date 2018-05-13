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

	def run(self,ro):
		os.system("clear")
		print(" ")
		
		#global ro
		
		if(ro==[]):
			ro=PreEnt.gestionIn()

		rs=ro[0]
		rz=ro[1]

		PreEnt.preparaEnt(rs,rz)

		while(True):
			os.system("clear")
			Storm.logo()
			print(" ")
			print("========== Contramedidas Storm ==========")
			print("1) Mejorar Integridad")
			print("2) Mejorar Autorización / Autenticación")
			print("3) Mejorar Anonimidad")
			print("=========================================")
			print("4) Iniciar Storm")
			print("5) Ayuda")
			print("6) Volver a contramedidas generales")
			print("7) Salir")
			print("=========================================")
			qm=input("Seleccionar una de las opciones: ")

			if(qm=="1"):
				Integridad.cfgSSL(rs)

			elif(qm=="2"):
				AtoAte.Menu(rs,rz)

			elif(qm=="3"):	
				AtoAte.Kerberos(rs,rz)

			elif(qm=="4"):
				Storm.iniciaStorm(rs,rz)

			elif(qm=="6"):
				devOP.contramedidas.Menu(ro)

			elif(qm=="5"):
				devOP.ayuda.Menu(ro)

			else:
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

	def confStorm(alm,rs):	#lectura del fichero de conf

		if("zookeeper" in rs):
			path=rs+"/conf/zoo.cfg"
			cd="rm "+rs+"/conf/zoo.cfg"
			cd2="mv "+rs+"/conf/zoo.cfg.new "+rs+"/conf/zoo.cfg"
		else:
			path=rs+"/conf/storm.yaml"
			cd="rm "+rs+"/conf/storm.yaml"
			cd2="mv "+rs+"/conf/storm.yaml.new "+rs+"/conf/storm.yaml"

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
					
					cadenas=alm[objeto]
					
					for cadena in cadenas:
						if(cadena in cadenas[-1]):
							g.write(" "+cadena+"\n")
							g.write("\n")
						else:
							g.write(" "+cadena+"\n")

					g.write(linea)
					g.write("\n")

					work=False

				elif(work):
					g.write(linea)

				linea=f.readline()
			print(linea)
			g.write(linea)

			f.close()
			g.close()

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

	def generaLineas(alm,rs):

		path=rs+"/conf/storm.yaml"
		cd="rm "+rs+"/conf/storm.yaml"
		cd2="mv "+rs+"/conf/storm.yaml.new "+rs+"/conf/storm.yaml"

		f=open(path)
		lineaf=f.readlines()
		f.close()

		f=open(path)
		g=open(rs+"/conf/storm.yaml.new","w")
		linea=f.readline()

		for objeto in alm:	#solo habrá una iteración - uso de python3 impide coger directamente con keys()
			cant=len(alm[objeto])
			work=False
			cont=False

			while(linea != lineaf[-1]):

				if(objeto in linea):
					work=True
					input(linea)

				if(work):
					cont==True
					if((linea=="# \n") or (linea==" \n")):
						for j in range(cant):
							g.write("\n")
						linea=f.readline()
					else:
						input(linea)
						input(lineaf[-1])
						g.write(linea)
						linea=f.readline()
				
				if(cont==False):
					g.write(linea)
					input(linea)
					linea=f.readline()

			g.write(linea)

			input("HECHO")
			f.close()
			g.close()
			input("PAUSA")
			os.system(cd)				
			os.system(cd2)


	def logo():
		print(" __                      _  __       ")
		print("/ _\ ___  ___ _   _ _ __(_)/ _|_   _ ")
		print("\ \ / _ \/ __| | | | '__| | |_| | | |")
		print("_\ \  __/ (__| |_| | |  | |  _| |_| |")
		print("\__/\___|\___|\__,_|_|  |_|_|  \__, |")
		print("			       |___/")

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

			cd="rm "+path
			cd2="mv "+path+".new"+" "+path

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

			g.write(linea)
			f.close()
			g.close()

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

		ssP=input("Ruta ssl (por defecto /home/.ssl): ")
		if(ssP == ''):
			ssP="/home/.ssl"

		existe=os.popen("ls "+ssP).read()
		if(existe==''):
			devOP.contramedidas.Certificados()

		os.system(" ========= ")
		input("Creación de certificados finalizado, pulsa [ENTER] para continuar."+"\n")

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
		alm['ui.https.truststore.type: ']=["drpc.https.port: 3774",
		'drpc.https.keystore.type: "jks"',
		"drpc.https.keystore.path: "+'"'+claveAlm+'"',
		"drpc.https.keystore.password: "+'"'+clavePr+'"']		

		Storm.confStorm(alm,rs)

class AtoAte:	#opciones para mejorar Autorización y Autenticación

	def Kerberos(rs,rz):	#COOKING
		
		devOP.contramedidas.Kerberos()	#realiza la preconfiguración e instalación

		# *** hay que crear usuarios y exportar los keytabs
		#print("Por favor ingresa a continuación lo siguiente: addprinc root/admin")
		#print("Después pulsa la tecla 'q' para salir.")
		#input("Pulsar [ENTER] para continuar.")
		#os.system("kadmin.local")

		os.system("clear")

		print(" ")
		dr=input("¿Dónde desea guardar los Keytabs necesarios? Indique ruta (Por defecto /pathStorm/conf/.keytabs): ")

		if(dr==''):
			dr=rs+"/conf/.keytabs"
			os.system("mkdir "+dr)

		os.system('kadmin.local -q "addprinc -randkey nimbus" ')
		os.system('kadmin.local -q "addprinc -randkey storm" ')
		os.system('kadmin.local -q "addprinc -randkey zookeeper" ')

		os.system('kadmin.local -q "ktadd -k '+dr+'/nimbus.keytab storm" ')
		os.system('kadmin.local -q "ktadd -k '+dr+'/storm.keytab storm" ')
		os.system('kadmin.local -q "ktadd -k '+dr+'/zookeeper.keytab zookeeper" ')


		#generación storm_jaas ***
		cd="touch "+rs+"/conf/storm_jaas.conf"
		os.system(cd)
		f=open(rs+"/conf/storm_jaas.conf","w")

		f.write("StormServer {"+"\n")
		f.write("   com.sun.security.auth.module.Krb5LoginModule required \n")
		f.write("	useKeyTab=true \n")
		f.write('	keyTab="'+dr+'/nimbus.keytab" \n')	
		f.write("	storeKey=true \n")
		f.write("	useTicketCache=false \n")
		f.write('	principal="nimbus";\n')
		f.write("}; \n")

		f.write("StormClient { \n")
		f.write("	com.sun.security.auth.module.Krb5LoginModule required")
		f.write("	useKeyTab=true")
		f.write('	keyTab="'+dr+'/storm.keytab" \n')	
		f.write("	storeKey=true \n")
		f.write("	useTicketCache=false \n")
		f.write('	serviceName="storm" \n')
		f.write('	principal="storm"; \n')
		f.write("}; \n")

		f.write("Client { \n")
		f.write("	com.sun.security.auth.module.Krb5LoginModule required \n")
		f.write("	useKeyTab=true \n")
		f.write('	keyTab="'+dr+'/storm.keytab" \n')	
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
		f.write('	keyTab="'+dr+'/zookeeper.keytab" \n')
		f.write("	storeKey=true \n")
		f.write("	useTicketCache=false \n")
		f.write('	serviceName="zookeeper" \n')
		f.write('	principal="zookeeper"; \n')
		f.write("}; \n")

		f.close()


		#modificación fichero zookeeper zoo.cnf - agregando Kerberos

		d={}
		d['autopurge.purgeInterval=']=["authProvider.1 = org.apache.zookeeper.server.auth.SASLAuthenticationProvider",
		"-Djava.security.auth.login.config="+rz+"/zk_jaas.conf",
		"kerberos.removeHostFromPrincipal = true",
		"kerberos.removeRealmFromPrincipal = true",
		"jaasLoginRenew=3600000"]
		
		Storm.confStorm(d,rz)	#en este caso, el fichero es zoo.cfg

		
		#modificación fichero storm.yaml

		d2={}
		d3={}

		#storm-java
		d2["storm.zookeeper.servers:"]=['java.security.auth.login.config: "'+rs+'/conf/storm_jaas.conf"',
		'storm.thrift.transport: "org.apache.storm.security.auth.kerberos.KerberosSaslTransportPlugin"',
		'storm.principal.tolocal: "org.apache.storm.security.auth.KerberosPrincipalToLocal"',
		'storm.zookeeper.superACL: "sasl:storm"']

		#nimbus - supervisor - ui
		d3["nimbus.seeds:"]=['nimbus.childopts: "-Xmx1024m -Djava.security.auth.login.config='+rs+'/conf/storm_jaas.conf"',
		'nimbus.authorizer: "org.apache.storm.security.auth.authorizer.SimpleACLAuthorizer"',
		'supervisor.childopts: "-Xmx256m -Djava.security.auth.login.config='+rs+'/conf/storm_jaas.conf"',
		'ui.childopts: "-Xmx768m -Djava.security.auth.login.config='+rz+'/conf/storm_jaas.conf"']

		#Storm.generaLineas(d2,rs)
		Storm.confStorm(d2,rs)

		#Storm.generaLineas(d3,rs)
		Storm.confStorm(d3,rs)


	def Menu(rs,rz):

		obj=[]

		kerberos=input("¿Instalar y configurar kerberos? s/n: ")
		ranger=input("¿Compilar e instalar Apache Ranger? s/n: ")
		
		obj.append(kerberos)
		obj.append(ranger)

		os.system("clear")
		print("Parámetros de configuración seleccionados: Kerberos ["+kerberos+"], Apache Ranger["+ranger+"]")
		continuar=input("¿Continuar con configuración seleccionada? s/n: ")

		os.system("clear")

		obj.append(continuar)
		if(Storm.validaPet(obj)):
			if(kerberos=='' or kerberos=='s'):
				AtoAte.Kerberos(rs,rz)	#instala y preconfigura kerberos

			if(ranger=='' or ranger=='s'):
				devOP.contramedidas.Ranger()	#compila ranger
		else:
			print("[ERROR] Por favor use 's'/'INTRO' o 'n' para seleccionar la correspondiente acción")
			print("Volviendo al menu principal ...")
			AtoAte.Menu(rs,rz)

if __name__== '__main__':
	storm=Storm()
	storm.run() 