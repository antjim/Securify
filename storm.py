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
			print("4) Volver a contramedidas generales")
			print("5) Salir")
			print("===================================")
			qm=input("Seleccionar una de las opciones: ")

			if(qm=="1"):
				Integridad.cfgSSL(rs)

			elif(qm=="4"):
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
		
		f.open(path)
		g.open(path+".new","w")

		lineaf=f.readlines()
		f.close()

		for objeto in alm:
			f.open(path)		
			linea=f.readline()

			while( linea != lineaf[-1] ):

				work=True

				if(objeto in linea):
					g.write(linea)
					cadenas=alm[objeto]
					
					for cadena in cadenas:
						if(cadena == cadenas[-1]):
							g.write(cadena+"\n\n")
						else:
							g.write(cadena+"\n")

					work=False

				elif(work):
					g.write(linea)

				linea=f.readline()

			g.close()
			f.close()

			cd="rm "+rs+"/conf/storm.yaml"
			cd2="mv "+rs+"/conf/storm.yaml.new "+rs+"/conf/storm.yaml"
			#os.system(cd)
			#os.system(cd2)

	def compruebaRuta(ruta):

		try:
			f=open(ruta+"/conf/storm.yaml")
			return False

		except:
			print("No existe el directorio Storm en la ruta: "+ruta)
			return True
		

class PreEnt:	#prepararemos directorios o descargaremos storm & zookeeper.

	def gestionIn():
	
		s=input("¿Tiene Apache Storm instalado? s/n: ")
		zk=input("¿Tiene ZooKeeper instalado? s/n: ")

		obj=[]
		obj.append(s)
		obj.append(zk)

		ro=[]

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

				if(Storm.compruebaRuta(rz) == False):
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

			f=open(path)
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

		def entZk(path):
			try:
				f=open(path)
				cd="mv "+path+"zoo_sample.cfg"+" "+path+"zoo.cfg"
				os.system(cd)
			except:
				pass
				#el fichero ya estaba modificado

		entStorm(path)
		entZk(pathz)


class Integridad:	#opciones de integridad para Storm

	def cfgSSL(rs):

		print("Se crearán unos certificados específicos para Storm.")
		input("Pulsa [ENTER] para continuar.")
		os.system("clear")
		devOP.contramedidas.Certificados()

		#input("Creación de certificados finalizado, pulsa [ENTER] para continuar.")
		claveAlm=input("Introduzca la clave para el almacén de certificados usados: ")
		clavePr=input("Introduzca la clave privada usada en los certificados: ")

		alm={}	#La clave privada es la que se solicita en el bash, la otra es del almacén
		#ui
		alm["nimbus.seeds: "]=["ui.https.port: 8080","ui.https.keystore.type: 'jks'","ui.https.keystore.path: "+"'"+claveAlm+"'","ui.https.keystore.password: "+"'"+clavePr+"'"]	
		#drpc
		alm["ui.https.keystore.password: "]=["drpc.https.port: 3774","drpc.https.keystore.type: 'jks'","drpc.https.keystore.path: "+"'"+claveAlm+"'","drpc.https.keystore.password: "+"'"+clavePr+"'"]		

		Storm.confStorm(alm,rs)

if __name__== '__main__':
	storm=Storm()
	storm.run() 