#Tout d'abord,on connecte l'interface a la classe de simulation CPU


import ui
import proc
import strategies
import wx


class Main:
    def __init__(self):
        app = wx.App()
        self.window = ui.MainWindow()
        self.window.Show()
        
        #on ajuoute les strategies crees au selecteur (chooser)
        
        for strategy_name in strategies.slist:
            self.window.strategy_selector.Append(strategy_name)
        self.window.strategy_selector.SetSelection(0)   #le selecteur commence comme void,donc on pre-select la premiere option
        
        self.window.Bind(wx.EVT_BUTTON, self.generate_procs, self.window.generate_button)        
        self.window.Bind(wx.EVT_BUTTON, self.run_pause, self.window.run_pause_button)
        
        self.cpu = None
        self.processes = []
        
        app.MainLoop()

        #quand notre application est preparee pour terminer (la boucle principale s'arrete), on s'assure qu'on arrete le CPU thread (s'il y en a un en train d'execution)
       
        if self.cpu != None and self.cpu.running:
            self.cpu.running = False
    
    
    def generate_procs(self, event):
        nr_processes = self.window.nr_processes_input.GetValue()
        self.processes = proc.generate_processes(nr_processes)
        
        self.window.add_processes(self.processes)
        self.window.run_pause_button.Enable(True)
    
    
    def run_pause(self, event):
        if self.cpu != None and self.cpu.running:   #s'il y a une simulation en progres (en train d'execution)

            #self.cpu.should_continue est un threading.Event,utilisee to interrompre le thread de CPU

                      
            if self.cpu.should_continue.is_set():  #quand il est sette,le thread continue uninterrompu,sinon il attend (voir proc->CPU->run() pour se rendre compte comment il est utilise)
                self.cpu.should_continue.clear()   #interrompre le thread de CPU
                self.window.run_pause_button.SetLabel("Resume")
                self.window.speed_input.Enable(True)  # quand on interrompre (pause) le programe,on peut changer la vitesse
            else:
                self.cpu.speed = self.window.speed_input.GetValue()
                self.cpu.should_continue.set()   #on reprend (resume) le thread de CPU
                self.window.run_pause_button.SetLabel("Pause")
                self.window.speed_input.Enable(False)
        else:  #si le programme ne fonctionne pas/on a choisi de le mettre en pause->on commence une nouvelle simulation           
            if len(self.processes) > 0:
                self.reset_values()
                
                strategy_name = self.window.strategy_selector.GetStringSelection()
                speed = self.window.speed_input.GetValue()
                
                self.cpu = proc.CPU(self.processes, strategies.slist[strategy_name], speed, self.cpu_listener)
                self.cpu.start()
                
                self.window.run_pause_button.SetLabel("Pause")

                # on desactive les boutons ,pour que l'utilisateur ne puisse pas changer les donnees de la simulation et alterer le fonctionnement(numero des processus etc..)
                
                self.window.generate_button.Enable(False)
                self.window.nr_processes_input.Enable(False)
                self.window.speed_input.Enable(False)
                self.window.strategy_selector.Enable(False)
    
    
    def reset_values(self):
        self.window.average_wait_value.Hide()
        self.window.average_run_value.Hide()
        
        for process in self.processes:
            proc.reset_process(process)
        self.window.update_processes(self.processes)
    
    
    def cpu_listener(self, cpu):
        wx.CallAfter(self.window_updater, cpu) #on a besoin de cela pour mettre a jour l'interface de l'autre thread
    
    
    def window_updater(self, cpu):
        self.cpu.should_continue.clear() #arrete temporairement,pour que les valeurs ne changent pas pendant la mise a jour de l'interface
        self.window.update_processes(self.processes)
        self.cpu.should_continue.set()

        #s'il a fini,on va calculer les temps
        
        if self.cpu.running == False:
            total_wait = 0
            total_run = 0
            for process in self.processes:
                total_wait += process['waited']
                total_run += process['waited'] + process['length']
            
            self.window.average_wait_value.set_value(total_wait/len(self.processes))
            self.window.average_run_value.set_value(total_run/len(self.processes))
            self.window.average_wait_value.Show()
            self.window.average_run_value.Show()
            self.window.times_panel.Layout()
            
            self.window.run_pause_button.SetLabel("Run")
            self.window.generate_button.Enable(True)
            self.window.nr_processes_input.Enable(True)
            self.window.speed_input.Enable(True)
            self.window.strategy_selector.Enable(True)



if __name__=='__main__':
    main = Main()
