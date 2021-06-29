
import classCena as Cena
import classImagem as Imagem
import classCamera as Camera
import classCanvas as Canvas
import wx
from wx import *

#le o arquivo obj
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

#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
  
def main():

  #Le o arquivo .obj e o armazena suas informacoes em uma matriz
  #Atribui a matriz recebida a uma imagem, que armazenara os dados sobre vertices e faces da imagem
  botijo = Imagem.Imagem(read_object('coarseTri.botijo'))
  mao = Imagem.Imagem(read_object('coarseTri.hand'))

  #inicializa um vetor para a luz
  luz = [-1, -1, -2]

  #inicializa uma cena
  cena = Cena.Cena(luz) 

  #Coloca quantas imagens for necessario na cena 
  cena.insereObjetos([botijo, mao])

  #Exemplo de algumas transformacoes possiveis da imagem
  botijo.aplica_transformacao([botijo.translacao(-1, 0, 3), botijo.rotacaoY(30)])
  mao.aplica_transformacao([mao.escala(2, 2, 2), mao.rotacaoY(90)])

  #retorna a cena em um arquivo de saida
  cena.writeScene("Cena_mao_vaso") 

  #Define os atributos da camera
  e_camera = [1.5 , 0.75 , 1.5]
  g_camera = [0, 0, 0]
  t_camera = [0 , 0 , 1]

  #Cria a cena da camera de acordo com os parametros passados
  camera = Camera.Camera(e_camera, g_camera, t_camera)

  # Coloca a cena criada anteriormente nas coordenadas da camera, aplica a projeçao e normaliza a imagem
  # Durante essa etapa aplicamos quase todos os passos da entrega 4
  camera.posiciona_imagem(cena, 1, 10, 1, 80)

  #Aplica a rasterizacao e exibe a cena em uma tela virtual, agora com luz :)
  #Foi utilizado o algoritmo de Gouraud para a iluminação
  #Como estamos trabalhando com figuras complesxas, a imagem possui alguns "buracos" 

  #PS. também pode aparecer uma mensagem de divisao por zero, mas ela não ira afetar o codigo

  app = wx.App(0)
  frame = wx.Frame(None, -1, 'Teste')
  canvas = Canvas.Canvas(frame, cena)
  frame.Show()
  app.MainLoop()

if __name__ == '__main__':
  main()
