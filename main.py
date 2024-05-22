from functools import total_ordering

types = {
  0: 1,
  1: 0,
  2: 2,
  3: 1,
  4: 1,
  5: 3,
}

typedescs = {
  0: "constant value",
  1: "identity",
  2: "sum",
  3: "cardinal successor",
  4: "N-type",
  5: "Psi",
}

argnames = {
  0: "value",
  2: "summand, addend",
  3: "input",
  4: "shrconf",
  5: "collapser, input, shrconf"
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
    # Some monotonous typechecking
    if self.type == 0 and not isinstance(self.inps["value"], Ordinal):
      raise Exception("Type 0 (constant value arithmetic term)'s input must be an ordinal.")
    elif self.type == 2 and not isinstance(self.inps["summand"], AT) or not isinstance(self.inps["addend"], AT):
      raise Exception("Type 2 (sum arithmetic term)'s inputs must be arithmetic terms.")
    elif self.type == 3 and not isinstance(self.inps["input"], AT):
      raise Exception("Type 3 (cardinal successor arithmetic term)'s input must be an arithmetic term.")
    elif self.type == 4 and not isinstance(self.inps["shrconf"], ME):
      raise Exception("Type 4 (N-type arithmetic term)'s input must be a shrewdness encoding.")
    elif self.type == 5 and not isinstance(self.inps["collapser"], AT) or not isinstance(self.inps["input"], AT):
      raise Exception("Type 5 (Psi arithmetic term)'s collapser and inputs must be arithmetic terms.")
    elif self.type == 5 and not isinstance(self.inps["shrconf"], ME):
      raise Exception("Type 5 (Psi arithmetic term)'s input must be a shrewdness encoding.")
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
        if self.inps["input"].type == 3:
          i = len(str(self.inps["input"]))-1
          noo = False
          while str(self.inps["input"])[i] != "^":
            i -= 1
            if str(self.inps["input"])[i] == "{":
              noo = True
              break
          plusstr = str(self.inps["input"])[i+1:] if not noo else str(self.inps["input"])[i+1:-1]
          return str(self.inps["input"])[:i+1] + ["{",""][int(noo)] + plusstr + "+}")
        else:
          return str(self.inps["input"]) + "^+"
      case 4:
        return "N(" + str(self.inps["shrconf"]) + ")"
      case 5:
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

ordtypes = {
  0: 0,
  1: 2,
  2: 1,
  3: 3
}

ordtypedescs = {
  0: "zero",
  2: "sum",
  3: "N",
  4: "Psi"
}

ordargnames = {
  2: "summand, addend",
  3: "input",
  4: "collapser, input, shrconf"
}

@total_ordering
class Ordinal:
  def __init__(self, type: int, **kwargs):
    self.type = type
    self.inps = kwargs.copy()
    if self.type not in ordtypes:
      raise Exception("Type not in range 0-3.")
    elif len(self.inps) != ordtypes[self.type]:
      raise Exception(f"Type {self.type} ({ordtypedescs[self.type]} ordinal) takes exactly {ordtypes[self.type]} arguments.")
    elif ", ".join(list(self.inps.keys())) != ordargnames[self.type]:
      raise Exception(f"Type {self.type} ({ordtypedescs[self.type]} ordinal)'s arguments must be \"{ordargnames[self.type]}\".")
  def copy(self):
    return AT(self.type, **self.inps)
  def __repr__(self):
    return str(self)
  def __str__(self):
    
