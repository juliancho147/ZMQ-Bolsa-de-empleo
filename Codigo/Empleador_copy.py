import zmq
from Clases import Oferta
from threading import Semaphore, Thread
import  time

# --------------------------------------------------
#   Establecimiento del pueto de conexion
# --------------------------------------------------
portPub = "5000"  # pueto para que el empleador publique su informacion
#portSub = "6000"  # puero para que el filtro pueda escuchar al empleador
# --------------------------------------------------
#   Se crea el contexto
# --------------------------------------------------
context = zmq.Context()
# --------------------------------------------------
#   Se crea el soket Publicador
# --------------------------------------------------
socketPub = context.socket(zmq.PUB)
#socketSub = context.socket(zmq.SUB)
socketPub.bind("tcp://*:{}".format(portPub))

# ------------------------------------
#     crear subscripción
# ------------------------------------


# agregar el nombre

# menu para que el empleador inserte nuevos datos
lista = []
f = open("ofertas.txt")
i = 0
titulo:str
descripcion:str
experiencia:str
estudio = []
habilidades = []
while True:
    l = f.readline()
    if i == 0 :
        titulo=l
    elif i ==  1:
        descripcion = l
    elif i == 2:
        experiencia = l
    elif i == 3:
        estudio = l
    elif i == 4:
        habilidades = l
    if not l:
        break
    if i == 4:
        i = 0
        o = Oferta(titulo, descripcion, experiencia, estudio, habilidades)
        lista.append(o)
        print(o)
    else:
        i += 1
time.sleep(1)
for i in lista:
    socketPub.send_pyobj(i)

semaforo = Semaphore(1)
class HiloFiltroSub(Thread):
    # este hilo se encarga de estar escuchando algun filtro
    # una lista de ofertas
    def __init__(self,ip,puerto,semaforo): #Constructor de la clase
         Thread.__init__(self)
         self.ip = ip
         self.puerto = puerto
         self.semaforo  = semaforo
    def enviarOfertas(self):
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://"+self.ip+":"+self.puerto)
        time.sleep(2)
        for i in lista:
            socketPub.send_pyobj(i)
    def run(self): #Metodo que se ejecutara con la llamada start
        self.semaforo.acquire()
        self.enviarOfertas()
        self.semaforo.release()
        
# HiloFiltroSub("25.8.248.34","5000",semaforo).start()   
# HiloFiltroSub("25.86.45.96","5000",semaforo).start() 