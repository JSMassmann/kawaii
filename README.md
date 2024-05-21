# kawaii
A Python library for handling ordinals up to, almost, the proof-theoretic ordinal of Π12-comprehension.

Done so far:

- Constructor, copying and stringification methods for <code>AT</code> class.

To do:

- Create <code>ME</code> class (subclass of <code>tuple</code>) and <code>V: ME -> set</code> method.
- Create (distinct) stringification and representation methods for <code>ME</code> class.
- Improve stringification method for <code>AT</code> class.
- Create <code>Ordinal</code> class with copying, stringification and comparison methods.
- Add stricter typing to class constructors to ensure bad stuff doesn't happen.

The library is based off of my OCF which reaches up to n-fold stability for finite n (but not quite nonprojectibility, i.e. limits of ω-fold stables). We have three classes:

- <code>AT</code>. These are arithmetic terms: they encode a function on ordinals built up from constants, identities, x,y -> x+y, x -> w^x, x -> x^+, N and Psi. These are used for denoting the degree of stability, e.g. "a that is a^+-stable".
- <code>ME</code>. These are shrewdness encoding, representing a combination of thinning operators, or a "nice" sequence of these, e.g. x -> x-fold iterated Pi_2. These are bundled into one by allowing <code>self.iters</code> etc. to be not only an <code>Ordinal</code> but also an <code>AT</code>.
- <code>Ordinal</code>. The actual things being encoded here.

There's a fair bit of recursive interplay between the three classes, but it's not turtles all the way down since it all "bottoms out".
