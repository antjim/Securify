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
		PreEnt.gestionIn()

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

			if(qm==1):
				Integridad.cfgSSL()

			elif(qm==4):
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


class PreEnt:	#prepararemos directorios o descargaremos storm & zookeeper.

	def gestionIn():
	
		s=input("¿Tiene Apache Storm instalado? s/n: ")
		zk=input("¿Tiene ZooKeeper instalado? s/n: ")

		obj=[]
		obj.append(s)
		obj.append(zk)

		if(validaPet(obj)):
			if(s == 's' or s==''):
				rs=input("Indique ruta dónde se encuentre Apache Storm: ")
			elif(s=='n'):
				print("Descargando versión apache-storm-1.2.1")
				os.system("wget http://apache.claz.org/storm/apache-storm-1.2.1/apache-storm-1.2.1.tar.gz")
				os.system("tar -zxvf apache-storm-1.2.1.tar.gz")
				os.system("rm apache-storm-1.2.1.tar.gz")
				rs=input("Indique ruta dónde desee guardar Apache Storm (por defecto /usr/apache-storm-1.2.1): ")

				if(rs==''):
					rs="/usr/"

				cd="mv apache-storm-1.2.1 "+rs
				os.system(cd)

			if(zk=='s' or zk==''):
				rz=input("Indique ruta dónde se encuentre ZooKeeper: ")
			elif(zk=='n'):
				print("Descargando zookeeper-3.4.10")
				os.system("wget http://apache.claz.org/zookeeper/zookeeper-3.4.10/zookeeper-3.4.10.tar.gz")
				os.system("tar -zxvf zookeeper-3.4.10.tar.gz")
				os.system("rm zookeeper-3.4.10.tar.gz")
				rs=input("Indique ruta dónde desee guardar Apache ZooKeeper (por defecto /usr/zookeeper-3.4.10): ")

				if(rz==''):
					rz="/usr/"

				cd="mv zookeeper-3.4.10 "+rz
				os.system(cd)
		else:
			print("Por favor use 's'/'INTRO' o 'n'  para seleccionar la correspondiente acción")
			PreEnt.gestionIn()


class Integridad:	#opciones de integridad para Storm

	def cfgSSL():
		print("Cooking")

		print("Se crearán unos certificados específicos para Storm.")
		input("Pulsa [ENTER] para continuar.")
		#os.system("clear")
		#devOP.contramedidas.Certificados()


if __name__== '__main__':
	storm=Storm()
	storm.run() 