# C:\Users\Mallory\Documents\code24.py

from Tkinter import *

def main():
	global t, T
	C = T[:]
	iter = 0
	while (iter <= detey):
		k, n = 0, 0
		m = -(Nx-1)
		T = C[:]
		while (k < Nx*Ny):
			if (k==0): 																# Coin Sud Ouest
				C[k] = T[k]*(1-4*Foh*(h*alpha+1)) + 4*Foh*alpha*h*T0 + 2*Foh*(T[k+Nx]+T[k+1])
			elif (k==Nx*(Ny-1)):													# Coin Nord Ouest
				C[k] = T[k]*(1-4*Foh*(h*alpha+1)) + 4*Foh*alpha*h*T0 + 2*Foh*(T[k-Nx]+T[k+1])
			elif (k==Nx*Ny-1):														# Coin Nord Est
				C[k] = T[k]*(1-4*Foh*(h*alpha+1)) + 4*Foh*alpha*h*T0 + 2*Foh*(T[k-Nx]+T[k-1])
			elif (k==Nx-1):															# Coin Sud Est
				C[k] = T[k]*(1-4*Foh*(h*alpha+1)) + 4*Foh*alpha*h*T0 + 2*Foh*(T[k+Nx]+T[k-1])
			elif (k<Nx-1):
				C[k] = T[k]*(1-2*Foh*(alpha*h+2)) + 2*Foh*alpha*h*T0 + 2*Foh*(T[k+Nx] + T[k+1]/2 + T[k-1]/2)			# Sud
			elif ((Nx*Ny-k)<Nx):
				C[k] = T[k]*(1-2*Foh*(alpha*h+2)) + 2*Foh*alpha*h*T0 + 2*Foh*(T[k-Nx] + T[k+1]/2 + T[k-1]/2)			# Nord
			elif (n==Nx and k!=Nx*(Ny-1)):
				C[k] = T[k]*(1-2*Foh*(alpha*h+2)) + 2*Foh*alpha*h*T0 + 2*Foh*(T[k+1] + T[k+Nx]/2 + T[k-Nx]/2)			# Ouest
				n = 0
			elif (m==Nx):
				C[k] = T[k]*(1-2*Foh*(alpha*h+2)) + 2*Foh*alpha*h*T0 + 2*Foh*(T[k-1] + T[k+Nx]/2 + T[k-Nx]/2)			# Est
				m = 0
			elif (k == Nx*Ny/4 + Nx/4):
				C[k] = T[k]*(1-4*Foh) + Foh*(T[k+1] + T[k-1] + T[k+Nx] + T[k-Nx]) + dt*Q	# Terme source au milieu
				
			elif (k == Nx*Ny/4 + 15*Nx/2):
				C[k] = T[k]*(1-4*Foh) + Foh*(T[k+1] + T[k-1] + T[k+Nx] + T[k-Nx]) + dt*2	# Terme source au milieu
				
			else:
				C[k] = T[k]*(1-4*Foh) + Foh*(T[k+1] + T[k-1] + T[k+Nx] + T[k-Nx])			# Reste des noeuds
			n += 1
			m += 1
			k += 1
		t += dt
		iter += 1
	T = C[:]
	plotter(T)
	if flag>0:
		fen.after(100,main)
		
def plotter(T):
	k, n, m = 0, 0, 0
	while (k<Nx*Ny):
		diff = max(T)-min(T)
		if diff:
			r = 764*(T[k]-min(T))/(max(T)-min(T))
		else:
			r = 382
		r = int(r)
		color = convertcol(r)
		if (n==Nx):				
			n = 0
			m += 1
		can.create_rectangle(n*h,m*h, (n+1)*h,(m+1)*h, fill=color, outline='')	
		k += 1
		n += 1
		
def convertcol(cool):	
	s = "#"
	alpha = (cool-cool%255)/255
	b = cool%255
	if alpha==0:
		s += "00"
		s += inter(b)
		s += "ff"
	elif alpha==1:
		s += inter(b)
		s += "ff"
		s += inter(255-b)
	elif alpha==2:
		s += "ff"
		s += inter(255-b)
		s += "00"
	return s

def inter(dec):
	k = 1
	s = ""
	while k>=0:
		intertype = (dec-dec%16**k)/16**k
		ic = convhexa(intertype)
		s += ic
		dec -= (intertype)*16**k
		k -= 1
	return s

def convhexa(two):
	if two>9:
		if two==10:
			two = "a"
		elif two==11:
			two = "b"
		elif two==12:
			two = "c"
		elif two==13:
			two = "d"
		elif two==14:
			two = "e"
		elif two==15:
			two = "f"
	two = str(two)
	return two

def start():
	global flag
	if flag==0:
		flag = 1
		main()
	else:
		flag = 0

def reinit():
	global t, T
	t = 0
	T = []
	k = 0
	while (k < Nx*Ny):
		T.append(T0)
		k += 1
	can.delete("all")

fen = Tk()
haut = 300
larg = 300
can = Canvas(fen, height = haut, width = larg, bg = 'ivory')
can.pack()

buttstart = Button(fen, text='Start / Stop', command=start).pack()
buttinit = Button(fen, text='Init', command=reinit).pack()

t = 0
flag = 0
T0 = 20
alpha = 1e-3
D = 1
Foh = 0.24
Q = 1
detey = 10
Nx = 20
h = larg/Nx
Ny = haut/h
dt = Foh*h*h/D

reinit()

fen.mainloop()