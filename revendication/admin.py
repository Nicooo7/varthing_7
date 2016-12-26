from django.contrib import admin

from .models import Proposition
from .models import Theme
from .models import Lieu
from .models import Profile
from .models import Soutien
from .models import Proximite
from .models import Autre_utilisateur
from .models import Organisation
from .models import Evenement
from .models import Proximite


admin.site.register(Proposition)
admin.site.register(Theme)
admin.site.register(Lieu)
admin.site.register(Profile)
admin.site.register(Soutien)
admin.site.register(Autre_utilisateur)
admin.site.register(Proximite)
admin.site.register(Organisation)
admin.site.register(Evenement)
