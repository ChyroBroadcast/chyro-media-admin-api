from chyro_sdk import Chyro, print_json


chyro = Chyro('test.chyro.fr', 'user', "password", log=True)
print_json(chyro.get('file', id=3009))
print_json(chyro.get('program', id=15707))
print_json(chyro.get('schedule', start=1475225248, duration=72, bc=1))
print_json(chyro.get('framerate'))
print_json(chyro.search('program', category_id=41, subcategory_id=107))
print(chyro.update('mediahr', 3009, {'mediahrtcin': '00:00:00:20', 'mediahrtcout': '00:45:00:00'}))

