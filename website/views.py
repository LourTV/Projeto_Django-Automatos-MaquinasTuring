import json
import os

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import AutomatoForm, ObterSequenciaForm, MaquinaTuringForm
from .models import Automato
from .models import MaquinaTuring
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from graphviz import Digraph
app_name = "website"
def layout(request):
	return render(request, 'website/layout.html')
def MostraAutomatos(request):
	context = {'website': Automato.objects.all()}
	return render(request, 'website/MostraAutomatos.html', context)
def MostraMaquinasTuring(request):
	context = {'website': MaquinaTuring.objects.all()}
	return render(request, 'website/MostraMaquinasTuring.html', context)

def Introducao(request):
	return render(request, 'website/Introducao.html')
def CriarAutomato(request):
	form = AutomatoForm(request.POST or None)
	if form.is_valid():
		form.save()
		IndiceUltimoAutomato = Automato.objects.all().count() - 1
		desenha_automato(IndiceUltimoAutomato)
		return HttpResponseRedirect(reverse('website:MostraAutomatos'))

	context = {'form': form}
	return render(request, 'website/CriarAutomato.html', context)

def EditarAutomato(request, automato_id):

	automato = Automato.objects.get(pk=automato_id)
	form = AutomatoForm(request.POST or None, instance=automato)
	if form.is_valid():
		form.save()
		IndiceUltimoAutomato = Automato.objects.all().count() - 1
		desenha_automato(IndiceUltimoAutomato)
		return HttpResponseRedirect(reverse('website:MostraAutomatos'))

	context = {'form': form, "automato_id": automato_id}
	return render(request, 'website/EditarAutomato.html', context)

def DetalhesAutomato(request, automato_id):

	context = {"automato_id": automato_id, "automato":Automato.objects.get(pk=automato_id)}
	return render(request, 'website/DetalhesAutomato.html', context)

def DetalhesMaquinaTuring(request, maquinaturing_id):

	context = {"maquinaturing_id": maquinaturing_id, "maquinaturing":MaquinaTuring.objects.get(pk=maquinaturing_id)}
	return render(request, 'website/DetalhesMaquinaTuring.html', context)

def ApagaAutomato(request, automato_id):
	automato = Automato.objects.get(pk=automato_id)
	Automato.objects.get(pk=automato_id).delete()
	path = os.getcwd()
	os.remove(path + '\\website\\static\\website\\imagens\\' + automato.Descricao + ".svg")
	os.remove(path + '\\website\\static\\website\\imagens\\' + automato.Descricao)
	return HttpResponseRedirect(reverse('website:MostraAutomatos'))

def EscolhaCriacaoAutomato(request):
	return render(request, 'website/EscolhaCriacaoAutomato.html')

def AutomatoUpload(request):
	# Build paths inside the project like this: BASE_DIR / 'subdir'.
	frase = ""
	BASE_DIR = Path(__file__).resolve().parent.parent
	if request.method =='POST':
		uploaded_file = request.FILES['AutomatoJSON']
		print(uploaded_file.name)
		print(uploaded_file.size)
		fs = FileSystemStorage()
		fs.save(uploaded_file.name, uploaded_file)
		try:
			with open(os.path.join(BASE_DIR, 'media')+"/" + uploaded_file.name, "r") as json_file:
				conteudo = json.load(json_file)
				json_file.close()
			os.remove(os.path.join(BASE_DIR, 'media')+"/" + uploaded_file.name)
			print(conteudo)
			Alfabeto = conteudo["alfabeto"]
			Estados = conteudo["estados"]
			EstadoInicial = conteudo["EstadoInicial"]
			EstadosDeAceitacao = conteudo["EstadosDeAceitacao"]
			DicionarioTransicao = conteudo["DicionarioTransicao"]
			Descricao = conteudo["Descricao"]
			print(Alfabeto)
			print(Estados)
			print(EstadoInicial)
			print(EstadosDeAceitacao)
			print(DicionarioTransicao)
			print(Descricao)
			IndiceUltimoAutomato = Automato.objects.all().count() - 1
			if IndiceUltimoAutomato >= 0:
				id = Automato.objects.all()[IndiceUltimoAutomato].id + 1
			else:
				id = 0
			novo = Automato(id, Alfabeto, Estados, EstadoInicial, EstadosDeAceitacao, DicionarioTransicao, Descricao)
			novo.save()
			IndiceUltimoAutomato = Automato.objects.all().count() - 1
			desenha_automato(IndiceUltimoAutomato)
			frase = "Autómato inserido com sucesso!"
		except:
			os.remove(os.path.join(BASE_DIR, 'media') + "/" + uploaded_file.name)
			frase = "Ocorreu um erro, por favor verifique o tipo de ficheiro e o seu conteúdo"
		uploaded_file
	context={"frase":frase}
	return render(request, 'website/AutomatoUpload.html', context)


