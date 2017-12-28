# simple commands
+ 1 2
- 2 1
# functions
plus = fn a b: + a b
plus 1 4
# saving variables
y = 10
+ y 20
applyFn = fn f : f 5 6
applyFn +
c = fn f x: f x
plusFive = fn x: + x 5
c plusFive 6;
