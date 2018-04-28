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

		while(menu):
			pre=input("¿Desea realizar el procesado? s/n:")
			if(pre=="s"):
				print("Instalando JAVA - jre 1.8.0_171")
				preprocesado.javaInstall()
				print("[OK] Instalación de Java finalizada.")



class preprocesado:
	def __init__(self,vmaven):
		self.vmaven=vmaven
	
	def javaInstall():
		os.system("mkdir /usr/java")
		os.system("tar -zxvf  utilidades/jre1.8.0_171.tar.gz")
		os.system("mv jre1.8.0_171 /usr/java")
		os.system("export JAVA_HOME=/usr/java/jre1.8.0_171")
		os.system("export PATH=$PATH:/usr/java/jre1.8.0_171/bin")


# -- fin clases --


if __name__== '__main__':
	app=App()
	app.run()

