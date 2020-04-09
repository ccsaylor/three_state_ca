import random
from matplotlib import pyplot as plt
from numpy import array_equal

def lookup_table(rule_number):
    """
    Returns a dictionary which maps ECA neighborhoods to output values. 
    Uses Wolfram rule number convention.
    
    Parameters
    ----------
    rule_number: int
        Integer value between 0 and 255, inclusive. Specifies the ECA lookup table
        according to the Wolfram numbering scheme.
        
    Returns
    -------
    lookup_table: dict
        Lookup table dictionary that maps neighborhood tuples to their output according to the 
        ECA local evolution rule (i.e. the lookup table), as specified by the rule number. 
    """
    if not isinstance(rule_number, int) or rule_number < 0 or rule_number > 19682:
        raise ValueError("rule_number must be an int between 0 and 19682, inclusive")
    neighborhoods = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
    n = rule_number
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    in_ternary = ''.join(reversed(nums))
    ternary_length = len(in_ternary)
    if ternary_length != 9:
        padding = 9 - ternary_length
        in_ternary = '0'*padding + in_ternary

    
    return dict(zip(neighborhoods, map(int, reversed(in_ternary)))) # use map so that outputs are ints, not strings

def unit_seed(margin_length):
    """
    Returns a list of a single '1' bounded by margin_length number of '0's 
    on either side. 
    
    Parameters
    ----------
    margin_length: int
        Number of zeros bounding the central one on either side. 
        
    Returns
    -------
    out: list
        [0,]*margin_length + [1,] + [0,]*margin_length
    """
    if not isinstance(margin_length, int) or margin_length < 0:
        raise ValueError("margin_length must be a postive int")
    
    return [0,]* margin_length + [1,] + [0,]*margin_length

def random_string(length):
    """
    Returns a list of 0s, 1s and 2s
    
    Parameters
    ----------
    length: int
        Number of values in list
        
    Returns
    -------
    out: list
    """
    initial_condition = [random.randint(0,2) for _ in range(length)]

    return initial_condition

def spacetime_field(rule_number, initial_condition, time_steps):
    """
    Returns a spacetime field array using the given rule number on the 
    given initial condition for the given number of time steps.
    
    Parameters
    ----------
    rule_number: int
        Integer value between 0 and 255, inclusive. Specifies the ECA lookup table
        according to the Wolfram numbering scheme.
    initial_condition: list
        Binary string used as the initial condition for the ECA. Elements of the list
        should be ints. 
    time_steps: int
        Positive integer specifying the number of time steps for evolving the ECA. 
    """
    if time_steps < 0:
        raise ValueError("time_steps must be a non-negative integer")
    # try converting time_steps to int and raise a custom error if this can't be done
    try:
        time_steps = int(time_steps)
    except ValueError:
        raise ValueError("time_steps must be a non-negative integer")
        
    # we will see a cleaner and more efficient way to do the following when we introduce numpy
    for i in initial_condition:
        if i not in [0,1,2]:
            raise ValueError("initial condition must be a list of 0s, 1s and 2s")
        
    lookup = lookup_table(rule_number)
    length = len(initial_condition)
    
    # initialize spacetime field and current configuration
    spacetime_field = [initial_condition]
    current_configuration = initial_condition.copy()

    # apply the lookup table to evolve the CA for the given number of time steps
    for t in range(time_steps):
        new_configuration = []
        for i in range(length):

            neighborhood = (current_configuration[(i-1)%length], 
                            current_configuration[i])

            new_configuration.append(lookup[neighborhood])

        current_configuration = new_configuration
        spacetime_field.append(new_configuration)
    
    return spacetime_field

def spacetime_diagram(
        spacetime_field, size=12, colors=plt.cm.Greys):
    """
    Produces a simple spacetime diagram image using matplotlib imshow with 'nearest' interpolation.
    
   Parameters
    ---------
    spacetime_field: array-like (2D)
        1+1 dimensional spacetime field, given as a 2D array or list of lists. Time should be dimension 0;
        so that spacetime_field[t] is the spatial configuration at time t. 
        
    size: int, optional (default=12)
        Sets the size of the figure: figsize=(size,size)
    colors: matplotlib colormap, optional (default=plt.cm.Greys)
        See https://matplotlib.org/tutorials/colors/colormaps.html for colormap choices.
        A colormap 'cmap' is called as: colors=plt.cm.cmap
    """
    plt.figure(figsize=(size,size))
    plt.imshow(spacetime_field, cmap=colors, interpolation='nearest')
    plt.show()

