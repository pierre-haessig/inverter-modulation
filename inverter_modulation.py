#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" Small graphical illustration of different kinds of PWM command types
for a *single phase* inverter.

Pierre Haessig — February 2012
"""

from __future__ import division, print_function

import numpy as np
import matplotlib.pyplot as plt

from traits.api import Range, Enum, Bool, HasTraits


class ModulationParameters(HasTraits):
    duty_cycle = Range(0.,1.,0.1,
                       label=u'duty cycle',
                       desc= u'modulation duty cycle')
    counter_type = Enum(('sawtooth', 'triangle'),
                        label=u'counter type',
                        desc= u'modulator counter type')
    
    revert_counter_2 = Bool(True,
                            label=u'revert counter 2',
                            desc= u'whether to revert counter 2')
    offset_counter_2 = Range(0.,1.,0.0,
                             label=u'offset counter 2',
                             desc= u'how much time offset for counter 2')
    def update_plot(self):
        '''update the Inverter modulation plot'''
        plot_pwm(self.duty_cycle, 
                 self.counter_type, self.revert_counter_2, self.offset_counter_2)
        
def plot_pwm(duty_cycle, counter_type, revert_counter2, offset2):
    '''plot the inverter modulation'''
    N = 1000 # How many points in the plots
    T = 1
    Vdc = 1.
    t = np.linspace(-T,2*T, N)
    if counter_type=='sawtooth':
        tnorm = t/T
        counter1 = tnorm % 1
        counter2 = (tnorm-offset2) % 1
    elif counter_type=='triangle':
        tnorm = t/T
        counter1 = tnorm % 1
        counter1 = 2*counter1    *(counter1 <0.5) +\
                   2*(1-counter1)*(counter1>=0.5)
        counter2 = (tnorm-offset2) % 1
        counter2 = 2*counter2    *(counter2 <0.5) +\
                   2*(1-counter2)*(counter2>=0.5)
    else: raise ValueError('unknown counter_type "%s"' % counter_type)
    
    if revert_counter2:
        counter2 = 1-counter2

    ### Compute Legs voltages:
    volt1 = (counter1 < duty_cycle)*Vdc
    volt2 = (counter2 < (1-duty_cycle))*Vdc
    volt_inv= volt1-volt2

    ### Plot:
    fig, (ax1, ax2, axInv) = plt.subplots(3, 1, sharex=True, num='Inverter Modulation')
    # Leg 1
    ax1.clear()
    lc,lv = ax1.plot(t, counter1, t, volt1, 'r')
    ld = ax1.hlines(duty_cycle, t.min(), t.max(), linestyle='dashed', colors='b')
    ax1.fill_between(t,duty_cycle, counter1, where=(counter1 < duty_cycle), alpha=0.2)
    ax1.set_title('Leg 1 modulation')
    ax1.legend((lc,ld,lv),('count 1','duty','volt 1'))
    ax1.grid(True)
    ax1.set_ylim(min(-.1*Vdc,-0.1), max(1.1*Vdc,1.1))

    # Leg 2
    ax2.clear()
    lc,lv = ax2.plot(t, counter2, t, volt2, 'r')
    ld = ax2.hlines(1-duty_cycle, t.min(), t.max(), linestyle='dashed', colors='b')
    ax2.fill_between(t,(1-duty_cycle), counter2, where=(counter2 <(1-duty_cycle)), alpha=0.2)
    ax2.set_title('Leg 2 modulation')
    ax2.legend((lc,ld,lv),('count 2','1 - duty','volt 2'))
    ax2.set_ylim(min(-.1*Vdc,-0.1), max(1.1*Vdc,1.1))
    ax2.grid(True)
    
    # Inverter voltages
    axInv.clear()
    axInv.plot(t, volt_inv , 'r')
    axInv.hlines(Vdc*(2*duty_cycle-1), t.min(), t.max(), linestyle='dashed', colors='r')
    axInv.set_title('Inverter voltage')
    axInv.set_xlabel('time')
    axInv.legend(('voltage', 'average'))
    axInv.grid(True)
    axInv.set_ylim(-1.1*Vdc, 1.1*Vdc)
    fig.canvas.draw()
    fig.show()

if __name__ == '__main__':
    # Launch the plot
    m = ModulationParameters()
    m.on_trait_change(handler = m.update_plot)
    m.update_plot()
    m.configure_traits()
