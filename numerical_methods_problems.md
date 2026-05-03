# Numerical Methods Problems

### Sheet 1: Chapter 1 - Solutions of Equations of One Variable

**Bisection Method:**
* 1. Use the bisection method to find solutions accurate to within $10^{-2}$ for $x^{3}-7x^{2}+14x-6=0$ on each of the following intervals: (a) [0, 1], (b) [1, 3.2], (c) [3.2, 4].
* 2. Use the bisection method to find solutions accurate to $10^{-3}$ for $x=\tan x$ on [4, 4.5].
* 3. Use the bisection method to find solutions accurate to $10^{-5}$ for the equation $e^{x}-x^{2}+3x-2=0$ for $0 \le x \le 1$.

**Secant Method:**
* 1. Use the secant method to approximate to within $10^{-4}$ the roots of the following equations: (a) $x^{3}-2x^{2}-5=0$ on [1, 4], (b) $x-\cos x=0$ on $[0, \frac{\pi}{2}]$.
* 2. Use the secant to approximate the solution of the equation $\ln(x-1)+\cos(x-1)=0$ for $1.3 \le x \le 2$.

---

### Sheet 2: Chapter 1 - Solutions of Equations of One Variable

**I. Method of simple iteration:**
* 1. Use the method of simple iteration to find the root to within an accuracy $10^{-5}$ of the equation $0.5x-\sin(x)=0$ using $x_{0}=\frac{\pi}{2}$.
* 2. Use the method of simple iteration to find the root of the equation $x^{3}-7x+1=0$ correct to three decimal places. (Assume $x_{0}=0$).
* 3. Use the method of simple iteration to find the root of the equation $x-\cos(x)=0$ correct to three decimal places. Try $x_{0}=\frac{\pi}{2}$ and then $x_{0}=0$.

**II. The Newton-Raphson Method:**
* 1. Use the Newton-Raphson method to approximate to within $10^{-4}$ the roots of the following equations: a. $x^{3}-2x^{2}-5=0$ on $[1, 4]$, b. $x-0.8-0.2\sin(x)=0$ on $[0, \frac{\pi}{2}]$.

---

### Sheet 3: Chapter 2 - Iterative Solutions of Linear Systems

**I. Exercises on Jacobi and Gauss-Seidel Methods:**
* Apply the Jacobi method and the Gauss-Seidel method to solve each of the following systems to within an accuracy of $10^{-3}$ (if possible), using the initial guess $x^{(0)}=0$:
    * (a) $3x_{1}-x_{2}+x_{3}=1$, $3x_{1}+6x_{2}+2x_{3}=0$, $3x_{1}+3x_{2}+7x_{3}=4$
    * (b) $10x_{1}-x_{2}=9$, $-x_{1}+10x_{2}-2x_{3}=7$, $-2x_{2}+10x_{3}=6$
    * (c) $2x_{1}-2x_{2}+x_{3}+x_{4}=0.8$, $-3x_{2}+0.5x_{3}+x_{4}=-6.6$, $5x_{3}-x_{4}=4.5$, $2x_{4}=3$

---

### Sheet 4: Chapter 3 - Interpolation and Polynomial Approximation

**I. Lagrange's Interpolation:**
* Use the following data to find the highest possible Lagrange's interpolating polynomial representing the following data:
    * (a) $f(1)=0.1924$, $f(1.05)=0.2414$, $f(1.1)=0.2933$, $f(1.15)=0.3492$. Then find the approximate value of $f(1.09)$ if you know that these data represent the function $f(x)=\log_{10}(\tan x)$, and compare your result with the exact one.
    * (b) $f(0.698)=0.7661$, $f(0.768)=0.7193$, $f(0.733)=0.7432$, $f(0.803)=0.6946$. Find the approximate value of $f(0.750)$. If you know that the given data represent the function $f(x)=\cos x$, then the exact value of $f(0.750)=0.7317$; compare this value with your obtained one.
