from functools import total_ordering
import re

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
  1: "",
  2: "summand, addend",
  3: "arg",
  4: "shrconf",
  5: "collapser, arg, shrconf"
}

def strsucc(string): # Stringification for successor ordinals. When the input is itself a successor, it searches to find a ^ or {.
  i = len(string)-1
  noo = False
  while string[i] != "^":
    i -= 1
    if string[i] == "{":
      noo = True
      break
  plusstr = string[i+1:] if not noo else string[i+1:-1]
  return string[:i+1] + ["{",""][int(noo)] + plusstr + "+}"

def listunion(l1,l2): # Union of lists, because sets can't contain custom objects (unless we have __hash__, but that's not possible either)
  new = l1.copy()
  for e in l2:
    if e in new:
      pass
    else:
      new.append(e)
  return new

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
    if self.type == 1:
        pass
    elif self.type == 0 and not isinstance(self.inps["value"], Ordinal):
      raise Exception("Type 0 (constant value arithmetic term)'s input must be an ordinal.")
    elif self.type == 2 and (not isinstance(self.inps["summand"], AT) or not isinstance(self.inps["addend"], AT)):
      raise Exception("Type 2 (sum arithmetic term)'s inputs must be arithmetic terms.")
    elif self.type == 3 and not isinstance(self.inps["arg"], AT):
      raise Exception("Type 3 (cardinal successor arithmetic term)'s input must be an arithmetic term.")
    elif self.type == 4 and not isinstance(self.inps["shrconf"], ME):
      raise Exception("Type 4 (N-type arithmetic term)'s input must be a shrewdness encoding.")
    elif self.type == 5 and (not isinstance(self.inps["collapser"], AT) or not isinstance(self.inps["arg"], AT)):
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
        return str(self.inps["summand"]) + "+" + str(self.inps["addend"])
      case 3:
        if self.inps["arg"].type == 3:
          return strsucc(str(self.inps["arg"]))
        else:
          return str(self.inps["arg"]) + "^+"
      case 4:
        return "N(" + str(self.inps["shrconf"]) + ")"
      case 5:
        return "Ψ_{" + str(self.inps["collapser"]) + "}^{" + str(self.inps["shrconf"]) + "}(" + str(self.inps["arg"]) + ")"
      case _:
        raise Exception("Arithmetic term could not be stringified.")

class ME:
  def __init__(self, **kwargs):
    if kwargs == {}:
      self.conj = []
      self.term = None
      self.arg = None
      self.iters = 0 # This is the only time iters will be an int. We use type(X.iters) is int rather than X.int == 0 because the latter tries to invoke __eq__, which can't compare against non-ordinal objects.
    else:
      if "conj" in kwargs:
        self.conj = kwargs["conj"]
      else:
        self.conj = []
      if "term" in kwargs:
        self.term = kwargs["term"]
      else:
        raise Exception(f"ME constructor argument \"term\" missing.")
      if "arg" in kwargs:
        self.arg = kwargs["arg"]
      else:
        self.arg = ME().copy()
      if "iters" in kwargs and kwargs["iters"] != 0:
        self.iters = kwargs["iters"]
      else:
        raise Exception(f"ME constructor argument \"iters\" missing or zero.")
      # More monotonous typechecking!
      if type(self.iters) is int:
        pass
      elif not isinstance(self.conj, list):
        raise Exception("Conjunctions of a shrewdness encoding must be formatted as a list.")
      elif not isinstance(self.term, AT):
        raise Exception("Term of a shrewdness encoding must be an arithmetic term.")
      elif not isinstance(self.arg, ME):
        raise Exception("Argument of a shrewdness encoding must be another shrewdness encoding.")
      elif not isinstance(self.iters, Ordinal):
        raise Exception("Iterations of a shrewdness encoding must be an ordinal.")
  def copy(self):
    return ME(conj=self.conj, term=self.term, arg=self.arg, iters=self.iters)
  def __repr__(self):
    return str(self)
  def __str__(self):
    if type(self.iters) is int:
      return "∅"
    else:
      return f"({str(self.conj)}, {self.term}, {self.arg}, {self.iters})"
  def V(self):
    if type(self.iters) is int:
      return []
    else:
      out = []
      for k in self.conj:
        out = listunion(out, k.V())
      out = listunion(out, self.arg.V())
      return listunion(out, [self.iters])

ordtypes = {
  0: 0,
  1: 2,
  2: 1,
  3: 1,
  4: 3
}

ordtypedescs = {
  0: "zero",
  1: "sum",
  2: "cardinal successor",
  3: "N",
  4: "Psi"
}

