:::::::::::::::::::
Inverter Modulation
:::::::::::::::::::

*keywords*: Power Electronics, Single phase Inverter, PWM

Purpose
-------
Small graphical illustration of different kinds of PWM command types
for a *single phase* inverter.

The duty cycle can be dynamically set.

Available options
-----------------
* sawtooth counter
* triangle counter (that is symetric sawtooth)
* counter offset between the two legs

Output Examples
---------------

Sawtooth counter, +Vdc/-Vdc output:

.. image:: https://github.com/pierre-haessig/inverter-modulation/raw/master/pwm_complementary.png

Triangle counter, +Vdc/0/-Vdc output:

.. image:: https://github.com/pierre-haessig/inverter-modulation/raw/master/pwm_symetrical.png

Pierre Haessig - February 1st, 2012

Update June 2012: 
Does not clear anymore the figure at each plot update,
but use set_data() or remove() method instead.
-> Better performance (animation fluidity) expected.
