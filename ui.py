#Interface graphique

import wx
from wx.lib.agw import ultimatelistctrl as ulc

SIDEBAR_GROUPS_BORDER = 6
SIDEBAR_ROWS_BORDER = 4
TIMES_BORDER = 4


#fonction d'utilite pour realiser un panneau avec un calibreur predefini, pour aider a layouting
def make_layout_panel(parent, direction=wx.HORIZONTAL, *args, **kwargs):
    panel = wx.Panel(parent, *args, **kwargs)
    panel.SetSizer(wx.BoxSizer(direction))
    return panel

#une valeur que tu peux changer et recuperer,avec une "label" indiquant qu'est-ce que c'est
class LabeledValue(wx.Panel):
    def __init__(self, parent, label="", value="", label_font=None, value_font=None):
        wx.Panel.__init__(self, parent)
        
        self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        
        self.label = wx.StaticText(self) 
        self.Sizer.Add(self.label)
        
        self.value = wx.StaticText(self) 
        self.Sizer.Add(self.value)
        
        self.set_label(label)
        self.set_value(value)
        
        if label_font != None: self.label.SetFont(label_font)
        if value_font != None: self.value.SetFont(value_font)
    
    def get_label(self):
        return self._label
    
    def set_label(self, label):
        self._label = label
        self.label.SetLabel(self._label + ": ")
        self.GetParent().Layout()
    
    def get_value(self):
        return self._value
    
    def set_value(self, value):
        self._value = value
        self.value.SetLabel(str(self._value))
        self.GetParent().Layout()



