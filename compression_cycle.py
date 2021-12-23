import CoolProp
from CoolProp.Plots import PropertyPlot
from CoolProp.Plots import SimpleCompressionCycle
import matplotlib.pyplot as plt


pp = PropertyPlot('HEOS::R32', 'PH', unit_system='EUR')
pp.calc_isolines()
cycle = SimpleCompressionCycle('HEOS::R32', 'PH', unit_system='EUR')
T0 = 273.15+0
pp.state.update(CoolProp.QT_INPUTS,0.0,T0-10)
p0 = pp.state.keyed_output(CoolProp.iP)
T2 = 273.15+68
pp.state.update(CoolProp.QT_INPUTS,1.0,T2+5)
p2 = pp.state.keyed_output(CoolProp.iP)
pp.calc_isolines(CoolProp.iT, [T0-273.15,T2-273.15], num=2)
cycle.simple_solve(T0, p0, T2, p2, 0.7, SI=True)
cycle.steps = 50
sc = cycle.get_state_changes()
print(sc)

pp.draw_process(sc)

plt.close(cycle.figure)

pp.show()
