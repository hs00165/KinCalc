from tkinter import * 
import matplotlib
from matplotlib.figure import Figure 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import math
  
# plot function is created for  
# plotting the graph in  
# tkinter window 



energy_saved = [[]]
energy_saved.clear()


def quit():
        root.destroy()


def Qvalue(Beam, Target, Ejectile, Recoil, Ex):

	MassTable = open("masstable.txt", "r")

	line_incriment = 0

	line1 = MassTable.readlines()
	for text in line1:

		if line_incriment > 38:

			MassExcessFlag = False
			content_index_Str = 0
			content_index_Flo = 0
			content_index = 0

			for content in text.split():
				try:
					num = float(content)

					content_index_Flo+=1
					content_index+=1

					if MassExcessFlag:

			    			MassExcess = num
			    			MassExcessFlag = False

				except:
					if content_index_Str == 0:

			    			mass = int(prev_float)
			    			Element = content
			    			MassExcessFlag = True

					content_index_Str+=1
					content_index+=1

				prev_float = num
			
			if str(mass) + Element == Beam:
		    		massB = mass
		    		ElemetB = Element
		    		MassExcessB = MassExcess

			if str(mass) + Element == Target:
		    		massT = mass
		    		ElemetT = Element
		    		MassExcessT = MassExcess

			if str(mass) + Element == Ejectile:
		    		massE = mass
		    		ElemetE = Element
		    		MassExcessE = MassExcess

			if str(mass) + Element == Recoil:
		    		massR = mass
		    		ElemetR = Element
		    		MassExcessR = MassExcess

		line_incriment+=1 
	q_value = ((MassExcessB + MassExcessT - MassExcessR - MassExcessE) / 1000.0)

	return q_value - float(Ex)







def GetMass(Particle):

	MassTable = open("masstable.txt", "r")

	line_incriment = 0

	line1 = MassTable.readlines()
	for text in line1:

		if line_incriment > 38:

			MassExcessFlag = False
			content_index_Str = 0
			content_index_Flo = 0
			content_index = 0

			for content in text.split():
				try:
					num = float(content)

					content_index_Flo+=1
					content_index+=1

					if MassExcessFlag:

			    			MassExcess = num
			    			MassExcessFlag = False

				except:
					if content_index_Str == 0:

			    			mass = int(prev_float)

			    			Element = content
			    			MassExcessFlag = True

					content_index_Str+=1
					content_index+=1

				prev_float = num
			
			if str(mass) + Element == Particle:
		    		massB = mass
		    		ElemetB = Element
		    		MassExcessB = MassExcess

		line_incriment+=1 


	return ((MassExcessB/1000)/931.5)+massB







def cond(Angle, M1, M2, M3, M4, Q):
	
	Psi = float(Angle)*(3.14159/180.0)

	T1 = float(ent_factor.get())

	Et = T1 + M1 + M2
	P1 = math.sqrt((T1**2) + (2*M1*T1))
	A = (2*M2*T1) + (2*M1*M3) + (2*M2*M3) + (2*Q*(M1+M2-M3)) - (Q**2)
	B = (Et**2) - ((P1**2)*(math.cos(Psi)**2))


	return ((A**2) - (4*(M3**2)*B))








def energy_calc(Angle, M1, M2, M3, M4, Q):

	Psi = float(Angle)*(3.14159/180.0)
	T1 = float(ent_factor.get())

	Eth = abs(Q)*( ((M1+M2)/M2) + (abs(Q)/(2*M2)) )

	Et = T1 + M1 + M2
	P1 = math.sqrt((T1**2) + (2*M1*T1))
	A = (2*M2*T1) + (2*M1*M3) + (2*M2*M3) + (2*Q*(M1+M2-M3)) - (Q**2)
	B = (Et**2) - ((P1**2)*(math.cos(Psi)**2))

	Et = T1 + M1 + M2

	T3 = (1/(2*B))*( (Et*A) + (P1*math.cos(Psi)*math.sqrt((A**2) - (4*(M3**2)*B))) ) - M3

	print(M1)

	return T3


def plot(): 

    # list of squares 
    angle = [] 
    energy = []
    Ex_energy = 0

    global energy_saved


    if len(ent_Ex.get()) != 0:
    	Ex_energy = float(ent_Ex.get())
    	
    m1 = float(GetMass(ent_M1.get()))*931.5
    m2 = float(GetMass(ent_M2.get()))*931.5
    m3 = float(GetMass(ent_M3.get()))*931.5
    m4 = float(GetMass(ent_M4.get()))*931.5
    Q = Qvalue(ent_M1.get(),ent_M2.get(),ent_M3.get(),ent_M4.get(),Ex_energy )


    for i in range(180):
        if cond(i, m1, m2, m3, m4, Q) > 0:
            energy.append(energy_calc(i, m1, m2, m3, m4, Q))
            angle.append(i)

        else:
            break

    # plotting the graph 
    plot1.plot(angle, energy) 
    fig.canvas.draw()

    energy_saved.append(energy)

  