ordargnames = {
  0: "",
  1: "summand, addend",
  2: "arg",
  3: "shrconf",
  4: "collapser, arg, shrconf"
}

def sugar(string): # Add sugar to stringified ordinals, e.g. 1+1 = 2
  # Initial replacements
  out = string.replace("Ψ_{0^+}^{∅}(0)", "1")
  out = out.replace("Ψ_{0^+}^{∅}(1)", "ω")
  # Natural numbers
  x = re.search("\d+\+\d+", out)
  while x != None:
    su = int(x.group().split("+")[0])
    ad = int(x.group().split("+")[1])
    out = out.replace(f"{su}+{ad}", str(su+ad))
    x = re.search("\d+\+\d+", out)
  return out

@total_ordering
class Ordinal:
  def __init__(self, type: int, **kwargs):
    self.type = type
    self.inps = kwargs.copy()
    if self.type not in ordtypes:
      raise Exception("Type not in range 0-4.")
    elif len(self.inps) != ordtypes[self.type]:
      raise Exception(f"Type {self.type} ({ordtypedescs[self.type]} ordinal) takes exactly {ordtypes[self.type]} arguments.")
    elif ", ".join(list(self.inps.keys())) != ordargnames[self.type]:
      raise Exception(f"Type {self.type} ({ordtypedescs[self.type]} ordinal)'s arguments must be \"{ordargnames[self.type]}\".")
  def copy(self):
    return AT(self.type, **self.inps)
  def __repr__(self):
    return str(self)
  def __str__(self):
    match self.type:
      case 0:
        return "0"
      case 1:
        out = f"{str(self.inps["summand"])}+{str(self.inps["addend"])}"
      case 2:
        if self.inps["arg"].type == 2:
          out = strsucc(str(self.inps["arg"]))
        else:
          out = f"{str(self.inps["arg"])}^+"
      case 3:
        out = f"N({str(self.inps["shrconf"])})"
      case 4:
        out = "Ψ_{" + str(self.inps["collapser"]) + "}^{" + str(self.inps["shrconf"]) + "}(" + str(self.inps["arg"]) + ")"
      case _:
        raise Exception("Ordinal could not be stringified.")
    return sugar(out)
  def cnf(self) -> list:
    match self.type:
      case 0:
        return []
      case 1:
        return self.inps["summand"].cnf() + self.inps["addend"].cnf()
      case 2:
        return [self.copy()]
      case 3:
        if type(comparand.inps["shrconf"]) is int:
          return []
        else:
          return [self.copy()]
      case 4:
        return [self.copy()]
  def __le__(self, comparand) -> bool: # Implicitly assumes terms involving anything in type 1 are CNF, which simplifies a big deal and is not too stringent in practical use.
    match self.type:
      case 0:
        return True
      case 1:
        if comparand.type == 0:
          return False
        elif comparand.type == 1:
          return self.inps["summand"].__le__(comparand.inps["summand"])
        else:
          return self.inps["summand"].__le__(comparand)
      case 2:
        if comparand.type == 0:
          return False
        elif comparand.type == 1:
          return self.__le__(comparand.inps["summand"])
        elif comparand.type == 2:
          return self.inps["arg"].__le__(comparand.inps["arg"])
        elif comparand.type == 3 and type(comparand.inps["shrconf"].iters) is int:
          return False
        else:
          return self.inps["arg"].__le__(comparand)
      case 3:
        if comparand.type == 0:
          return False
        elif comparand.type == 1:
          return self.__le__(comparand.inps["summand"])
        elif comparand.type == 2:
          return self.__le__(comparand.inps["arg"])
        elif comparand.type == 3:
          raise Exception("Comparison for these ordinals currently unsupported.")
        else:
          return True
      case 4:
        if comparand.type == 0:
          return False
        elif comparand.type == 1:
          return self.__le__(comparand.inps["summand"])
        elif comparand.type == 2:
          return self.__le__(comparand.inps["arg"])
        else:
          raise Exception("Comparison for these ordinals currently unsupported.")
  def __eq__(self, comparand) -> bool:
    match self.type:
      case 0:
        return True if comparand.type == 0 or (comparand.type == 3 and type(comparand.inps["shrconf"].iters) is int) else False
      case 1:
        return True if comparand.type == 1 and self.cnf() == comparand.cnf() else False
      case 2:
        return True if comparand.type == 2 and self.inps()["arg"] == comparand.inps()["arg"] else False
      case _:
        raise Exception("Comparison for these ordinals currently unsupported.")
