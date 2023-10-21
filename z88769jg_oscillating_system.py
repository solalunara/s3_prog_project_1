#%%

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
<http://www.gnu.org/licenses/>.
"""

__author__ = "Luna Greenberg"
__email__ = __contact__ = "jackgphysics@gmail.com"
__date__ = "2023/10/18"
__deprecated__ = False
__license__ = "GPLv3"
__status__ = "Production"
__version__ = "0.0.2"

### IMPORTS ###
import numpy as np;
import matplotlib.pyplot;

### UTILITY FUNCTIONS ###

def ConditionalInput( condition, prompt: str, failprompt ) -> float:
    """Get a float value from the user and validate it against an arbitrary condition
    
       Parameters:
            condition -- lambda function (float -> bool) used to validate user input\n
            prompt -- string the program should prompt the user for the input\n
            failprompt -- lambda function (float -> string) that returns what the program should say when the user's input fails to meet the condition\n
        Returns:
            float -- a float value provided by the user that satisfies the condition
    """
    # treat -inf like a holding value
    # because python doesn't have do-while loops for some reason
    # and we can check for the input being -inf manually and change it
    val = float( "-inf" );
    while ( not condition( val ) ):
        try:
            if ( val != float( "-inf" ) ):
                print( failprompt( val ) );

            val = float( input( "\n" + prompt ) );

            #just throw and call -inf an invalid number
            if ( val == float( "-inf" ) ):
                raise Exception;
        
        #can't do blanket except, breaks Control-C functionality
        except Exception:
            print( "That was not a valid number. Valid numbers include only digits and a maximum of one (1) decimal place." );
            val = float( "-inf" );
        
        #add a little 7C easter egg for Control-C
        except KeyboardInterrupt:
            print( "\nIt's hard to believe that it's over, isn't it? Funny, how we get attached to the struggle" );
            exit( 1 );
    return val;

### VARIABLES ###
# yes, functions can be variables too. look at how they're used in the code #
# see first line in "MAIN CODE EXECUTION" section for the meaning of the variable names #

def a1_condition( a1 ):
    return a1 > 0.1 and a1 < 50.0;
a1_prompt = "Please enter a value for a1: ";
def a1_failprompt( a1 ):
    if ( a1 == 0.1 or a1 == 50.0 ):
        return "Your value is exactly equal to one of the exclusive boundaries";
    elif ( a1 < 0.1 ):
        return "Your value is too low - make sure it is greater than 0.1";
    elif ( a1 > 50.0 ):
        return "Your value is too high - make sure it is less than 50.0";
    else:
        raise SystemError( "This should be an impossible state. You've been bitflipped or something has gone horribly wrong" );

def freq_condition( freq ):
    return freq >= 1 and freq <= 200;
freq_prompt = "Please enter a value for the frequency (1-200 Hz): ";
def freq_failprompt( freq ):
    if ( freq < 1 ):
        return "Your value is too low - make sure it is greater than 1";
    elif ( freq > 200 ):
        return "Your value is too high - make sure it is less than 200";
    else:
        raise SystemError( "This should be an impossible state. You've been bitflipped or something has gone horribly wrong" );

def Imin_condition( Imin ):
    return Imin > 0.0 and Imin < 1.0;
Imin_prompt = "Please enter the minimum fractional intensity (0.0-1.0) to consider: ";
def Imin_failprompt( Imin ):
    if ( Imin == 0.0 or Imin == 1.0 ):
        return "Your value is exactly equal to one of the exclusive boundaries";
    elif ( Imin < 0.0 ):
        return "Your value is too low - make sure it is greater than 0.0";
    elif ( Imin > 1.0 ):
        return "Your value is too high - make sure it is less than 1.0";
    else:
        raise SystemError( "This should be an impossible state. You've been bitflipped or something has gone horribly wrong" );


### MAIN CODE EXECUTION ###

print( "\nThe equation for a damped forced oscillation is \n\n"
       "(A0 + a1 t^2)^(-1) * cos(a2 t)\n\n"
       "where A0 takes the value 2.0 /m,\n"
       "a2 is 2pi times the frequency, which is limited to the range freq=1-200 Hz inclusive [1, 200],\n"
       "and a1 is limited to the range 0.1 to 50.0 /m/s^2 exclusive (0.1, 50.0)\n\n"
       "The oscillator will continue on indefinitely, but we can consider it finished when\n" 
       "the intensity drops below a certain fraction of what it started at, Imin, which will\n"
       "range from 0 to 1 exclusive (0, 1), at which point we will calculate the number of\n"
       "completed cycles and the time of the first minimum after the final maximum." );

# get variables from user #

#a1 relates to how fast the function decays
a1 = ConditionalInput( a1_condition, a1_prompt, a1_failprompt );

#frequency & angular velocity calculation
freq = ConditionalInput( freq_condition, freq_prompt, freq_failprompt );
a2 = freq * 2 * np.pi;

#minimum fractional intensity to consider for counting num cycles
Imin = ConditionalInput( Imin_condition, Imin_prompt, Imin_failprompt );


# do fun maths thingies #

# first analyze the system without a cosine component
# 2 / ( 2 + a1 t^2 ) = sqrt( Imin )
t_exact = np.sqrt( ( 2 / np.sqrt( Imin ) - 2 ) / a1 );

# then find the greatest multiple of n*pi that's less than t_exact
# we can do this by scaling into a coord system where the period is 1 and then taking the floor
# using 2 * freq because I = A^2
n_osc = np.floor( t_exact * 2 * freq );

#then add half a period to get to the minimum and reverse scale
t_osc = ( n_osc + 0.5 ) / ( freq * 2 );

# do a plot to sanity check the results
# 100 dots per oscillation, max 1e6
t = np.linspace( 0, 2 * t_osc, min( 100 * 2 * int( n_osc ), int(1e6) ) );
I_frac = ( 2 / ( 2 + a1 * t**2 ) * np.cos( a2 * t ) )**2
I_frac /= I_frac[ 0 ];
matplotlib.pyplot.plot( t, I_frac );
matplotlib.pyplot.axhline( Imin, label="I_min", color="r" );
matplotlib.pyplot.plot( np.array([t_osc, t_osc, t_osc]), np.linspace( 0, 1, 3 ), color="m", label="t_osc" );
matplotlib.pyplot.xlabel( "Time (seconds)" );
matplotlib.pyplot.ylabel( "Fractional Intensity" );
matplotlib.pyplot.legend();
matplotlib.pyplot.xlim( 0, 2 * t_osc );
matplotlib.pyplot.ylim( 0, 1 );

print( "\nNumber of oscillations above fractional intensity {0}: {1}".format( Imin, n_osc ) )
print( "Time of intensity minimum following {0}th peak: {1:.3f}".format( n_osc, t_osc ) );
    
# %%