def clearPlots():
	global energy_saved

	plot1.cla()
	plot1.minorticks_on()
	#plot1.grid()

	plt.tick_params(axis='both', which='both', direction='in')
	plt.title('Light ejectile kinematics', fontname='times new roman')
	plt.xlabel('Angle [Degrees]', fontname='times new roman')
	plt.ylabel('Energy [MeV]', fontname='times new roman')
	fig.canvas.draw()

	energy_saved.clear()




def PrintToFile():
	global energy_saved


	f = open("saved_kin_file.dat", "w")
















# the main Tkinter window 
window = Tk() 
  
# setting the title  
window.title('ReKiC: Relativistic Kinematics Calculator') 
  
# dimensions of the main window 
window.geometry("900x600") 


frame_a = Frame(
	master=window, 
	relief=RAISED, 
	borderwidth=5,
	width=300,
	height=600,
)

frame_b = Frame(
	master=window, 
	relief=RAISED, 
	borderwidth=5,
	width=800,
	height=600,
)

subframe_a = Frame(
	master=frame_a, 
	relief=SUNKEN, 
	borderwidth=5,
	width=300,
	height=60,
)

subframe_a.rowconfigure(0, minsize=30, weight=1)
subframe_a.columnconfigure([0, 1], minsize=50, weight=1)




  
# button that displays the plot 
plot_button = Button(master = frame_a,  
                     command = plot, 
                     height = 2,  
                     width = 10, 
                     text = "Plot") 

delete_button = Button(master = frame_a,  
                     command = clearPlots, 
                     height = 2,  
                     width = 10, 
                     text = "Clear") 

quit_button = Button(master = frame_a,  
                     command = window.quit, 
                     height = 2,  
                     width = 10, 
                     text = "Quit") 



lbl_Benergy = Label(
	master=subframe_a,
	text="E Beam",
)
lbl_Benergy.grid(row=0, column=0)
ent_factor = Entry(
	master=subframe_a,
	width=6,
)
ent_factor.grid(row=0, column=1)


lbl_M1 = Label(
	master=subframe_a,
	text="Beam",
)
lbl_M1.grid(row=1, column=0)
ent_M1 = Entry(
	master=subframe_a,
	width=4,
)
ent_M1.grid(row=1, column=1)

lbl_M2 = Label(
	master=subframe_a,
	text="Target",
)
lbl_M2.grid(row=2, column=0)
ent_M2 = Entry(
	master=subframe_a,
	width=4,
)
ent_M2.grid(row=2, column=1)

lbl_M3 = Label(
	master=subframe_a,
	text="Eject",
)
lbl_M3.grid(row=3, column=0)
ent_M3 = Entry(
	master=subframe_a,
	width=4,
)
ent_M3.grid(row=3, column=1)

lbl_M4 = Label(
	master=subframe_a,
	text="Recoil",
)
lbl_M4.grid(row=4, column=0)
ent_M4 = Entry(
	master=subframe_a,
	width=4,
)
ent_M4.grid(row=4, column=1)

lbl_Ex = Label(
	master=subframe_a,
	text="Ex energy",
)
lbl_Ex.grid(row=5, column=0)
ent_Ex = Entry(
	master=subframe_a,
	width=6,
)
ent_Ex.grid(row=5, column=1)






# the figure that will contain the plot 
fig = plt.figure(figsize = (8, 5.5), 
         dpi = 100) 


# adding the subplot 
plot1 = fig.add_subplot(111) 
plot1.minorticks_on()
#plot1.grid()

plt.tick_params(axis='both', which='both', direction='in')
plt.title('Light ejectile kinematics')
plt.xlabel('Angle [Degrees]')
plt.ylabel('Energy [MeV]')



# creating the Tkinter canvas 
# containing the Matplotlib figure 
canvas = FigureCanvasTkAgg(fig, master = frame_b) 

# placing the canvas on the Tkinter window 
canvas.get_tk_widget().pack()

# creating the Matplotlib toolbar 
toolbar = NavigationToolbar2Tk(canvas, frame_b) 
toolbar.update() 
  
# placing the toolbar on the Tkinter window 
canvas.get_tk_widget().pack() 

  
# place the button  
# in main window 
plot_button.pack() 



frame_a.pack(fill=BOTH,side=LEFT, expand=False)
subframe_a.pack(fill=BOTH,side=TOP, expand=False)
frame_b.pack(fill=BOTH,side=LEFT, expand=False)

delete_button.pack()
quit_button.pack(fill=BOTH,side=BOTTOM)
  
# run the gui 
window.mainloop() 
