import numpy as np
from numpy import linalg as LA

class Camera():
    def init(self, e, g):

        self.e = e #posicao da camera
        self.g = g #ponto observado

        self.t = [34, 1, 21]

        self.n = [g[0] - e[0], g[1] - e[1], g[2] - e[2]] #vetor normal ao plano de projecao
        norm = LA.norm(self.n)               # n = (g - e) / ( |g - e| )
        self.n = self.n/norm

        self.u = np.cross(self.t, self.n)
        norm = LA.norm(self.u)               # n = (t X n) / ( |t X n| )
        self.u = self.n/norm

        self.v = np.cross(self.n, self.u)

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
    
  def getFaces(self, x):
    return self.faces[x]

  def getFaces(self, x, y):
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

    transformacao = matriz[0]

    for i in range(1, len(matriz)):
      transformacao = np.matmul(transformacao, matriz[i])

    for i in range(len(self.vertices)):

      aux = []
      aux.append(float(self.vertices[i][0]))
      aux.append(float(self.vertices[i][1]))
      aux.append(float(self.vertices[i][2]))
      aux.append(float(1))
      
      vetor = np.array(aux)
      novo_vetor = np.matmul(transformacao, vetor)

      self.vertices[i][0] = novo_vetor[0]
      self.vertices[i][1] = novo_vetor[1]
      self.vertices[i][2] = novo_vetor[2]

  def escala(self, escala):

    matriz = np.array([[escala,      0,      0,    0],
                       [     0, escala,      0,    0],
                       [     0,      0, escala,    0],
                       [     0,      0,      0,    1]])

    return matriz

  def translacao(self, dx, dy, dz):

    matriz = np.array([[     1,      0,      0,   dx],
                       [     0,      1,      0,   dy],
                       [     0,      0,      1,   dz],
                       [     0,      0,      0,    1]])

    return matriz
  
  def rotacaoZ(self, angulo):
    rad = np.pi * (angulo/180)
    matriz = np.array([[np.cos(rad), -np.sin(rad),           0,       0],
                       [np.sin(rad),  np.cos(rad),           0,       0],
                       [          0,            0,           1,       0],
                       [          0,            0,           0,       1]])

    return matriz

  def rotacaoX(self, angulo):

    rad = np.pi * (angulo/180)

    matriz = np.array([[           1,            0,            0,       0],
                       [           0,  np.cos(rad), -np.sin(rad),       0],
                       [           0,  np.sin(rad),  np.cos(rad),       0],
                       [           0,            0,            0,       1]])

    return matriz
    
  def rotacaoY(self, angulo):

    rad = np.pi * (angulo/180)

    matriz = np.array([[  np.cos(rad),           0,  np.sin(rad),       0],
                       [            0,           1,            0,       0],
                       [ -np.sin(rad),           0,  np.cos(rad),       0],
                       [            0,           0,            0,       1]])

    return matriz

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
  transformacoes = [img.escala(2), img.rotacaoX(180), img.rotacaoY(180), img.translacao(-200,20,400)]
  
  img.aplica_transformacao(transformacoes)
  
  img.write_obj(nome_objeto) 

if __name__ == '__main__':
  main()