def TestarAutomato(request, automato_id):
	automato = Automato.objects.get(pk=automato_id)
	form = ObterSequenciaForm(request.POST or None)
	Aceite = ""
	if request.method == 'POST':
		form = ObterSequenciaForm(request.POST or None)
		if form.is_valid():

			Alfabeto = automato.Alfabeto
			Estados = set(automato.Estados)
			EstadoInicial = automato.EstadoInicial
			EstadosDeAceitacao = set(automato.EstadosDeAceitacao)
			ListaDicionarioTransicao = automato.DicionarioTransicao.split()
			DicionarioTransicao = {}
			for elemento in ListaDicionarioTransicao:
				DicionarioTransicao[elemento[0], elemento[1]] = elemento[2]
			sequencia = form['Sequencia'].value()
			EstadoAtual = EstadoInicial
			try:
				for elemento in sequencia:
					EstadoAtual = DicionarioTransicao[EstadoAtual,elemento]
					print(EstadoAtual)
				if EstadoAtual in EstadosDeAceitacao:
					print("Sequência aceite\n")
					Aceite = "Sequência Aceite"
				else:
					print("Sequência Negada")
					Aceite = "Sequência Negada"
			except:
				Aceite = "Ocorreu um erro. Por favor verifique a sequência inserida. Para mais informações, verifique os detalhes deste autómato."

	else:
		form = ObterSequenciaForm()
	context = {'form': form, "automato_id": automato_id, "Aceite":Aceite}
	return render(request, 'website/TestarAutomato.html', context)

def desenha_automato(automato_id):
	automato = Automato.objects.all()[automato_id]
	print("KAJMSODLAJSDMÇ")
	class Grafico():
		def __init__(self):
			self.Alfabeto = automato.Alfabeto
			self.Estados = set(automato.Estados)
			self.EstadoInicial = automato.EstadoInicial
			self.EstadosDeAceitacao = set(automato.EstadosDeAceitacao)
			ListaDicionarioTransicao = automato.DicionarioTransicao.split()
			self.DicionarioTransicao = {}
			self.Descricao = automato.Descricao
			for elemento in ListaDicionarioTransicao:
				self.DicionarioTransicao[elemento[0], elemento[1]] = elemento[2]
			d = Digraph(name=self.Descricao)
			print("B")
			# configurações gerais
			d.graph_attr['rankdir'] = 'LR'
			d.edge_attr.update(arrowhead='vee', arrowsize='1')
			# d.edge_attr['color'] = 'blue'
			d.node_attr['shape'] = 'circle'
			# d.node_attr['color'] = 'blue'

			# Estado inicial
			d.node('Start', label='', shape='none')

			# Estados de transição
			self.estadosDeTransicao = set(self.Estados) - set(self.EstadosDeAceitacao)
			for estado in self.estadosDeTransicao:
				d.node(estado)
				print("C")

			# Estado aceitação
			for estado in self.EstadosDeAceitacao:
				d.node(estado, shape='doublecircle')
				print("D")

			# Transicoes
			d.edge('Start', self.EstadoInicial)

			for tuplo, estadoSeguinte in self.DicionarioTransicao.items():
				d.edge(tuplo[0], estadoSeguinte, label=tuplo[1])

			# print(d.source)
			d.format = 'svg'
			path = os.getcwd()
			print("OLAAAAAAAAAAAAAAAAAAAAAAA")
			d.render(path + '\\website\\static\\website\\imagens\\' + self.Descricao)

	ola = Grafico()

def CriarMaquinaTuring(request):
	form = MaquinaTuringForm(request.POST or None)
	if form.is_valid():
		form.save()
		IndiceUltimaMaquina = MaquinaTuring.objects.all().count() - 1
		desenha_MaquinaTuring(IndiceUltimaMaquina)
		return HttpResponseRedirect(reverse('website:MostraMaquinasTuring'))


	context = {'form': form}
	return render(request, 'website/CriarMaquinaTuring.html', context)

