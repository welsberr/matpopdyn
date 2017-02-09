# matpopdyn
Matrix-based Population Dynamics (Leslie and Lefkovitch approaches)

Code to generically handle population dynamics using either Leslie age-matrix or Lefkovich age-stage matrix approaches.

Originally released in my blog post, "Population Modeling in Python", 2012/10/08
http://austringer.net/wp/index.php/2012/10/08/population-modeling-in-python/

Text from that post:

A long-time standard method in population modeling is the Leslie matrix. This technique applies when one has data about the age structure of a population and produces estimates going forward by using matrix multiplication to go from the population numbers, fecundity, and survivorship numbers to get the estimate of the population in each age class at the next time step.

A similar method is the Lefkovitch approach. This is still based upon matrix operations, but the underlying data involves stages rather than age structure. This sort of model is often used to capture more complex life histories than are tracked in a Leslie matrix model.

The similarities make it straightforward to incorporate both approaches into one supporting Python class.

The following Python module defines the LMatrix class. The dependencies are the Numpy module and the interval module. I used “pip install interval” to get the interval module on my machine. If you run this module in standalone mode, it runs a test of the LMatrix model with a web-accessible example of a Leslie matrix and of a Lefkovitch matrix.
