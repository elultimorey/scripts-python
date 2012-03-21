import urllib2
import sys
import re

# Los parametros son los que se le pasan al programa "python"
#	La linea en consola seria "python programa.py screen-user"
if (len(sys.argv) == 2):
	try:
		# url de la version web de twitter del perfil del usuario especificado
		url = 'http://mobile.twitter.com/'+sys.argv[1]+'/about';
		# Se abre un socket a la url para obtener el HTML luego se cierra
		usock = urllib2.urlopen(url);
		data = usock.read();
		usock.close();

		print ">>> Resumen de usuario:";

		# screen-name
		recomp = re.compile('<div class=\'user-screen-name\'>\n<strong>(.+)</strong>\n\((.+)\)');
		print '\tscreen-name:\t' + recomp.search(data).group(1);
		print '\tuser_name:\t' + recomp.search(data).group(2);

		# following
		recomp = re.compile('<a href="http://mobile.twitter.com/'+sys.argv[1]+'/following">Following:(.+)</a>');
		print '\tfollowing:\t' + recomp.search(data).group(1);

		# followers
		recomp = re.compile('<a href="http://mobile.twitter.com/'+sys.argv[1]+'/followers">Followers:(.+)</a>');
		print '\tfollowers:\t' + recomp.search(data).group(1);

		# location
		recomp = re.compile('<b>Location:</b>\n(.+)\n');
		if recomp.search(data):
			print '\tlocation:\t' + recomp.search(data).group(1);

		# bio
		recomp = re.compile('<b>Bio:</b>\n(.+)\n');
		if recomp.search(data):
			print '\tbio:\t\t' + recomp.search(data).group(1);

		# web
		recomp = re.compile('<b>Web:</b>\n<a href="(.+)" target="twitter_external">');
		if recomp.search(data):
			print '\tweb:\t\t' + recomp.search(data).group(1);

		#imagen
		recomp = re.compile('class="list-tweet-img" lowend_override="true" src="(.+)"');
		if recomp.search(data):
			print 'imagen de perfil:\t' + recomp.search(data).group(1).replace('_normal', '_reasonably_small');

	except:
		print '>>> ERROR: el usuario no existe.';
else:
	print '>>> ERROR: el numero de parametros es incorrecto.';