def EditarMaquinaTuring(request, maquinaturing_id):

	maquinaturing = MaquinaTuring.objects.get(pk=maquinaturing_id)
	form = MaquinaTuringForm(request.POST or None, instance=maquinaturing)
	if form.is_valid():
		form.save()
		IndiceUltimaMaquina = MaquinaTuring.objects.all().count() - 1
		desenha_MaquinaTuring(IndiceUltimaMaquina)
		return HttpResponseRedirect(reverse('website:MostraMaquinasTuring'))

	context = {'form': form, "maquinaturing_id": maquinaturing_id}
	return render(request, 'website/EditarMaquinaTuring.html', context)

def ApagaMaquinaTuring(request, maquinaturing_id):
	maquinaturing = MaquinaTuring.objects.get(pk=maquinaturing_id)
	MaquinaTuring.objects.get(pk=maquinaturing_id).delete()
	path = os.getcwd()
	os.remove(path + '\\website\\static\\website\\imagens\\MaquinasTuring\\' + maquinaturing.Descricao + ".svg")
	os.remove(path + '\\website\\static\\website\\imagens\\MaquinasTuring\\' + maquinaturing.Descricao)
	return HttpResponseRedirect(reverse('website:MostraMaquinasTuring'))

def EscolhaCriacaoMaquinaTuring(request):
	return render(request, 'website/EscolhaCriacaoMaquinaTuring.html')

def TestarMaquinaTuring(request, maquinaturing_id):
	maquinaturing = MaquinaTuring.objects.get(pk=maquinaturing_id)
	form = ObterSequenciaForm(request.POST or None)
	Resultado = ""
	if request.method == 'POST':
		form = ObterSequenciaForm(request.POST or None)
		if form.is_valid():

			Alfabeto = maquinaturing.Alfabeto
			Estados = set(maquinaturing.Estados)
			EstadoInicial = maquinaturing.EstadoInicial
			EstadosDeAceitacao = set(maquinaturing.EstadosDeAceitacao)
			ListaDicionarioTransicao = maquinaturing.DicionarioTransicao.split()
			DicionarioTransicao = {}
			for elemento in ListaDicionarioTransicao:
				DicionarioTransicao[elemento[0], elemento[1]] = [elemento[2], elemento[3], elemento[4]]
			sequencia = form['Sequencia'].value()
			EstadoAtual = EstadoInicial

			ListaSequencia = list(
				"ΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔ" + sequencia + "ΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔΔ")
			Indice = 0

			while ListaSequencia[Indice] == "Δ":
				Indice += 1
			try:
				print(ListaSequencia[Indice])
				print(Indice)
				while EstadoAtual not in EstadosDeAceitacao:
					AUX = ListaSequencia[Indice]
					ListaSequencia[Indice] = DicionarioTransicao[EstadoAtual, ListaSequencia[Indice]][1]
					print(Indice)
					print(ListaSequencia[Indice])
					if DicionarioTransicao[EstadoAtual, AUX][2] == "R":
						Indice += 1
					elif DicionarioTransicao[EstadoAtual, AUX][2] == "L":
						Indice -= 1
					EstadoAtual = DicionarioTransicao[EstadoAtual, AUX][0]
				print(ListaSequencia)
			except:
				Resultado = ("Sequencia não aceite. Sequência resultante:") + str(ListaSequencia)
			if EstadoAtual in EstadosDeAceitacao:
				for elemento in ListaSequencia:
					if elemento != "Δ":
						IndiceInicio = 0
						while ListaSequencia[IndiceInicio] == "Δ":
							IndiceInicio += 1
						StringLista = "".join([str(item) for item in ListaSequencia])
						Resultado = ("Sequencia aceite. Sequência resultante: ") + str(StringLista.split("Δ")[Indice])
						break
					else:
						Resultado = ("Sequencia aceite. Sequência resultante: ") + str(ListaSequencia)




	else:
		form = ObterSequenciaForm()
	context = {'form': form, "maquinaturing_id": maquinaturing_id, "Resultado":Resultado}
	return render(request, 'website/TestarMaquinaTuring.html', context)


