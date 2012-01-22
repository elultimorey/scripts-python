import urllib2
import sys

# Ejemplo url: Murcia en Enero de 1981
# http://clima.tiempo.com/clima-en-murcia-084300-1981-Enero.html

# Convierte un string en otro que servira para obtener una url valida
def city (ciudad):
        return ciudad.lower().replace(" - ", " ").replace(" / ", " ").replace("-", "+").replace(" ", "+")

# Obtiene el codigo que acompana a la ciudad en la url
def getCode(ciudad):
        url = "http://clima.tiempo.com/clima-en-Europa-Espana-SP.html"
        usock = urllib2.urlopen(url)
        data = usock.read()
        usock.close()

        spl = "clima-en-" + city(ciudad)  + "-"

        c = data.split(spl)
        c1 = c[1].split(".")
        return c1[0]
# Convierte un float a string, cambiando ademas el punto por la coma (para copiar en EXEL y crear graficas)
def float_to_str(number):
	return str(number).replace(".", ",")

# Los parametros son los que se le pasan al programa "python"
#	La linea en consola seria "python programa.py "Murcia" 1992 2011 datos.txt"
#	El parametro 0 seria "programa.py" y el 4 "datos.txt"
# 		El parametro del documento en el que guardar los datos es opcional

# Se abre el documento indicado con la opcion de escribir
if (len(sys.argv) == 5):
	file = open(sys.argv[4], "w")
if (len(sys.argv) > 3):
	if (len(sys.argv[1].split("("))==1):
		meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
		# Todas las urls de la web clima.tiempo.com tienen el mismo patron
		base_url = 'http://clima.tiempo.com/clima-en-' + city(sys.argv[1])  +  '-' + getCode(sys.argv[1]) + "-"
		# Se abre el documento indicado con la opcion de escribir
		# Si ocurre un error en un mes de un anyo se mostrara esta linea
		mensaje_fallo_url = "> (*): No hay datos suficientes en los anyos marcados en la web http://clima.tiempo.com/clima-en-Europa-Espana-SP.html"
		mostrar = False
	
		# Se escribe en el documento de texto la cabecera de los datos
		if (len(sys.argv) == 5):
			file.write("ANO\tPRECIP.\tT_MIN\tT_MAX\tT_MEDIA\n")
		print "ANO\tPRECIP.\tT_MIN\tT_MAX\tT_MEDIA"
	
		# El bucle exterior va desde el ano de inicio al de fin+1 de uno en uno
		for i in range(int(sys.argv[2]), int(sys.argv[3])+1, 1):
			temperatura_maxima = -1000.0 	# No creo que se alcance en ningun lugar los -1000.0 grados
			temperatura_minima = 1000.0 	# Ni tampoco los +1000.0
			precipitaciones = 0.0
			temperatura = 0.0
			fallo = False
		
			# El bucle recorre el array de string de los meses
			for mes in meses:
				# Se le anade el final de la url
				url = base_url + str(i) + '-' + mes + '.html'
				# Se abre un socket a la url para obtener el HTML luego se cierra
				usock = urllib2.urlopen(url)			
				data = usock.read()
				usock.close()
			
				# Se recorta el HTML por "Temperatura M&aacute;xima mensual:</b> "
				tamaxima = data.split("Temperatura M&aacute;xima mensual:</b> ")
				# Si exite en tamaxima tendremos mas de un objeto
				if (len(tamaxima)>1):
					# Si existen datos obtenemos los datos recortando el HTML por donde nos interesa
					tamax = float(tamaxima[1].split(" ")[0])
					if (tamax > temperatura_maxima):
						temperatura_maxima = tamax
					tamin = float(data.split("Temperatura M&iacute;nima mensual:</b> ")[1].split(" ")[0])
					if (tamin < temperatura_minima):
						temperatura_minima = tamin
					precipitaciones += float(data.split("Precipitaci&oacute;n Total mensual:</b> ")[1].split(' ')[0])
			 		temperatura += float(data.split("Temperatura Media mensual:</b> ")[1].split(' ')[0])
				else:
					# Si hay un fallo en un mes el anyo se detiene
					fallo = True
					mostrar = True
					break

			if (not fallo):
				temperatura = temperatura/12
				line = str(i) + "\t"  + float_to_str(precipitaciones) + "\t" + float_to_str(temperatura_minima) + "\t" + float_to_str(temperatura_maxima) + "\t"  + float_to_str(temperatura)
			else:
				line = str(i) + "\t*\t*\t*\t*"
			if (len(sys.argv) == 5):
				file.write(line + "\n")
			print line

		if (mostrar):
			if (len(sys.argv) == 5):
				file.write(mensaje_fallo_url)
			print mensaje_fallo_url
	else:
		print "> Esa estacion no tenia datos cuando se hizo este script y para no ensuciar el codigo se prefirio no incluirla"
else:
	print "> ERROR: el numero de parametros es incorrecto. (CIUDAD FECHA_INI FECHA_FIN ARCHIVO_SALIDA)"
