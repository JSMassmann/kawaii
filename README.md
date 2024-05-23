# kawaii
A Python library for handling ordinals up to, almost, the proof-theoretic ordinal of Π12-comprehension.

Done so far:

- Constructor, copying and stringification methods for <code>AT</code>, <code>ME</code> and <code>Ordinal</code> classes.
- Recursive <code>V: ME -> list</code> method.
- Recursive <code>cnf: Ordinal -> list</code> method.

To do:

- More sugar for <code>Ordinal</code> stringification.
- Comparison methods for <code>Ordinal</code> class.
- Add stricter typing to <code>Ordinal</code> constructors to ensure bad stuff doesn't happen.
- Arithmetic, e.g. addition, for <code>Ordinal</code> class.

The library is based off of my OCF which reaches up to n-fold stability for finite n (but not quite nonprojectibility, i.e. limits of ω-fold stables). We have three classes:

- <code>AT</code>. These are arithmetic terms: they encode a function on ordinals built up from constants, identities, x,y -> x+y, x -> w^x, x -> x^+, N and Psi. These are used for denoting the degree of stability, e.g. "a that is a^+-stable".
- <code>ME</code>. These are shrewdness encodings, representing a combination of thinning operators, or a "nice" sequence of these, e.g. x -> x-fold iterated Pi_2. These are bundled into one by allowing <code>self.iters</code> etc. to be not only an <code>Ordinal</code> but also an <code>AT</code>.
- <code>Ordinal</code>. The actual things being encoded here.

There's a fair bit of recursive interplay between the three classes, but it's not turtles all the way down since it all "bottoms out".