def MaquinaTuringUpload(request):
	# Build paths inside the project like this: BASE_DIR / 'subdir'.
	frase = ""
	BASE_DIR = Path(__file__).resolve().parent.parent
	if request.method =='POST':
		uploaded_file = request.FILES['MaquinaTuringJson']
		print(uploaded_file.name)
		print(uploaded_file.size)
		fs = FileSystemStorage()
		fs.save(uploaded_file.name, uploaded_file)
		try:
			with open(os.path.join(BASE_DIR, 'media')+"/" + uploaded_file.name, "r") as json_file:
				conteudo = json.load(json_file)
				json_file.close()
			os.remove(os.path.join(BASE_DIR, 'media')+"/" + uploaded_file.name)
			print(conteudo)
			Alfabeto = conteudo["alfabeto"]
			Alfabeto= Alfabeto.replace("Î”", "Δ")
			Estados = conteudo["estados"]
			EstadoInicial = conteudo["EstadoInicial"]
			EstadosDeAceitacao = conteudo["EstadosDeAceitacao"]
			DicionarioTransicao = conteudo["DicionarioTransicao"]
			Descricao = conteudo["Descricao"]

			ListaDicionario = list(DicionarioTransicao)
			IndiceLista = 0
			for item in ListaDicionario:
				if item == "”":
					ListaDicionario.remove(item)
				elif item == "Î":
					ListaDicionario[IndiceLista] = "Δ"
				IndiceLista+=1
			DicionarioTransicao = "".join(ListaDicionario)
			print(f"LISTA: {ListaDicionario}")


			print(Alfabeto)
			print(Estados)
			print(EstadoInicial)
			print(EstadosDeAceitacao)
			print(DicionarioTransicao)
			print(Descricao)
			IndiceUltimaMaquina = MaquinaTuring.objects.all().count() - 1
			if IndiceUltimaMaquina >= 0:
				id = MaquinaTuring.objects.all()[IndiceUltimaMaquina].id + 1
			else:
				id = 0
			novo = MaquinaTuring(id, Alfabeto, Estados, EstadoInicial, EstadosDeAceitacao, DicionarioTransicao,
								 Descricao)
			novo.save()
			IndiceUltimaMaquina = MaquinaTuring.objects.all().count() - 1
			desenha_MaquinaTuring(IndiceUltimaMaquina)
			uploaded_file
			frase = "Máquina de turing inserida com sucesso!"
		except:
			os.remove(os.path.join(BASE_DIR, 'media') + "/" + uploaded_file.name)
			frase = "Ocorreu um erro, por favor verifique o tipo de ficheiro e o seu conteúdo"
	context={"frase":frase}
	return render(request, 'website/MaquinaTuringUpload.html', context)



def desenha_MaquinaTuring(maquinaturing_id):
	maquinaturing = MaquinaTuring.objects.all()[maquinaturing_id]
	print("KAJMSODLAJSDMÇ")
	class GraficoTuring():
		def __init__(self):
			self.Alfabeto = maquinaturing.Alfabeto
			self.Estados = set(maquinaturing.Estados)
			self.EstadoInicial = maquinaturing.EstadoInicial
			self.EstadosDeAceitacao = set(maquinaturing.EstadosDeAceitacao)
			ListaDicionarioTransicao = maquinaturing.DicionarioTransicao.split()
			self.DicionarioTransicao = {}
			self.Descricao = maquinaturing.Descricao
			for elemento in ListaDicionarioTransicao:
				self.DicionarioTransicao[elemento[0], elemento[1]] = [elemento[2], elemento[3], elemento[4]]
			d = Digraph(name=self.Descricao)
			print("B")
			# configurações gerais
			d.graph_attr['rankdir'] = 'LR'
			d.edge_attr.update(arrowhead='vee', arrowsize='1')
			# d.edge_attr['color'] = 'blue'
			d.node_attr['shape'] = 'circle'
			# d.node_attr['color'] = 'blue'

			# Estado inicial
			d.node('Start', label='', shape='none')

			# Estados de transição
			self.estadosDeTransicao = set(self.Estados) - set(self.EstadosDeAceitacao)
			for estado in self.estadosDeTransicao:
				d.node(estado)
				print("C")

			# Estado aceitação
			for estado in self.EstadosDeAceitacao:
				d.node(estado, shape='doublecircle')
				print("D")

			# Transicoes
			d.edge('Start', self.EstadoInicial)

			for tuplo, tuplo2 in self.DicionarioTransicao.items():
				d.edge(tuplo[0], tuplo2[0], label=tuplo[1] + tuplo2[1] + tuplo2[2])

			# print(d.source)
			d.format = 'svg'
			path = os.getcwd()
			print("OLAAAAAAAAAAAAAAAAAAAAAAA")
			d.render(path + '\\website\\static\\website\\imagens\\MaquinasTuring\\' + self.Descricao)

	adeus = GraficoTuring()
