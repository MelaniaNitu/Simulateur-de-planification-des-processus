#ici on a implementer les strategies utilisees par le simulateur du CPU 

#Une strategie prend le processus en cours d'execution (s'il existe un),
#le temps courant de la CPU, et sa file d'attente, et retourne quel processus
#de la CPU devrait fonctionner suivant




slist = dict()


#Shortest Job First, Non-Preemptive (SJFNP)
def sjfnp_run(current_process, current_time, queue):
    if current_process == None:
        if len(queue) > 0:
            shortest = queue[0]
            for process in queue:
                if process['length'] < shortest['length']:
                    shortest = process
            queue.remove(shortest)
            return shortest
    
    return current_process

slist['SJFNP'] = sjfnp_run


#Round Robin (RR)
max_steps = 3
def rr_run(current_process, current_time, queue):
    if current_process == None or (current_process['steps'] == max_steps):
        if current_process != None:
            current_process['steps'] = 0
            queue.append(current_process)
        if len(queue) > 0:
            current_process = queue.pop(0)
    
    if current_process != None:
        current_process['steps'] += 1
    
    return current_process

slist['RR'] = rr_run

