from dearpygui.core import *
from dearpygui.simple import *
from dearpygui.demo import *

from calculs import *

enable_docking(shift_only = False,dock_space=True)

add_additional_font("Fonts/Open_Sans/OpenSans-SemiBold.ttf", 20)
#add_additional_font("Fonts/Roboto/Roboto-Regular.ttf", 20)

itp,t,x,v = calcul_vitesse_piston(0.3,1000,0.5)
v = v[:itp]
x = x[:itp]
t = t[:itp]

def Recalculate_vitesse(sender,data):
    global v,t,x
    k = get_value("raideur_ressort")
    log_debug(f"Nouvelle raideur = {k}")
    m = get_value("masse_piston")
    log_debug(f"Nouvelle masse = {m}")
    l = get_value("course_piston")
    log_debug(f"Nouvelle course = {l}")
    # calculer new values
    itp,t,x,v = calcul_vitesse_piston(l*0.01,k,m)
    v = v[:itp]
    x = x[:itp]
    t = t[:itp]
    # Update plot
    add_line_series("Plot_position", "position", t, x)
    add_line_series("Plot_vitesse", "vitesse", t, v)
    _data(sender,data)

with window("Main"):
    add_button("Calculate")

with window("Configuration",width=300,height=450,x_pos=0,y_pos=0):
    add_drag_float("Raideur ressort",source ="raideur_ressort",format = "%.0f n.m-1",default_value = 1000.0,max_value = 10000,speed = 100)
    add_drag_float("Course piston",source ="course_piston",format = "%.2f cm",default_value = 30,speed = 0.1)    
    add_drag_float("Masse piston",source ="masse_piston",format = "%.3f kg",default_value = 0.3,speed = 0.01)
    add_dummy(width=50)
    add_same_line()
    add_button("RECALCULER",callback = Recalculate_vitesse,width = 150,height = 50)
    add_separator()
    add_drag_float("Diametre orifice",source ="diametre_orifice",format = "%.3f cm",default_value = 5,speed = 0.5)
    add_drag_float("Viscosite",source ="viscosite",format = "%.3f ",default_value = 0.002,speed = 0.01)

with window("Profile vitesse",width=500,height=300,x_pos=765,y_pos=0):
    with tab_bar("profiles"):
        with tab("Vitesse"):
            add_plot("Plot_vitesse",height = 200,x_axis_name = "temps",y_axis_name="vitesse")
            add_line_series("Plot_vitesse", "vitesse", t, v)
        with tab("Position"):
            add_plot("Plot_position",height = 200,x_axis_name = "temps",y_axis_name="position")
            add_line_series("Plot_position", "position", t, x)


Vmax = np.max(v)
Vmoy = vitesse_moyenne(v)
Gamma = circulation(v,t,tp=t[-1],integrale=False)
D = 0.05 #m
L = 0.0
mu = 0.002
tp = t[-1]

def _data(sender,data):
    global Vmax,Vmoy,Gamma,D,L,mu,tp
    global v,t
    Vmax = np.max(v)
    Vmoy = vitesse_moyenne(v)
    Gamma = circulation(v,t,tp=t[-1],integrale=False)
    L = get_value("course_piston")
    D = get_value("diametre_orifice")
    mu = get_value("viscosite")
    tp = t[-1]

def Update_table():
    clear_table("vitesses")
    add_row("vitesses", ["Vitesse Maximale du piston",f"{Vmax:.2f}","m/s"])
    add_row("vitesses", ["Vitesse Moyenne du piston", f"{Vmoy:.2f}","m/s"])
    add_row("vitesses", ["Circulation ", f"{Gamma:.3f}",""])
    add_row("vitesses", ["Circulation approx ", f"{Vmoy**2*t[-1]*0.5:.3f}",""])
    add_row("vitesses", ["Ratio L/D ", f"{L/D:.2f}",""])
    add_row("vitesses", ["Ratio Circulation Expected ", f"{1.18*(L/D)**0.25:.2f}",""])
    U = (Gamma/(2*np.pi*D))*(np.log((4*D)/((4*mu*tp)**0.5))-0.558)
    R = D/2
    xi = R*(np.exp(Gamma/(4*np.pi*R))/np.exp(U))
    add_row("vitesses", ["Vitesse Vortex U", f"{U:.3f}","m/s"])
    add_row("vitesses", ["Epaisseur Core xi ", f"{xi:.3f}",""])


with window("Resultats",width=760,height=300,x_pos=0,y_pos=460):
    add_text("Vitesses")
    add_table("vitesses", ["Parametre", "Valeur","unitée"])

set_render_callback(Update_table)

#show_demo()
#show_documentation()
#show_debug()
show_logger()
start_dearpygui(primary_window = "Main")