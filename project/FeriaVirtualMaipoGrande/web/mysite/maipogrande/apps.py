from django.apps import AppConfig


class MaipograndeConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maipogrande'

    def ready(self):
        
    	import maipogrande.signals