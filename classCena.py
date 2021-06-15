class Cena():
  def __init__(self):
    self.objs = []
    self.vObjn =0
  
  #metodo para inserir objetos na cena
  def insereObjetos(self, objs):
    
    for i in range(0, len(objs)):
      obj = objs[i]
      
      #para todo objeto recalcula os vertices que a face está vinculada
      for j in range(0, obj.getFacesLen()):
        faceX = obj.getFaces(j,0)
        faceY = obj.getFaces(j,1)
        faceZ = obj.getFaces(j,2)
        
        obj.setFaces(j,0, faceX+self.vObjn)
        obj.setFaces(j,1, faceY+self.vObjn)
        obj.setFaces(j,2, faceZ+self.vObjn)

      self.vObjn += obj.getVerticesLen()
    self.objs.extend(objs)

  #escreve no objeto os detalhes da cena
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

  #metodos get
  def getObjeto(self, x):
    return self.objs[x]

  def getQtdObjetos(self):
    return len(self.objs)
