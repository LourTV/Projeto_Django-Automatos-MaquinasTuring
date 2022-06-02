from django.urls import path
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "website"

urlpatterns = [
    path('', views.layout, name='layout'),
    path('Introducao', views.Introducao, name='Introducao'),
    path('MostraAutomatos', views.MostraAutomatos, name='MostraAutomatos'),
    path('MostraMaquinasTuring', views.MostraMaquinasTuring, name='MostraMaquinasTuring'),
    path('CriarAutomato', views.CriarAutomato, name='CriarAutomato'),
    path('CriarMaquinaTuring', views.CriarMaquinaTuring, name='CriarMaquinaTuring'),
    path('AutomatoUpload', views.AutomatoUpload, name='AutomatoUpload'),
    path('MaquinaTuringUpload', views.MaquinaTuringUpload, name='MaquinaTuringUpload'),
    path('TestarAutomato/<int:automato_id>', views.TestarAutomato, name='TestarAutomato'),
    path('TestarMaquinaTuring/<int:maquinaturing_id>', views.TestarMaquinaTuring, name='TestarMaquinaTuring'),
    path('EscolhaCriacaoAutomato', views.EscolhaCriacaoAutomato, name='EscolhaCriacaoAutomato'),
    path('EscolhaCriacaoMaquinaTuring', views.EscolhaCriacaoMaquinaTuring, name='EscolhaCriacaoMaquinaTuring'),
    path('EditarAutomato/<int:automato_id>', views.EditarAutomato, name='EditarAutomato'),
    path('EditarMaquinaTuring/<int:maquinaturing_id>', views.EditarMaquinaTuring, name='EditarMaquinaTuring'),
    path('DetalhesAutomato/<int:automato_id>', views.DetalhesAutomato, name='DetalhesAutomato'),
    path('DetalhesMaquinaTuring/<int:maquinaturing_id>', views.DetalhesMaquinaTuring, name='DetalhesMaquinaTuring'),
    path('ApagaAutomato/<int:automato_id>', views.ApagaAutomato, name='ApagaAutomato'),
    path('ApagaMaquinaTuring/<int:maquinaturing_id>', views.ApagaMaquinaTuring, name='ApagaMaquinaTuring'),

]

urlpatterns += staticfiles_urlpatterns()