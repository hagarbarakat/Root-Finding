from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Treeview
from sympy import *
from sympy import sympify
from math import *
import time
import matplotlib
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use("TkAgg")


replacements = {
    'sin' : 'np.sin',
    'cos' : 'np.cos',
    'exp': 'np.exp',
    'log' : 'np.log',
    '^': '**',
}


def load():
    filename = filedialog.askopenfilename(initialdir="/", title="select file", filetypes=(("text files", "*.txt"), ("all files", "*.*")))
    print(filename)
    f = open(filename, "r")
    equ = f.readline()
    print(equ)
    eqEntry.delete(0, END)
    eqEntry.insert(0, equ)


def rep(user_expr):
    if user_expr.find("e^x") > -1:
        user_expr = user_expr.replace("e^x", "exp(x)")
    if user_expr.find("e^-x") > -1:
        user_expr = user_expr.replace("e^-x", "exp(-x)")
    if user_expr.find("ln(x)"):
        user_expr = user_expr.replace("ln(x)", "log(x)")
    if user_expr.find("x^"):
        user_expr = user_expr.replace("x^", "x**")
    print(user_expr)
    #result = eval(user_expr)
    #print("Result = {}".format(result))
    return user_expr



def f():
    equationStr = str(eqEntry.get())
    newequation = ""
    equationStr = rep(equationStr)
    for j in range(len(equationStr)):
        if equationStr[j] == '^':
            newequation += "**"
        else:
            newequation += equationStr[j]
            try:
                if equationStr[j].isdigit() and equationStr[j + 1].isalpha():
                    newequation += "*"
            except IndexError:
                continue
    print(newequation)
    return newequation


def g():
    equationStr = str(gxEq.get())
    newequation = ""
    equationStr = rep(equationStr)
    for j in range(len(equationStr)):
        if equationStr[j] == '^':
            newequation += "**"
        else:
            newequation += equationStr[j]
            try:
                if equationStr[j].isdigit() and equationStr[j + 1].isalpha():
                    newequation += "*"
            except IndexError:
                continue
    print(newequation)
    return newequation


def func(x):
    equationStr = str(eqEntry.get())
    newequation = ""
    equationStr = rep(equationStr)
    for j in range(len(equationStr)):
        if equationStr[j] == '^':
            newequation += "**"
        else:
            newequation += equationStr[j]
            try:
                if equationStr[j].isdigit() and equationStr[j+1].isalpha():
                   newequation += "*"
            except IndexError:
                continue
    print(newequation)
    try:
        return eval(newequation)
    except ZeroDivisionError:
        notFound.config(text="Divide by zero error for f(x)")


def gfunc(x):
    equationStr = str(gxEq.get())
    newequation = ""
    equationStr = rep(equationStr)
    for j in range(len(equationStr)):
        if equationStr[j] == '^':
            newequation += "**"
        else:
            newequation += equationStr[j]
            try:
                if equationStr[j].isdigit() and equationStr[j + 1].isalpha():
                    newequation += "*"
            except IndexError:
                continue
    print(newequation)
    try:
        return eval(newequation)
    except ZeroDivisionError:
        notFound.config(text="Divide by zero error for g(x)")


def f_prime(number):
    x = Symbol('x')
    s = f()
    expr = sympify(s)
    fprime = expr.diff(x)
    print(fprime)
    try:
        print("evaaal", fprime.evalf(subs={x: number}))
        return fprime.evalf(subs={x: number})
    except ZeroDivisionError:
        notFound.config(text="Divide by zero error for f'(x)")


def g_prime(number):
    x = Symbol('x')
    s = g()
    expr = sympify(s)
    print("equaton ",expr)
    fprime = expr.diff(x)
    print(fprime)

    try:
        print("evaaal", fprime.evalf(subs={x: number}))
        return fprime.evalf(subs={x: number})
    except ZeroDivisionError:
        notFound.config(text="Divide by zero error for g'(x)")




