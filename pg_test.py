import numpy as np

class Imagem():
	def __init__(self, dados):

		self.vertices = []
		self.faces = []

		for i in range(len(dados)):

			aux = []

			if(dados[i][0] == 'v'):
				aux.append(float(dados[i][1]))
				aux.append(float(dados[i][2]))
				aux.append(float(dados[i][3]))
				self.vertices.append(aux)
				
			if(dados[i][0] == 'f'):
				aux.append(int(dados[i][1]))
				aux.append(int(dados[i][2]))
				aux.append(int(dados[i][3]))
				self.faces.append(aux)

	def getVertices(self, x):
		return self.vertices[x]

	def getVertices(self, x, y):
		return self.vertices[x][y]
    
	def getFaces(self, x, y):
		return self.faces[x]

	def getFaces(self, x):
		return self.faces[x][y]

	def write_obj(self, obj):
		with open('{}_NOVO.obj'.format(obj), 'w') as w:

			for i in range(len(self.vertices)):                
				w.write('v {} {} {}'.format(self.vertices[i][0], self.vertices[i][1], self.vertices[i][2]))
				w.write('\n')

			for i in range(len(self.faces)):                
				w.write('f {} {} {}'.format(self.faces[i][0], self.faces[i][1], self.faces[i][2]))
				w.write('\n')

		w.close()

	def aplica_transformacao(self, matriz):

		for i in range(len(self.vertices)):

			aux = []
			aux.append(float(self.vertices[i][0]))
			aux.append(float(self.vertices[i][1]))
			aux.append(float(self.vertices[i][2]))
			aux.append(float(1))
			
			vetor = np.array(aux)
			novo_vetor = np.matmul(matriz, vetor)

			self.vertices[i][0] = novo_vetor[0]
			self.vertices[i][1] = novo_vetor[1]
			self.vertices[i][2] = novo_vetor[2]

	def escala(self, escala):

		matriz = np.array([[escala,      0,      0,    0],
				  		   [     0, escala,      0,    0],
				           [     0,      0, escala,    0],
				           [     0,      0,      0,    1]])

		self.aplica_transformacao(matriz)


def read_object(obj):
	
	data = []

	with open('{}.obj'.format(obj), 'r') as r:
		whole_file = r.read()
		lines = whole_file.split('\n')        
		for line in lines:            
			lines_fixed = line.split(' ')
			data.append(lines_fixed)
	r.close()

	data.pop(-1)

	return data


def main():

	nome_objeto = 'coarseTri.hand'
	dados = read_object(nome_objeto)
	img = Imagem(dados)

	img.escala(1/2)

	img.write_obj(nome_objeto)

if __name__ == '__main__':
	main()