def test_lookup_table255():
    lt = lookup_table(255)
    expected_outputs = [0, 1, 1, 0, 0, 1, 0, 0, 0] # outputs in lexicographical order
    for neighborhood, expected_out in zip(neighborhoods, expected_outputs):
        assert lt[neighborhood] == expected_out,\
        "neighborhood {} gives wrong output!".format(neighborhood)
    print("all outputs look good!") # remove if using testing framework like nose

def test_lookup_table9841():
    lt = lookup_table(9841)
    expected_outputs = [1, 1, 1, 1, 1, 1, 1, 1, 1] # outputs in lexicographical order
    for neighborhood, expected_out in zip(neighborhoods, expected_outputs):
        assert lt[neighborhood] == expected_out,\
        "neighborhood {} gives wrong output!".format(neighborhood)
    print("all outputs look good!") # remove if using testing framework like nose

def test_lookup_table19682():
    lt = lookup_table(19682)
    expected_outputs = [2, 2, 2, 2, 2, 2, 2, 2, 2] # outputs in lexicographical order
    for neighborhood, expected_out in zip(neighborhoods, expected_outputs):
        assert lt[neighborhood] == expected_out,\
        "neighborhood {} gives wrong output!".format(neighborhood)
    print("all outputs look good!") # remove if using testing framework like nose

def test_spacetime0():
    obs_field = spacetime_field(0, random_string(20), 20)
    expected_config = [0,]*20
    
    for time, observed_config in enumerate(obs_field[1:]): # skip the random initial condition
        assert array_equal(observed_config, expected_config), \
        "configuration at time {} not correct".format(time)
    print('All configurations correct!') # remove if using testing framework like nose

def test_spacetime22():
    initial = [0,0,2,0,1,0]
    obs_field = spacetime_field(22, initial, 2)
    expected_config_1 = [1, 1, 2, 0, 1, 0]
    expected_config_2 = [1, 0, 0, 0, 1, 0]
    assert array_equal(obs_field[1], expected_config_1), \
    "time step 1 is incorrect"
    assert array_equal(obs_field[2], expected_config_2),\
    "time step 2 is incorrect"
    print('both time steps give correct output') # remove if using testing framework like nose

    
class ECA(object):
    """
    Elementary cellular automata simulator.
    """
    def __init__(self, rule_number, initial_condition):
        """
        Initializes the simulator for the given rule number and initial condition.
        
        Parameters
        ----------
        rule_number: int
            Integer value between 0 and 255, inclusive. Specifies the ECA lookup table
            according to the Wolfram numbering scheme.
        initial_condition: list
            Binary string used as the initial condition for the ECA. Elements of the list
            should be ints. 
        
        Attributes
        ----------
        lookup_table: dict
            Lookup table for the ECA given as a dictionary, with neighborhood tuple keys. 
        initial: array_like
            Copy of the initial conditions used to instantiate the simulator
        spacetime: array_like
            2D array (list of lists) of the spacetime field created by the simulator.
        current_configuration: array_like
            List of the spatial configuration of the ECA at the current time
        """
        # we will see a cleaner and more efficient way to do the following when we introduce numpy
        for i in initial_condition:
            if i not in [0,1,2]:
                raise ValueError("initial condition must be a list of 0s, 1s and 2s")
                
        self.lookup_table = lookup_table(rule_number)
        self.initial = initial_condition
        self.spacetime = [initial_condition]
        self.current_configuration = initial_condition.copy()
        self._length = len(initial_condition)

    def evolve(self, time_steps):
        """
        Evolves the current configuration of the ECA for the given number of time steps.
        
        Parameters
        ----------
        time_steps: int
            Positive integer specifying the number of time steps for evolving the ECA.  
        """
        if time_steps < 0:
            raise ValueError("time_steps must be a non-negative integer")
        # try converting time_steps to int and raise a custom error if this can't be done
        try:
            time_steps = int(time_steps)
        except ValueError:
            raise ValueError("time_steps must be a non-negative integer")

        for _ in range(time_steps): # use underscore if the index will not be used
            new_configuration = []
            for i in range(self._length):

                neighborhood = (self.current_configuration[(i-1)%self._length], 
                                self.current_configuration[i])

                new_configuration.append(self.lookup_table[neighborhood])

            self.current_configuration = new_configuration
            self.spacetime.append(new_configuration)

rule_110 = ECA(110, random_string(100))
rule_110.evolve(50)
spacetime_diagram(rule_110.spacetime, 10)