def singlestep():
    if func(float(initialEntry.get()))*func(float(secondEntry.get())) < 0:
        bi(float(initialEntry.get()), float(secondEntry.get()), 1,0)


def s(string):
    for old, new in replacements.items():
        string = string.replace(old, new)
    print(string)
    return string


def bi(a,b,counter, acc):
    window.update()
    window.deiconify()
    buttona= Button(window,text="Single Step",command=lambda : bi(a,b,counter+1,acc))
    buttona.grid(row=1, column=0)
    figure = Figure(figsize=(6,5), dpi=100)
    plot = figure.add_subplot(1, 1, 1)
    canvas = FigureCanvasTkAgg(figure, window)
    canvas.get_tk_widget().grid(row=0, column=0)
    fun = f()
    n = s(fun)
    f2s = np.vectorize(n)
    x = np.array(range(int(a)-2, int(b)+2))
    y = eval(n)
    print(y)
    c = (a + b) / 2
    e = accuracy(c,acc)
    plot.vlines(a, 1, 10, linestyles="dotted",color='g', linewidth=2)
    plot.vlines(b, 1, 10, linestyles="dotted", color='y', linewidth=2)
    plot.vlines(c, 1, 10, linestyles="dotted", color='b', linewidth=2)
    plot.plot(a, func(a), color="g", marker="o", linestyle="")
    plot.plot(b, func(b), color="y", marker="o", linestyle="")
    plot.plot(c, func(c), color="b", marker="o", linestyle="")
    if counter < int(maxEntry.get()) and e > float(prEntry.get()):
        buttona.config(state="normal")
        if func(c) == 0:
            buttona.config(state="disabled")
        if func(c) * func(a) < 0:
            buttona.config(state="normal")
            b = c
        else:
            buttona.config(state="normal")
            a = c
    else:
            buttona.config(state= "disabled")
    plot.plot(x, y, color="blue")
    winiterations.config(text="Iteration = " + str(counter))
    winmaxiterations.config(text="Maximium number of Iterations = "+maxEntry.get())
    xr.config(text="Root = " + str(c))
    acc = c



def bisection(a, b):
    clear()
    secondEntry.config(state="normal")
    start = time.time()
    e= float(prEntry.get())
    if func(a) * func(b) >= 0:
        wrong = "You have not assumed right a and b"
        notFound.config(text=wrong)
        print("You have not assumed right a and b\n")
        return
    acc = 0
    c = 0
    x = 0
    if str(maxEntry.get()) != "":
      i = int(maxEntry.get())
    else:
        i = 50
    count = 1
    while i > 0 and e < accuracy(c,x):
        x = c
        i = i - 1
        c = (a + b) / 2
        result.insert('', count-1, text=str(count), values=(str(a), str(b), str(c), str(func(a)), str(func(b)),
                                                            str(func(c)), accuracy(c, x)), open=True)
        count = count + 1
        acc= accuracy(c,x)
        if func(c) == 0.0:
            break

        # Decide the side to repeat the steps
        if func(c) * func(a) < 0:
            b = c
            print("change in xu")
            print("xu", b)

        else:
            a = c
            print("change in xl")
            print("xl", a)
    end = time.time()
    print("The value of root is : ", "%.4f" % c)
    labelresult.config(text="Root = " + str(c))
    times.config(text="Time = "+ str(end-start))
    iterations.config(text="Number of Iterations = " + str(count-1))
    accuarcy.config(text="Accuracy = "+str(acc))



