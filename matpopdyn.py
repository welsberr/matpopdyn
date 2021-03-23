"""
matpopdyn.py

Trying out population dynamics in Python.
Wesley R. Elsberry

"""

class LMatrix:
  """
  LMatrix

  A support class for Leslie and Lefkovitch matrix use for
  population dynamics.

  This is a generic class that allows for an arbitrary number of age
  classes or stages.
  """

  def __init__(self,stAges):
    import numpy as num
    import numpy.matlib as M
    from numpy.matlib import rand,zeros,ones,empty,eye
    import interval

    """
    In either Leslie age-structured or Lefkovitch stage-
    structured population modeling, the central feature
    is a special matrix representing both fecundity of
    ages/stages and survivorship in each age/stage.

    The Leslie age-structured matrix is slightly simpler,
    since each iteration moves the population forward
    by a time step equal to the difference between the
    age classes.

    The Lefkovitch stage-structured matrix,
    on the other hand, may have unequal times spent in
    each stage, and thus other elements of the matrix
    represent the fraction of individuals that continue
    to remain in the stage per time step of the model.
    Those lie on the main diagonal.

    The matrix in either case is an N-by-N matrix, where
    N is the number of ages or stages (stAges parameter).
    Because most values in the matrix are zero, we'll
    start with that.
    """

    self.stAges = stAges # Keep track of how many age/stage classes there are
    self.m = zeros((self.stAges,self.stAges))
    self.step = 0 # We are at the beginning
    self.popvec = []
    self.survival = []
    self.recurrence = []
    self.fecundity = []

  def LM_AddFecundity(self,fvector):
    """
    Method to set fecundity values for an LMatrix.

    This is done by setting the first row of the
    matrix to the values in the vector.

    A mismatch between the length of the vector and
    the width of the matrix leaves both unchanged.
    """
    if (fvector.shape[0] == self.stAges):
      # Just replace the row
      self.m[0] = fvector
      # Save it in the object
      self.fecundity = fvector
    else:
      print("Mismatch in size: %s vs. %s" % (self.stAges - 1,fvector.shape[0]))

  def LM_AddSurvival(self,survival):
    """
    Add the values for survival that shift population members
    from one age/stage to the next.
    The values come in as the "survival" vector, a Numpy array.
    They replace values in the m matrix in the diagonal from
    [1,0] to [N-1,N-2].
    """
    if (survival.shape[0] == (self.stAges - 1)):
      for ii in range(1,self.stAges):
        self.m[ii,ii-1] = survival[ii-1]
      # Save it in the object
      self.survival = survival
    else:
      print("Mismatch in size: %s vs. %s" % (self.stAges - 1,survival.shape[0]))

  def LM_AddRecurrence(self,recur):
    """
    Add the values for survival of organisms remaining in the same
    stage. This is for stage-structured population models only.
    The input is as the vector recur, and its values replace those
    in the m matrix along the main diagonal from [1,1] to [N-1,N-1].
    """
    if (recur.shape[0] == (self.stAges - 1)):
      for ii in range(1,self.stAges):
        self.m[ii,ii] = recur[ii-1]
      # Save it in the object
      self.recurrence = recur
    else:
      print("Mismatch in size: %s vs. %s" % (self.stAges - 1,recur.shape[0]))

  def LM_SetOneRelation(self,fromState,toState, value):
    """
    Method to set a relation that does not fall on the survival
    diagonal or the recurrence diagonal. This is useful for more
    complex stage-structured population modeling where organisms
    from one stage may graduate to multiple other stages at defined
    rates.
    """
    iv = interval.Interval.between(0,self.stAges-1)
    if ((fromState in iv) and (toState in iv)):
      # print(self.m)
      self.m[toState,fromState] = value
      # print(self.m)

  def LM_SetPopulation(self,popvector):
    """
    Another central feature of these models is that the size
    of the population is kept in a 1xN column vector. For the
    implementation here, the actual representation is as a
    Numpy array, which has no column vector as such. This will
    be handled in the actual stepping method.
    """
    if (popvector.shape[0] == (self.stAges)):
      self.popvec = popvector
    else:
      print("Mismatch in size: %s vs. %s" % (self.stAges,popvector.shape[0]))

  def LM_StepForward(self):
    """
    Do the matrix multiplication to obtain the new population
    vector. Retain the previous population vector.

    Handle turning population vector into a column vector for the
    multiplication.
    """
    # Convert the population array to a Numpy matrix and transpose it
    # to get the column vector we need. Multiply the L* matrix by
    # the column vector, resulting in a new column vector with the
    # population at the next step.
    nextpopvec = num.mat(self.m) * num.mat(self.popvec).T

    # Save the old population vector
    self.lastpopvec = self.popvec

    # Replace the population vector with the new one, which means
    # transposing it and converting to Numpy array type
    self.popvec = num.array(nextpopvec.T)

    # Track the number of steps taken
    self.step += 1

  def LM_TotalPopulation(self):
    """
    Return the total population size. Sums the "popvec" vector.
    """
    if (0 < len(self.popvec)):

      # Population vector as array multiplied by column vector of 1s is a sum
      t = num.mat(self.popvec) * ones(self.stAges).T

      return t[0,0]
    else:
      return 0.0

