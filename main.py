import CoolProp
from CoolProp.CoolProp import PropsSI
from CoolProp.Plots import PropertyPlot, SimpleCompressionCycle
import matplotlib.pyplot as plt
import numpy as np

from helpers import bar_to_kPa, kw_to_tr

deg = u"\N{DEGREE SIGN}"

refrigerant = 'R134a'

'''Suction Conditions'''
t_sat_evap = 1.7 #degC
superheat = 10 #degC

'''Discharge Conditions'''
t_sat_cond = 51.7 #degC
subcooling = 5 #degC

'''Compressor Parameters'''
Vswept = 309.6 #m3/hr @ 3000rpm (Swept Volume)
rev = 6600 #rpm (Compressor Speed)
volume_eff = 0.9 # Volumetric Efficiency
ie = 0.70 # Isentropic Efficiency
motor_eff = 0.95 # Motor Efficiency

''' Suction and Discharge parameters '''
p_suc = PropsSI('P','T', t_sat_evap+273.15, 'Q', 0, refrigerant)/100000 #barG
p_dis = PropsSI('P','T', t_sat_cond+273.15, 'Q', 0, refrigerant)/100000 #barG
density = PropsSI('D','T',t_sat_evap+superheat+273.15,'P',p_suc*100000,refrigerant)


'''Compressor Calc'''
c_dis = Vswept/(3000*60) #m3/rev
f = rev / 60 #Hz
V_suc = c_dis * volume_eff * rev * 60 #m3/hr
m = density * c_dis * volume_eff *rev / 60 # mass flow [kg/s]

'''Entalpies of the compression cycle'''
s1 = PropsSI('S', 'T', t_sat_evap+superheat+273.15, 'P', p_suc*100000, refrigerant)/1000 # [kJ/kg.K]
s2 = s1 # [kJ/kg]
h1 = PropsSI('H', 'T', t_sat_evap+superheat+273.15, 'P', p_suc*100000, refrigerant)/1000 # [kJ/kg]
h2 = PropsSI('H', 'P', p_dis*100000, 'S', s1*1000, refrigerant)/1000 # [kJ/kg]
h2a = ((h2-h1)/ie)+h1 # [kJ/kg]
#T_dis_ie = PropsSI('T','P', p_dis*100000, 'S', s2, refrigerant) # Isentropic Discharge Temperature
#T_dis_a = PropsSI('T','P', p_dis*100000, 'H', h2a, refrigerant) # Actual Discharge Temperature
h3 = PropsSI('H', 'T',t_sat_cond-subcooling+273.15, 'P', p_dis*100000, refrigerant)/1000 # [kJ/kg]
h4 = h3 # [kJ/kg]
qL = h1 - h4 #/ Latent heat [kj/Kg]
w_comp = h2a - h1 # Compressor work [kJ/kg]
w_input = w_comp / motor_eff # Input work [kJ/kg]
Qh = m * (h2a - h3) # Condeser Capacity [kW]
Ql = qL * m # Evaporator Capacity [kW]
Wcomp = w_comp * m # Comporessor duty [kW]
Winput = w_input * m # Input Power [kW]
COPr = Ql / Winput # Refrigeration COP
COPh = Qh / Winput # Heat pump COP

print("CONDITIONS")
print(f"Te = {t_sat_evap} {deg}C")
print(f"ps = {p_suc} barG")
print(f"Tc = {t_sat_cond} {deg}C")
print(f"pd = {p_dis} barG")
print(f"Ro = {density} kg/m3")

print("")

#Print Compresso Parameters
print(f"Theoretical Swept Volume = {Vswept} m3/hr @ 3000 rpm")
print(f"Comporessor Displacement = {c_dis} m3/rev")
print(f"Volumetric Efficiency = {volume_eff*100} %")
print(f"Speed = {rev} rpm")
print(f"Suction Volume Flow Rate = {V_suc} m3/hr @ {rev} rpm")
print(f"Mass Flow = {m} kg/s @ {rev} rpm")

print('')

print(h1)
print(h2)
print(h2a)
print(s1)
print(s2)
print(h3)
print(h4)
print(qL)
print(w_comp)
print(w_input)
print(Qh)
print(Ql)
print(Wcomp)
print(Winput)
print(COPr)
print(COPh)
print(kw_to_tr(Qh))
print(kw_to_tr(Ql))


h_points = np.array([h1, h2a, h3, h4, h1])
p_points = np.array([p_suc, p_dis, p_dis, p_suc, p_suc])


pp = PropertyPlot(f"HEOS::{refrigerant}", 'PH', unit_system='EUR')
pp.calc_isolines()
cycle = SimpleCompressionCycle(f"HEOS::{refrigerant}", 'PH', unit_system='EUR')
T0 = 273.15+t_sat_evap
pp.state.update(CoolProp.QT_INPUTS,0.0,T0-superheat)
p0 = pp.state.keyed_output(CoolProp.iP)
T2 = 273.15+t_sat_cond
pp.state.update(CoolProp.QT_INPUTS,1.0,T2+subcooling)
p2 = pp.state.keyed_output(CoolProp.iP)
pp.calc_isolines(CoolProp.iT, [T0-273.15,T2-273.15], num=2)
cycle.simple_solve(T0, p0, T2, p2, 0.7, SI=True)
cycle.steps = 50
sc = cycle.get_state_changes()

pressures = np.array(sc.P/100000)
enthalpies = np.array(sc.H/1000)

plt.plot(h_points, p_points, 'g')
plt.plot((h1, h2), (p_suc, p_dis), 'r')
plt.plot(enthalpies, pressures, 'b')

plt.xlabel("Specific Enthalpy [kJ/kg]")
plt.ylabel("Pressure [bar]")
plt.title(f"Compression Cycle with {refrigerant}")
plt.grid()

plt.savefig("Charts/Cycle.png")

pp.draw_process(sc)
pp.title(f"p-h Diagram of {refrigerant}")
pp.savefig('Charts/p-h.png')
#pp.show()

#plt.show()