def regulafalsi(a, b):
    clear()
    secondEntry.config(state="normal")
    start = time.time()
    if func(a) * func(b) >= 0:
        wrong = "You have not assumed right a and b"
        notFound.config(text=wrong)
        print("You have not assumed right a and b")
        return -1
    i = 0
    e = float(prEntry.get())
    c = 0  # Initialize result
    x = 0
    acc = 0
    if int(maxEntry.get()) != "":
      MAX_ITER = int(maxEntry.get())
    else:
        MAX_ITER = 50
    while i < MAX_ITER and e < accuracy(c, x):
        x = c
        print("xxxxxx", x)
        # Find the point that touches x axis
        print(i)
        print('f(xl)->', func(a))
        print('f(xu)->', func(b))
        c = (a * func(b) - b * func(a)) / (func(b) - func(a))
        result.insert('', i+1, text=str(i+1), values=(str(a), str(b), str(c), str(func(a)), str(func(b)), str(func(c)),
                                                      accuracy(c, x)), open=True)
        print('xr -> ', c)
        acc= accuracy(c,x)
        # Check if the above found point is root
        if func(c) == 0:
            break

        # Decide the side to repeat the steps
        elif func(c) * func(a) < 0:
            b = c
            print('xu-> ', b)
        else:
            a = c
            print('xl-> ', a)
        i=i+1
    end= time.time()
    print("The value of root is : ", '%.4f' % c)
    labelresult.config(text="Root = " + str(c))
    times.config(text="Time =  "+ str(end-start))
    iterations.config(text="Number of Iterations = " + str(i))
    accuarcy.config(text="Accuracy = " + str(acc))


def accuracy(current, previous):
    if current == 0:
        x = 100
    else:
        x = abs((current-previous)/current)
    print("accur", x)
    return x


def fixedPoint(gfunc,  approx, tol, n):
    clear()
    secondEntry.config(state="disabled")
    start = time.time()
    if abs(g_prime(approx)) >= 1:
        notFound.config(text="Converges")
    else:
        i = 0
        p = 0
        e = float(prEntry.get())
        while i < n:
            print(approx)
            p = gfunc(approx)
            print("P", p)
            x = accuracy(p, approx)
            result.insert('', i + 1, text=str(i+1), values=(str(p), str(x)), open=True)
            i=i+1
            if abs(x) < tol:
                print("p<tol", p)
                end = time.time()
                times.config(text="Time =  " + str(end - start))
                labelresult.config(text="Root = " + str(p))
                iterations.config(text="Number of Iterations = " + str(i))
                accuarcy.config(text="Accuracy = " + str(x))
                return p
            approx = p
        end = time.time()
        times.config(text="Time =  " + str(end - start))
        labelresult.config(text="Root = " + str(p))
        iterations.config(text="Number of Iterations = " + str(i))
        accuarcy.config(text="Accuracy = " + str(x))
    #return notFound.config(text="Method failed after {} iterations".format(n))


def newtons(approx, tol, n):
    clear()
    secondEntry.config(state="disabled")
    start = time.time()
    p0 = approx
    i=0
    while i < n:
        p = p0 - (func(p0)/f_prime(p0))  # this is the calculation of the guess
        print("p", p)
        x = accuracy(p, p0)
        result.insert('', i+1, text=str(i+1), values=(str(p), str(x)), open=True)
        i = i + 1
        if accuracy(p, p0) < tol:
            end = time.time()
            times.config(text="Time =  " + str(end - start))
            iterations.config(text="Number of Iterations = " + str(i))
            accuarcy.config(text="Accuracy = " + str(x))
            print("<tol", p)
            labelresult.config(text="Root = " + str(p))
            return p
        p0 = p
    return notFound.config(text="Method failed after {} iterations".format(n))


def secant(f, a, b, N):
    clear()
    start = time.time()
    if f(a)*f(b) >= 0:
        print("Secant method fails.")
        notFound.config(text="Secant method fails.")
        return None
    x1 = a
    x2 = b
    m_n=0
    x=0
    n=0
    c=a
    while n < N:
        m_n = x1 - f(x1)*(x2 - x1)/(f(x2) - f(x1))
        print("current= ", m_n)
        x = accuracy(m_n,c)
        print("accuracy = ", x)
        result.insert('', n, text=str(n+1), values=(str(x2), str(x1),str(m_n), str(f(x2)), str(f(x1)), str(f(m_n)),
                                                      str(x)), open=True)
        f_m_n = f(m_n)
        c=m_n
        n=n+1
        x2 = x1
        x1=m_n
        if f_m_n == 0:
            end = time.time()
            print("The value of root is : ", '%.4f' % m_n)
            times.config(text="Time =  " + str(end - start))
            labelresult.config(text="Root = " + str(m_n))
            iterations.config(text="Number of Iterations = " + str(n))
            accuarcy.config(text="Accuracy = " + str(x))
            print("Found exact solution.")
            return m_n
        if x < float(prEntry.get()):
            break


    end = time.time()
    print("The value of root is : ", '%.4f' % m_n)
    times.config(text="Time =  "+ str(end-start))
    labelresult.config(text="Root = " + str(m_n))
    iterations.config(text="Number of Iterations = " + str(n))
    accuarcy.config(text="Accuracy = " + str(x))


