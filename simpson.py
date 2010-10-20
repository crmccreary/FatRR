"""
Closed Simpson's rule for 
    \int_a^b f(x) dx
Divide [a,b] iteratively into h, h/2, h/4, h/8, ... step sizes; and,
for each step size, evaluate f(x) at a+h, a+3h, a+5h, a+7h, ..., b-3h,
b-h, noting that other points have already been sampled.

At each iteration step, data are sampled only where necessary so that
the total data is represented by adding sampled points from all
previous steps:
    step 1:	h	a---------------b
    step 2:	h/2 	a-------^-------b
    step 3:	h/4	a---^-------^---b
    step 4:	h/8	a-^---^---^---^-b
    total:		a-^-^-^-^-^-^-^-b
So, for step size of h/n, there are n intervals, and the data are
sampled at the boundaries including the 2 end points.

If old = Trapezoid formula for an old step size 2h, then Trapezoid
formula for the new step size h is obtained by 
    new = old/2 + h{f(a+h) + f(a+3h) + f(a+5h) + f(a+7h) +...+ f(b-3h)
	+ f(b-h)}
Also, Simpson formula for the new step size h is given by
    simpson = (4 new - old)/3
"""
def close_enough(u, v, TOL):
    if abs(u-v) <= TOL*abs(u) and abs(u-v) <= TOL*abs(v):
        return True
    else:
        return False
    
def closedpoints(func, a, b, TOL=1e-6): # f(x)=func(x)
    h = b - a
    old2 = old = h * (func(a) + func(b)) / 2.0
    count = 0
    while 1:
        h = h / 2.0
        x, sum = a + h, 0
        while x < b:
            sum = sum + func(x)
            x = x + 2 * h
        new = old / 2.0 + h * sum
        new2 = (4 * new - old) / 3.0
        if abs(new2 - old2) < TOL * (1 + abs(old2)) and count > 4: return new2
        old = new # Trapezoid
        old2 = new2 # Simpson
        count = count + 1
        #print 'closedpoints(%d): Trapezoid=%s, Simpson=%s' % (count, new, new2)