if __name__ == "__main__":
  """
  Generic initialization suggested at
  http://www.scipy.org/NumPy_for_Matlab_Users
  """
  # Make all numpy available via shorter 'num' prefix
  import numpy as num
  # Make all matlib functions accessible at the top level via M.func()
  import numpy.matlib as M
  # Make some matlib functions accessible directly at the top level via, e.g. rand(3,3)
  from numpy.matlib import rand,zeros,ones,empty,eye
  # Define a Hermitian function
  def hermitian(A, **kwargs):
    return num.transpose(A,**kwargs).conj()

  # Make some shorcuts for transpose,hermitian:
  # num.transpose(A) -> T(A)
  # hermitian(A) -> H(A)
  T = num.transpose
  H = hermitian

  import interval

  # Check it against an existing example data set
  # http://www.cnr.uidaho.edu/wlf448/Leslie1.htm

  ex1 = LMatrix(4)

  fex1 = num.array([0.5, 2.4, 1.0, 0.0])
  ex1.LM_AddFecundity(fex1)

  sex1 = num.array([0.5, 0.8, 0.5])
  ex1.LM_AddSurvival(sex1)

  pex1 = num.array([20, 10, 40, 30])
  ex1.LM_SetPopulation(pex1)

  print(pex1)
  print(ex1.m)
  ex1.LM_StepForward()
  print(ex1.popvec)

  # It checks out!

  # Another example, this time of a stage-structured population
  # http://www.afrc.uamont.edu/whited/Population%20projection%20models.pdf
  ex2 = LMatrix(3)

  fex2 = num.array([0.0, 52, 279.5])
  ex2.LM_AddFecundity(fex2)

  sex2 = num.array([0.024, 0.08])
  ex2.LM_AddSurvival(sex2)

  rex2 = num.array([0.25, 0.43])
  ex2.LM_AddRecurrence(rex2)

  pex2 = num.array([70.0,20.0,10.0])
  ex2.LM_SetPopulation(pex2)

  print(pex2)
  print(ex2.m)
  ex2.LM_StepForward()
  print(ex2.popvec)
  print(ex2.LM_TotalPopulation())

  ex2.LM_StepForward()
  print(ex2.LM_TotalPopulation())

  ex2.LM_StepForward()
  print(ex2.LM_TotalPopulation())

  for ii in range(22):
    ex2.LM_StepForward()
    print(ex2.popvec)

  # Tests OK!

"""
Output from the standalone run:

[20 10 40 30]
[[ 0.5 2.4 1. 0. ]
[ 0.5 0. 0. 0. ]
[ 0. 0.8 0. 0. ]
[ 0. 0. 0.5 0. ]]
[[ 74. 10. 8. 20.]]
[ 70. 20. 10.]
[[ 0.00000000e+00 5.20000000e+01 2.79500000e+02]
[ 2.40000000e-02 2.50000000e-01 0.00000000e+00]
[ 0.00000000e+00 8.00000000e-02 4.30000000e-01]]
[[ 3835. 6.68 5.9 ]]
3847.58
2093.1914
5811.535142
[[ 19837904.89838918 393232.36554185 30519.85368983]]
"""