def clear():
    accuarcy.config(text="")
    times.config(text="")
    notFound.config(text="")
    labelresult.config(text="")
    iterations.config(text="")

def sel():

    first = initialEntry.get()
    second = secondEntry.get()
    if var.get() == 1:
        result.delete(*result.get_children())
        bisection(float(first), float(second))
        singlestep()
    elif var.get() == 2:
        result.delete(*result.get_children())
        regulafalsi(float(first), float(second))
    elif var.get() == 3:
        result.delete(*result.get_children())
        fixedPoint(gfunc, float(first), float(prEntry.get()), int(maxEntry.get()))
    elif var.get() == 4:
        result.delete(*result.get_children())
        newtons(float(first), float(prEntry.get()), int(maxEntry.get()))
    elif var.get() == 5:
        result.delete(*result.get_children())
        secant(func, float(first), float(second), int(maxEntry.get()))

def change():
    result.delete(*result.get_children())
    if var.get() == 3:
        gxEq.config(state="normal")

    else:
        gxEq.config(state="disabled")
    secondEntry.config(state="disabled")
    result.column("#0", width=80, minwidth=270, stretch=NO)
    result.column("one", width=300, minwidth=150, stretch=NO)
    result.column("two", width=445, minwidth=0)
    result.column("three", width=0, minwidth=0, stretch=NO)
    result.column("four", width=0, minwidth=0, stretch=NO)
    result.column("five", width=0, minwidth=0, stretch=NO)
    result.column("six", width=0, minwidth=0, stretch=NO)
    result.column("seven", width=0, minwidth=0, stretch=NO)
    result.heading("#0", text="Iteration", anchor=CENTER)
    result.heading("one", text="xi", anchor=CENTER)
    result.heading("two", text="εa", anchor=CENTER)
    result.grid(row=7, column=0, columnspan=5, sticky="ns", padx=(10, 0), pady=10)
    scroll = Scrollbar(root)
    scroll.grid(row=7, column=5, sticky="nse", pady=10)  # set this to column=2 so it sits in the correct spot.
    scroll.configure(command=result.yview)
    result.configure(yscrollcommand=scroll.set)

def restore():
    result.delete(*result.get_children())
    secondEntry.config(state="normal")
    gxEq.config(state="disabled")
    result.column("#0", width=70, minwidth=70, stretch=NO)
    result.column("one", width=100, minwidth=150, stretch=NO)
    result.column("two", width=100, minwidth=200)
    result.column("three", width=100, minwidth=50, stretch=NO)
    result.column("four", width=100, minwidth=50, stretch=NO)
    result.column("five", width=100, minwidth=50, stretch=NO)
    result.column("six", width=100, minwidth=50, stretch=NO)
    result.column("seven", width=150, minwidth=50, stretch=NO)
    if var.get() != 5:
        result.heading("#0", text="Iteration", anchor=W)
        result.heading("one", text="xl", anchor=W)
        result.heading("two", text="xu", anchor=W)
        result.heading("three", text="xr", anchor=W)
        result.heading("four", text="f(xl)", anchor=W)
        result.heading("five", text="f(xu)", anchor=W)
        result.heading("six", text="f(xr)", anchor=W)
        result.heading("seven", text="εa", anchor=W)
        result.grid(row=7, column=0, columnspan=5, sticky="ns", padx=(10, 0), pady=10)
    else:
        result.heading("#0", text="Iteration", anchor=W)
        result.heading("one", text="x2", anchor=W)
        result.heading("two", text="x1", anchor=W)
        result.heading("three", text="xr", anchor=W)
        result.heading("four", text="f(x2)", anchor=W)
        result.heading("five", text="f(x1)", anchor=W)
        result.heading("six", text="f(xr)", anchor=W)
        result.heading("seven", text="εa", anchor=W)
        result.grid(row=7, column=0, columnspan=5, sticky="ns", padx=(10, 0), pady=10)


