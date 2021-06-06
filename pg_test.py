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

  def getFacesLen(self):
    return len(self.faces)

  def getVerticesLen(self):
    return len(self.vertices)

  def getFacesLen(self):
    return len(self.faces)

  def setFaces(self, x, y, value):
    self.faces[x][y] = value

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

  def escala(self, escalaX, escalaY, escalaZ):

    matriz = np.array([[escalaX,      0,      0,    0],
				  		         [     0, escalaY,      0,    0],
				               [     0,      0, escalaZ,    0],
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

class scene():
  def __init__(self):
    self.objs = []
    self.vObjn =0

  def insereObjetos(self, objs):
    
    for i in range(0, len(objs)):
      obj = objs[i]
      
      for j in range(0, obj.getFacesLen()):
        faceX = obj.getFaces(j,0)
        faceY = obj.getFaces(j,1)
        faceZ = obj.getFaces(j,2)
        
        obj.setFaces(j,0, faceX+self.vObjn)
        obj.setFaces(j,1, faceY+self.vObjn)
        obj.setFaces(j,2, faceZ+self.vObjn)

      self.vObjn += obj.getVerticesLen()
    self.objs.extend(objs)

  def writeScene(self, name):
    with open('{}_NOVO.obj'.format(name), 'w') as w:
      for obj in self.objs:    

        for i in range(obj.getVerticesLen()):                
          w.write('v {} {} {}'.format(obj.getVertices(i, 0), obj.getVertices(i, 1), obj.getVertices(i, 2)))
          w.write('\n')

        for i in range(obj.getFacesLen()):                
          w.write('f {} {} {}'.format(obj.getFaces(i, 0), obj.getFaces(i, 1), obj.getFaces(i, 2)))
          w.write('\n')
    w.close()

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

  nome_objeto = 'coarseTri.cube'
  mao = read_object(nome_objeto)
  botijo = read_object('coarseTri.botijo')

  img = Imagem(mao)
  img2 = Imagem(botijo)
  img3 = Imagem(mao)
  transformacoesImg = [img.escala(2000, 0.2, 2000), img.translacao(-0.5,0,-0.5)]#chao 10X10
  transformacoesImg2 = [img3.translacao(0,2,0)]#botijo encima do chao
  
  img.aplica_transformacao(transformacoesImg)
  #img2.aplica_transformacao(transformacoesImg2)

  cena = scene() 
  cena.insereObjetos([img, img2])
  cena.writeScene("cena_Maos") 

if __name__ == '__main__':
  main()