class MainWindow(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY):
        wx.Frame.__init__(self, parent=parent, id=id, title="Simulateur de planification des processus", size=(770,400))
        self.Centre()
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))
        
        
        #les 'fonts' doivent etre definies apres le demarrage de l'application,donc ils sont ici, au lieu de la configuration en haut

        LABEL_FONT = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        VALUE_FONT = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        main_panel = make_layout_panel(self, wx.HORIZONTAL)
        self.Sizer.Add(main_panel, 1, wx.EXPAND)


        #Barre laterale
        #======================
        sidebar_panel = make_layout_panel(main_panel, wx.VERTICAL, style=wx.BORDER_SIMPLE)
        main_panel.Sizer.Add(sidebar_panel, 0, wx.EXPAND)
        
        
        #Configurer les commandes
        #Setup controls
        #===========
        setup_group = wx.StaticBox(sidebar_panel, label="Preparation")
        setup_group.static_sizer = wx.StaticBoxSizer(setup_group, wx.VERTICAL)
        sidebar_panel.Sizer.Add(setup_group.static_sizer, 0, wx.EXPAND|wx.ALL, SIDEBAR_GROUPS_BORDER)
        
        
        nr_processes_panel = make_layout_panel(sidebar_panel, wx.HORIZONTAL)
        setup_group.static_sizer.Add(nr_processes_panel, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, SIDEBAR_ROWS_BORDER)
        
        nr_processes_label = wx.StaticText(nr_processes_panel, label="Nombre de processus: ") 
        nr_processes_panel.Sizer.Add(nr_processes_label, 1, wx.ALIGN_CENTER_VERTICAL)
        
        nr_processes_input = wx.SpinCtrl(nr_processes_panel, min=2, initial=10, value='10', size=(60,22))
        nr_processes_panel.Sizer.Add(nr_processes_input, 0, wx.EXPAND)
        
        
        generate_button = wx.Button(sidebar_panel, label="Generer")
        setup_group.static_sizer.Add(generate_button, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, SIDEBAR_ROWS_BORDER)
        #===========
        
        
        #Simulation controls
        #===========
        simulation_group = wx.StaticBox(sidebar_panel, label="Simuler")
        simulation_group.static_sizer = wx.StaticBoxSizer(simulation_group, wx.VERTICAL)
        sidebar_panel.Sizer.Add(simulation_group.static_sizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, SIDEBAR_GROUPS_BORDER)
        
        
        strategy_panel = make_layout_panel(sidebar_panel, wx.HORIZONTAL)
        simulation_group.static_sizer.Add(strategy_panel, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, SIDEBAR_ROWS_BORDER)
        
        strategy_label = wx.StaticText(strategy_panel, label="Strategie: ") 
        strategy_panel.Sizer.Add(strategy_label, 1, wx.ALIGN_CENTER_VERTICAL)
        
        strategy_selector = wx.Choice(strategy_panel)
        strategy_panel.Sizer.Add(strategy_selector, 0, wx.EXPAND)
        
        
        speed_panel = make_layout_panel(sidebar_panel, wx.HORIZONTAL)
        simulation_group.static_sizer.Add(speed_panel, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, SIDEBAR_ROWS_BORDER)
        
        speed_label = wx.StaticText(speed_panel, label="Vitesse de simulation: ") 
        speed_panel.Sizer.Add(speed_label, 1, wx.ALIGN_CENTER_VERTICAL)
        
        speed_input = wx.SpinCtrl(speed_panel, min=1, initial=5, value='5', size=(60,22))
        speed_panel.Sizer.Add(speed_input, 0, wx.EXPAND)
        
        
        run_pause_button = wx.Button(sidebar_panel, label="Execution")
        run_pause_button.Enable(False)
        simulation_group.static_sizer.Add(run_pause_button, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, SIDEBAR_ROWS_BORDER)
        #===========
        #======================

        
        #table des processus
        process_table = ulc.UltimateListCtrl(main_panel, agwStyle=ulc.ULC_REPORT|ulc.ULC_HAS_VARIABLE_ROW_HEIGHT|ulc.ULC_BORDER_SELECT)
        process_table.Enable(False)
        process_table.InsertColumn(0, "Nom du processus",width=110)
        process_table.InsertColumn(1, "Temps d'arrivee",width=100)
        process_table.InsertColumn(2, "Longueur",width=60)
        process_table.InsertColumn(3, "Progres", width=130)
        process_table.InsertColumn(4, "Restant",width=60)
        process_table.InsertColumn(5, "Attendu")
        main_panel.Sizer.Add(process_table, 1, wx.EXPAND)


        #Barre de temps
        #===========
        times_panel = make_layout_panel(self, wx.HORIZONTAL, style=wx.BORDER_SIMPLE, size=(-1,30))
        self.Sizer.Add(times_panel, 0, wx.EXPAND)
        
        average_wait_value = LabeledValue(times_panel, label="Temps moyen d'attente", label_font=LABEL_FONT, value_font=VALUE_FONT)
        average_wait_value.value.SetFont(VALUE_FONT)
        average_wait_value.Hide()
        times_panel.Sizer.Add(average_wait_value, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, TIMES_BORDER)
        
        times_panel.Sizer.AddSpacer(6)
        
        average_run_value = LabeledValue(times_panel, label="Temps moyen d'execution", label_font=LABEL_FONT, value_font=VALUE_FONT)
        average_run_value.Hide()
        times_panel.Sizer.Add(average_run_value, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, TIMES_BORDER)
        #===========
        
        
        #on fait accessible les variables qu'on a besoin
        self.times_panel = times_panel
        self.process_table = process_table
        
        self.average_wait_value = average_wait_value
        self.average_run_value = average_run_value
        
        self.nr_processes_input = nr_processes_input
        self.strategy_selector = strategy_selector
        self.speed_input = speed_input
        
        self.generate_button = generate_button
        self.run_pause_button = run_pause_button
    
    
    def add_processes(self, processes):
        self.process_table.DeleteAllItems()
        
        for process in processes:
            pos = self.process_table.InsertStringItem(process['id'], "P%d" % (process['id']+1))
            self.process_table.SetStringItem(pos, 1, str(process['start_time']))
            self.process_table.SetStringItem(pos, 2, str(process['length']))
            
            gauge = wx.Gauge(self.process_table, range = process['length'])
            gauge.SetValue(process['done'])
            gauge.SetSize(wx.Size(process['length'] * 10, -1))
            self.process_table.SetItemWindow(pos, 3, wnd=gauge, expand=False)
            
            self.process_table.SetStringItem(pos, 4, str(process['length'] - process['done']))
            self.process_table.SetStringItem(pos, 5, str(process['waited']))


    def update_processes(self, processes):
        for process in processes:
            self.process_table.Select(process['id'], process['queued'])
            
            gauge = self.process_table.GetItemWindow(process['id'], 3)
            gauge.SetValue(process['done'])
            
            self.process_table.SetStringItem(process['id'], 4, str(process['length'] - process['done']))
            self.process_table.SetStringItem(process['id'], 5, str(process['waited']))



#on teste le code
if __name__ == '__main__':
    app = wx.App()
    window = MainWindow()
    window.Show()
    app.MainLoop()

