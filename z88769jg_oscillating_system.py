#!/usr/bin/env python
""" assignment 1 oscillating system

This program simulates a system that undergoes forced damped oscillations,
calculating the number of oscillations above a user-given fractional intensity
and the time taken to complete those oscillations, using a user-given frequency
for the system.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Luna Greenberg"
__email__ = __contact__ = "jackgphysics@gmail.com"
__date__ = "2023/10/18"
__deprecated__ = False
__license__ = "GPLv3"
__maintainer__ = "developer"
__status__ = "Production"
__version__ = "0.0.1"

### IMPORTS ###
import numpy as np;
from scipy.signal import argrelextrema;

### UTILITY FUNCTIONS ###

# treat -inf like a holding value
# because python doesn't have do-while loops for some reason
# and we can check for the input being -inf manually and change it
def ConditionalInput( condition, prompt, failprompt ):
    val = float( "-inf" );
    while ( not condition( val ) ):
        try:
            if ( val != float( "-inf" ) ):
                print( failprompt );

            val = float( input( "\n" + prompt ) );

            #just throw and call -inf an invalid number
            if ( val == float( "-inf" ) ):
                raise Exception;
        
        #can't do blanket except, breaks Control-C functionality
        except Exception:
            print( "That was not a valid number. Please try again." );
            val = -float( "inf" );
        
        #add a little 7C easter egg for Control-C
        except KeyboardInterrupt:
            print( "\nIt's hard to believe that it's over, isn't it? Funny, how we get attached to the struggle" );
            exit( 1 );
    return val;

### VARIABLES ###
# yes, functions can be variables too. look at how they're used in the code #

#conditions given by assignment guidelines
def a1_condition( a1 ):
    return a1 > 0.1 and a1 < 50.0;
a1_prompt = "Please enter a value for a1: ";
a1_failprompt = "Please make sure your value is in the range 0.1 to 50.0 exclusive";

#make sure the programming language can handle the value given for the frequency
def freq_condition( freq ):
    return abs( freq ) > 1e-300 and abs( freq ) < 1e300;
freq_prompt = "Please enter a value for the frequency: ";
freq_failprompt = "Why are you like this. Make sure your value is a reasonable number.";

def Imin_condition( Imin ):
    return Imin > 0.0 and Imin < 1.0;
Imin_prompt = "Please enter the minimum fractional intensity (0.0-1.0) to consider: ";
Imin_failprompt = "Please make sure your value is in the range 0.0 to 1.0 exclusive";


### MAIN CODE EXECUTION ###

print( "\nThe equation for a damped forced oscillation is \n\n"
       "(A0 + a1 t^2)^(-1) * cos(a2 t)\n\n"
       "where A0 takes the value 2.0 /m\n"
       "and a1 is limited to the range 0.1 < a1 < 50.0 /m/s^2\n" );

#get variables from user
a1 = ConditionalInput( a1_condition, a1_prompt, a1_failprompt );

freq = ConditionalInput( freq_condition, freq_prompt, freq_failprompt );
a2 = freq * 2 * np.pi;

Imin = ConditionalInput( Imin_condition, Imin_prompt, Imin_failprompt );

#make a plot

#start at N=100 and climb if neccesary
N = 100;
n = -1;
while ( n < 0 ):
    t = np.linspace( 0.0, 1/freq * N, 0.01 * ( N / 100.0 ) );
    y = ( 2.0 + a1 * t**2 )**(-1) * np.cos( a2 * t );

    max_y_indices = argrelextrema( y, np.greater );
    max_y = y[ max_y_indices ];

    #if we don't get to the fractional intensity, go again
    if ( max_y[ max_y.length - 1 ] > Imin ):
        N *= 10;
        continue;
    
    for i in range( max_y.length ):
        if ( max_y[ i ] < Imin ):
            n = i; #want the num before it goes below (-1), but +1 because start at 0
            break;
        
    min_y_indices = argrelextrema( y, np.less );
    