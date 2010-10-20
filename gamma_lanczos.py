# Copyright (c) 2010 the authors listed at the following URL, and/or
# the authors of referenced articles or incorporated external code:
# http://en.literateprograms.org/Gamma_function_with_the_Lanczos_approximation_(Python)?action=history&offset=20090111205238
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
# Retrieved from: http://en.literateprograms.org/Gamma_function_with_the_Lanczos_approximation_(Python)?oldid=15934

from cmath import *

g = 7
lanczos_coef = [ \
     0.99999999999980993,
   676.5203681218851,
 -1259.1392167224028,
   771.32342877765313,
  -176.61502916214059,
    12.507343278686905,
    -0.13857109526572012,
     9.9843695780195716e-6,
     1.5056327351493116e-7]

def gamma(z):
    z = complex(z)
    if z.real < 0.5:
        return pi / (sin(pi*z)*gamma(1-z))
    else:
        z -= 1
        x = lanczos_coef[0] + \
            sum(lanczos_coef[i]/(z+i)
                for i in range(1, g+2))
        t = z + g + 0.5
        return sqrt(2*pi) * t**(z+0.5) * exp(-t) * x

if __name__ == '__main__':
    print gamma(5.81).real