root = Tk()
root.title("Root Finding")
menu = Menu(root)
root.config(menu=menu)
submenu = Menu(menu)
menu.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open File", command=load)
equation = Label(root, text="Equation")
equation.grid(row=2, sticky=W)
gx= Label(root, text="G(x)")
gx.grid(row=2, column=3)
gxEq= Entry(root)
gxEq.grid(row=2,column=4)
eqEntry = Entry(root)
eqEntry.grid(row=2, column=1)
precision=Label(root, text="Precision")
initialGuess= Label(root,text="First point of interval - Point")
initialGuess.grid(row=3, sticky=W)
initialEntry= Entry(root)
initialEntry.grid(row=3,column=1)
secondGuess=Label(root,text="Second point of interval")
secondGuess.grid(row=3, column=3)
secondEntry= Entry(root)
secondEntry.grid(row=3,column=4)
precision.grid(row=4, sticky=W)
prEntry= Entry(root)
prEntry.grid(row=4, column=1)
maxIteration = Label(root,text="Maximum number of Iterations")
maxIteration.grid(row=4, column=3)
maxEntry = Entry(root)
maxEntry.grid(row=4, column=4)
select= Button(root, text="Select", padx=10, pady=3, command=sel)
select.grid(row=6, column=4, sticky= E)
var = IntVar()
R1 = Radiobutton(root, text="Bisection Method", variable=var, value=1,command=restore)
R1.grid(row=5, sticky= W)
R2 = Radiobutton(root, text="Regula Falsi", variable=var, value=2,command=restore)
R2.grid(row=5, column=1)
R3 = Radiobutton(root, text="Fixed Iterative", variable=var, value=3, command=change)
R3.grid(row=5, column=2)
R4 = Radiobutton(root, text="Newton Raphson", variable=var, value=4, command= change)
R4.grid(row=5, column=3)
R5 = Radiobutton(root, text="Secant Method", variable=var, value=5,command=restore)
R5.grid(row=5, column=4)
result = Treeview(root)
result["columns"] = ("one", "two", "three", "four", "five", "six", "seven")
restore()
scroll = Scrollbar(root)
scroll.grid(row=7, column=5, sticky="nse", pady=10)
scroll.configure(command=result.yview)
scrollhoriz=Scrollbar(root,orient=HORIZONTAL)
scrollhoriz.grid(row=7, column=0, columnspan=5, sticky="sew", padx=(10, 0))
scrollhoriz.config(command=result.xview)
result.configure(yscrollcommand=scroll.set,xscrollcommand=scrollhoriz.set)
notFound = Label(root)
notFound.grid(row=9,column=0, sticky=W, padx=(20, 0))
labelresult= Label(root)
labelresult.grid(row=9, column=0, sticky=W, padx=(10, 0))
times = Label(root)
times.grid(row=9, column=2, sticky=W, padx=(10, 0))
iterations = Label(root)
iterations.grid(row=10, column=0, sticky=W, padx=(10, 0))
accuarcy = Label(root)
accuarcy.grid(row=10, column=2, sticky=W, padx=(10, 0))
root.geometry("850x450")
window = Tk()
winiterations= Label(window)
winiterations.grid(row=3, column=0)
winmaxiterations= Label(window)
winmaxiterations.grid(row=4, column=0)
xr= Label(window)
xr.grid(row=7, column=0)
window.withdraw()
root.mainloop()