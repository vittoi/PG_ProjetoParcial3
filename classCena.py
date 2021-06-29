class Cena():
  def __init__(self, luz):
    self.objs = []
    self.vetor_luz = luz
    self.vObjn =0
  
  #metodo para inserir objetos na cena
  def insereObjetos(self, objs):
    self.objs.extend(objs)

  #escreve no objeto os detalhes da cena
  def writeScene(self, name):
    self.vObjn = 0 

    with open('{}_FINAL.obj'.format(name), 'w') as w:
      for obj in self.objs:    

        for i in range(obj.getVerticesLen()):                
          w.write('v {} {} {}'.format(obj.getVertices(i, 0), obj.getVertices(i, 1), obj.getVertices(i, 2)))
          w.write('\n')

        for i in range(obj.getFacesLen()):                
          w.write('f {} {} {}'.format(obj.getFaces(i, 0) + self.vObjn, obj.getFaces(i, 1) + self.vObjn, obj.getFaces(i, 2) + self.vObjn))
          w.write('\n')

        self.vObjn += obj.getVerticesLen()

    w.close()

  #metodos get
  def getObjeto(self, x):
    return self.objs[x]
 
  def getTodosObjetos(self):
    return self.objs

  def getQtdObjetos(self):
    return len(self.objs)
    
    #Funcao para normalizar os vertices
  def normaliza(self):

    menorX = 0
    maiorX = 0
    menorY = 0
    maiorY = 0
    menorZ = 0
    maiorZ = 0

    for j in range(self.getQtdObjetos()):

      img = self.getObjeto(j)

      for i in range(0, img.getQtdVertices()):
      
        aux = []
        
        if(float(img.getVertices(i,0) < menorX)):
          menorX = float(img.getVertices(i,0))

        if(float(img.getVertices(i,0) > maiorX)):
          maiorX = float(img.getVertices(i,0))

        if(float(img.getVertices(i,1) < menorY)):
          menorY = float(img.getVertices(i,1))

        if(float(img.getVertices(i,1) > maiorY)):
          maiorY = float(img.getVertices(i,1))

        if(float(img.getVertices(i,2) < menorZ)):
          menorZ = float(img.getVertices(i,2))

        if(float(img.getVertices(i,2) > maiorZ)):
          maiorZ = float(img.getVertices(i,2))

    #calcula a media dos vertices
    mediaX = (menorX + maiorX)/2
    mediaY = (menorY + maiorY)/2
    mediaZ = (menorZ + maiorZ)/2

    #Calcula a distancia entre o menor e o maior ponto de cada orientacao
    distanciaX = (abs(menorX) + abs(maiorX))
    distanciaY  = (abs(menorY) + abs(maiorY))
    distanciaZ  = (abs(menorZ)+ abs(maiorZ))

    distanciaMax = max(distanciaX, distanciaY, distanciaZ)

    #Aplica a transformacao final para deixar os vertices entre -1 e 1
    for j in range(self.getQtdObjetos()):
      img = self.getObjeto(j)
      img.aplica_transformacao([img.escala(2/distanciaMax, 2/distanciaMax, 2/distanciaMax), img.translacao(-mediaX, -mediaY, -mediaZ)])
