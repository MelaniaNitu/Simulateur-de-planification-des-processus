#on definit la classe de simulation CPU et des fonctions pour faire les processus pour elle


import threading
import time
import random


class CPU(threading.Thread):
    def __init__(self, processes, strategy, speed=1, listener=None):
        threading.Thread.__init__(self)
        
        self.procs_to_run = list(processes)  #on fait une copie de la liste,parce qu'on va la changer
        self.speed = speed                   
        self.strategy = strategy
        self.listener = listener
        self.should_continue = threading.Event()  #utilisee pour pouvoir interrompre le thread
    
    
    def run(self):
        self.running = True
        self.time = 0
        self.queue = []
        self.current_process = None
        self.should_continue.set()  # commoncer dans l'etat d'execution/non-interrompu
        
        while self.running:
            self.should_continue.wait()  #va s'arreter quand should_continue est clair (False),quand il est sette (True) va continuer
            self.run_step()                  
            time.sleep(1/float(self.speed))
    
    
    def run_step(self):
        
        #si le processus precedent est termine, on se prepare e choisir un nouveau
        if self.current_process != None and self.current_process['done'] == self.current_process['length']:
                self.current_process = None
        
        #processus arrivees dans file d'attente         
        to_remove = []   #utilise pour effacer les processus de la liste d'execution,sans casser la boucle for
        for process in self.procs_to_run:
            if process['start_time'] <= self.time:
                self.queue.append(process)
                to_remove.append(process)
        for process in to_remove:
            self.procs_to_run.remove(process)

        #on marque les processus comme etant dans la file d'attente pour l'interface graphique
        
        for process in self.queue:
            process['queued'] = True

        #Consulter la strategie choisie pour le processus qu'on veut executer
          
        self.current_process = self.strategy(self.current_process, self.time, self.queue)
        
        #executer une etape dans le processus choisi (s'il y en a un)
       
        if self.current_process != None:
            self.current_process['queued'] = False
            self.current_process['done'] += 1

        #et incrementer le temps d'attente pour les processus qui sont dans la file d'attente.
        
        for process in self.queue:
            process['waited'] += 1
        
        self.time += 1

        #arreter l'execution si on n'a rien a faire de plus
        
        if (self.current_process == None or self.current_process['done'] == self.current_process['length']) and len(self.queue) == 0 and len(self.procs_to_run) == 0:
            self.running = False
        
        #informer le "listener" (s'il y en a un) qu'on a execute une etape
       
        if self.listener != None:
            self.listener(self)



def make_process(start_time, length):
    process = dict()
    process['start_time'] = start_time
    process['length'] = length
    reset_process(process)
    return process


def reset_process(process):
    process['done'] = 0
    process['waited'] = 0
    process['queued'] = False
    process['steps'] = 0


def generate_processes(nr, max_start=10, max_length=10):
    processes = []
    random.seed()

    #creer les processus avec les temps initiels et les longueurs aleatoires (random)

    for i in range(nr):
        start_time = random.randint(0, max_start)
        length = random.randint(1, max_length)
        processes.append(make_process(start_time, length))

    #assurer au moins une processus qui commence a 0,donc on n'attend pas inutilement
    
    proc = random.choice(processes)
    proc['start_time'] = 0

    # trier la liste,en fonction de la longueur et puis en fonction du temps initial
   
    processes = sorted(processes, key=lambda k: k['length'])
    processes = sorted(processes, key=lambda k: k['start_time'])

    #on attribue aux processus des identites(id),basees sur leur index 
   
    for i, process in enumerate(processes):
        process['id'] = i
    
    return processes



#on va teste le code
if __name__ == '__main__':
    import strategies
    
    processes = generate_processes(4)
    print("Processes:")
    for process in processes:
        print("id: %d, start_time: %d, length: %d" % (process['id'], process['start_time'], process['length']))
    
    print("")
    
    def test_listener(cpu):
        print("Time: %d" % cpu.time)
        print("Queue: %s" % [process['id'] for process in cpu.queue])
        if cpu.current_process != None:
            print("Current process: id: %d, length: %d, done: %d" % (cpu.current_process['id'], cpu.current_process['length'], cpu.current_process['done']))
        else:
            print("Current process: None")
        print("")
    
    cpu = CPU(processes, strategies.slist['SJFNP'], 1, test_listener)
    cpu.start()
    cpu.join()
