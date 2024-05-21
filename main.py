from functools import total_ordering

types = {
  0: 1,
  1: 0,
  2: 2,
  3: 1,
  4: 1,
  5: 1,
  6: 3,
}

typedescs = {
  0: "constant value",
  1: "identity",
  2: "sum",
  3: "exponential",
  4: "cardinal successor",
  5: "N-type",
  6: "Psi",
}

argnames = {
  0: "value",
  2: "summand, addend",
  3: "exponent",
  4: "input",
  5: "shrconf",
  6: "collapser, input, shrconf"
}

class AT:
  def __init__(self, type: int, **kwargs):
    self.type = type
    self.inps = kwargs.copy()
    if self.type not in types:
      raise Exception("Type not in range 0-6.")
    elif len(self.inps) != types[self.type]:
      raise Exception(f"Type {self.type} ({typedescs[self.type]} arithmetic term) takes exactly {types[self.type]} arguments.")
    elif ", ".join(list(self.inps.keys())) != argnames[self.type]:
      raise Exception(f"Type {self.type} ({typedescs[self.type]} arithmetic term)'s arguments must be \"{argnames[self.type]}\".")
  def copy(self):
    return AT(self.type, **self.inps)
  def __repr__(self):
    return str(self)
  def __str__(self):
    match self.type:
      case 0:
        return str(self.inps["value"])
      case 1:
        return "t"
      case 2:
        return str(self.inps["summand"]) + " + " + str(self.inps["addend"])
      case 3:
        return "ω^{" + str(self.inps["exponent"]) + "}"
      case 4:
        return str(self.inps["input"]) + "^+"
      case 5:
        return "N(" + str(self.inps["shrconf"]) + ")"
      case 6:
        return "Ψ_{" + str(self.inps["collapser"]) + "}^{" + str(self.inps["shrconf"]) + "}(" + str(self.inps["input"]) + ")"
      case _:
        raise Exception("Arithmetic term could not be stringified.")

class ME:
  def __init__(self, **kwargs):
    if kwargs == {}:
      self.conj = []
      self.term = None
      self.inp = None
      self.iters = 0
    else:
      if "conj" in kwargs:
        self.conj = kwargs["conj"]
      else:
        self.conj = []
      if "term" in kwargs:
        self.term = kwargs["term"]
      else:
        raise Exception(f"ME constructor argument \"term\" missing.")
      if "inp" in kwargs:
        self.inp = kwargs["inp"]
      else:
        self.inp = ME().copy()
      if "iters" in kwargs:
        self.iters = kwargs["iters"]
      else:
        self.iters = 1
  def copy(self):
    return ME(conj=self.conj, term=self.term, inp=self.inp, iters=self.iters)

class Ordinal:
  def __init__(self, type: int, **kwargs):
    pass
