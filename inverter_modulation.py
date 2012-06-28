#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" Small graphical illustration of different kinds of PWM command types
for a *single phase* inverter.

Pierre Haessig — February 2012
update June 2012: do not clear the figure at each update anymore,
                  use set_data() or remove() method instead.
                  -> better performance (fluidity) expected
"""

from __future__ import division, print_function

import numpy as np
import matplotlib.pyplot as plt
from traits.api import Range, Enum, Bool, HasTraits

### Parameters of the plot
N = 100 # How many points in the plots
T = 1 # Period of the modulator
Vdc = 1. # Amplitude of the DC bus

# Create the time vector:
t = np.linspace(-T,2*T, N)
tnorm = t/T

# Permanent dict to store the plot objects & patches
pwm = {}


class ModulationParameters(HasTraits):
    '''parameters of the PWM modulation'''
    duty_cycle = Range(0.,1.,0.25,
                       label=u'duty cycle',
                       desc= u'modulation duty cycle')
    counter_type = Enum(('sawtooth', 'triangle'),
                        label=u'counter type',
                        desc= u'modulator counter type')
    
    revert_counter_2 = Bool(False,
                            label=u'revert counter 2',
                            desc= u'whether to revert counter 2')
    offset_counter_2 = Range(0.,1.,0.0,
                             label=u'offset counter 2',
                             desc= u'how much time offset for counter 2')
    
    def __init__(self, **traits):
        '''initialize the plot'''
        HasTraits.__init__(self, **traits)
        
        init_plot_pwm(self.duty_cycle, self.counter_type,
                      self.revert_counter_2, self.offset_counter_2)
        
    def update_plot(self):
        '''update the plot'''
        update_plot_pwm(self.duty_cycle, self.counter_type,
                        self.revert_counter_2, self.offset_counter_2)
# end of ModulationParameters class


def init_plot_pwm(duty_cycle, counter_type, revert_counter_2, offset_counter_2):
    '''plot the inverter modulation for the first time.
    Plot objects are stored in the `pwm` dict
    '''
    if counter_type=='sawtooth':
        counter1 = tnorm % 1
        counter2 = (tnorm-offset_counter_2) % 1
    elif counter_type=='triangle':
        counter1 = tnorm % 1
        counter1 = 2*counter1    *(counter1 <0.5) +\
                   2*(1-counter1)*(counter1>=0.5)
        counter2 = (tnorm-offset_counter_2) % 1
        counter2 = 2*counter2    *(counter2 <0.5) +\
                   2*(1-counter2)*(counter2>=0.5)
    else: raise ValueError('unknown counter_type "%s"' % counter_type)
    
    if revert_counter_2:
        counter2 = 1-counter2
    
    ### Compute Legs voltages:
    volt1 = (counter1 < duty_cycle)*Vdc
    volt2 = (counter2 >= duty_cycle)*Vdc
    volt_inv= volt1-volt2
    
    ### Plot:
    # Dictionnary to hold all the useful references to plot objects
    #pwm = {}
    fig, (ax1, ax2, ax_inv) = plt.subplots(3, 1, sharex=True, 
                                          num='Inverter Modulation')
    pwm['fig'] = fig
    pwm['ax1'] = ax1
    pwm['ax2'] = ax2
    pwm['ax_inv'] = ax_inv
    
    # Leg 1
    pwm['cnt_line1'],pwm['volt_line1'] = ax1.plot(t, counter1, t, volt1, 'r')
    pwm['cmp_line1'] = ax1.hlines(duty_cycle, t.min(), t.max(),
                           linestyle='dashed', colors='b')
    pwm['cmp_fill1'] = ax1.fill_between(t,duty_cycle, counter1,
                             where=(counter1 < duty_cycle), alpha=0.2)
    ax1.set_title('Leg 1 modulation')
    ax1.legend((pwm['cnt_line1'],pwm['cmp_line1'],pwm['volt_line1']),('count 1','duty','volt 1'))
    ax1.grid(True)
    ax1.set_ylim(min(-.1*Vdc,-0.1), max(1.1*Vdc,1.1))

    # Leg 2
    pwm['cnt_line2'],pwm['volt_line2'] = ax2.plot(t, counter2, t, volt2, 'r')
    pwm['cmp_line2'] = ax2.hlines(duty_cycle, t.min(), t.max(),
                           linestyle='dashed', colors='b')
    pwm['cmp_fill2'] = ax2.fill_between(t, duty_cycle, counter2,
                            where= counter2 >= duty_cycle, alpha=0.2)
    ax2.set_title('Leg 2 modulation')
    ax2.legend((pwm['cnt_line2'],pwm['cmp_line2'],pwm['volt_line2']),('count 2','1 - duty','volt 2'))
    ax2.set_ylim(min(-.1*Vdc,-0.1), max(1.1*Vdc,1.1))
    ax2.grid(True)
    
    # Inverter voltages
    pwm['volt_line_inv'], = ax_inv.plot(t, volt_inv , 'r', label='voltage')
    pwm['avg_line_inv'] = ax_inv.hlines(Vdc*(2*duty_cycle-1), t.min(), t.max(),
                                linestyle='dashed', colors='r', label='average')
    ax_inv.set_title('Inverter voltage')
    ax_inv.set_xlabel('time')
    ax_inv.legend()
    ax_inv.grid(True)
    ax_inv.set_ylim(-1.1*Vdc, 1.1*Vdc)
    
    # Better subplot layout
    fig.tight_layout()
    # Display !
    fig.show()
# end init_plot_pwm


def update_plot_pwm(duty_cycle, counter_type, revert_counter_2, offset_counter_2):
    '''update the inverter modulation plot
    by updating the plot object found in the `pwm` dict
    '''
    if counter_type=='sawtooth':
        counter1 = tnorm % 1
        counter2 = (tnorm-offset_counter_2) % 1
    elif counter_type=='triangle':
        counter1 = tnorm % 1
        counter1 = 2*counter1    *(counter1 <0.5) +\
                   2*(1-counter1)*(counter1>=0.5)
        counter2 = (tnorm-offset_counter_2) % 1
        counter2 = 2*counter2    *(counter2 <0.5) +\
                   2*(1-counter2)*(counter2>=0.5)
    else: raise ValueError('unknown counter_type "%s"' % counter_type)
    
    if revert_counter_2:
        counter2 = 1-counter2

    ### Compute Legs voltages:
    volt1 = (counter1 < duty_cycle)*Vdc
    volt2 = (counter2 >= duty_cycle)*Vdc
    volt_inv= volt1-volt2

    ### Plot:
    # Leg 1
    pwm['cnt_line1'].set_data(t, counter1)
    pwm['volt_line1'].set_data(t, volt1)
    pwm['cmp_fill1'].remove()
    pwm['cmp_fill1'] = pwm['ax1'].fill_between(t, duty_cycle, counter1,
                                   where=(counter1 < duty_cycle), alpha=0.2)
    pwm['cmp_line1'].remove()
    pwm['cmp_line1'] = pwm['ax1'].hlines(duty_cycle, t.min(), t.max(),
                                         linestyle='dashed', colors='b')

    # Leg 2
    pwm['cnt_line2'].set_data(t, counter2)
    pwm['volt_line2'].set_data(t, volt2)
    pwm['cmp_fill2'].remove()
    pwm['cmp_fill2'] = pwm['ax2'].fill_between(t, duty_cycle, counter2,
                                   where = counter2 >= duty_cycle, alpha=0.2)
    pwm['cmp_line2'].remove()
    pwm['cmp_line2'] = pwm['ax2'].hlines(duty_cycle, t.min(), t.max(),
                                         linestyle='dashed', colors='b')

    # Inverter voltages
    pwm['volt_line_inv'].set_data(t, volt_inv)
    pwm['avg_line_inv'].remove()
    pwm['avg_line_inv'] = pwm['ax_inv'].hlines(Vdc*(2*duty_cycle-1),
                                               t.min(), t.max(),
                                linestyle='dashed', colors='r', label='average')
    pwm['fig'].canvas.draw()
# end update_plot_pwm


if __name__ == '__main__':
    # Launch the plot:
    m = ModulationParameters()
    m.on_trait_change(handler = m.update_plot)
    # Lauch the Traits modification UI:
    m.configure_traits()
