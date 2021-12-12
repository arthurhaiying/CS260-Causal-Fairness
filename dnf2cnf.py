from os import name
import sys

from sympy.core.symbol import Symbol


####################################################################################################
# Method 1: Tseitin algorithm which may introduce auxiliary variables
####################################################################################################
def flatter(lst):
    x = []
    for i in lst:
        abs_lst = [abs(j) for j in i]
        x.extend(abs_lst)
    return x

def Tseitin(dnf):
    maxi = max(flatter(dnf))
    next = maxi + 1
    ans=[]
    for i in dnf:
        ans.append([-1*i[j] for j in range(len(i))]+[next])
        for j in i:
            ans.append([j,-1*next])
        next += 1
    return ans

############################################################################################
# Method 2: Sympy library to_cnf()
############################################################################################

from sympy import symbols
from sympy.logic.boolalg import And, Or, Not
from sympy.logic.boolalg import to_cnf

def make_expression(dnf):
    # create symbols
    var_to_symbol = {}
    for term in dnf:
        for var in term:
            var = -var if var < 0 else var
            if var not in var_to_symbol:
                # new variable
                name = 'x%d' % var
                x = symbols(name)
                var_to_symbol[var] = x

    # make And expr from term
    def make_term(term):
        args = []
        for var in term:
            if var > 0: # positive literal
                x = var_to_symbol[var]
                args.append(x)
            else: # negative literal
                var = -var
                x = var_to_symbol[var]
                args.append(Not(x))

        return And(*args)

    # make dnf expression
    args = []
    for term in dnf:
        arg = make_term(term)
        args.append(arg)
    
    dnf_expr = Or(*args)
    return dnf_expr, var_to_symbol

def convert_cnf_to_list(cnf_expr, var_to_symbol):
    symbol_to_var = {v:k for k,v in var_to_symbol.items()}
    # build symbol -> var dict
    def is_literal(x):
        return isinstance(x, Not) or isinstance(x, Symbol)
    def is_clause(clause):
        return isinstance(clause, Or)

    def convert_literal(x):
        if isinstance(x, Symbol):
            var = symbol_to_var[x]
            return var
        elif isinstance(x, Not):
            assert len(x.args) == 1
            var = symbol_to_var[x.args[0]]
            return -var
        else:
            raise RuntimeError("{} is not literal!".format(x))

    def convert_clause(clause):
        l = []
        for x in clause.args:
            var = convert_literal(x)
            l.append(var)
        return l


    cnf2 = [] # list representation for cnf
    for arg in cnf_expr.args:
        if is_literal(arg):
            var = convert_literal(arg)
            cnf2.append([var])
        elif is_clause(arg):
            l = convert_clause(arg)
            cnf2.append(l)
        else:
            raise ValueError("Bad CNF!")

    return cnf2

def dnf2cnf(dnf):
    dnf_expr, var_to_symbol = make_expression(dnf)
    cnf_expr = to_cnf(dnf_expr, simplify=True)
    cnf = convert_cnf_to_list(cnf_expr, var_to_symbol)
    return cnf




if __name__ == '__main__':
    dnf = [[1,2], [-3]]
    dnf_expr, var_to_symbol = make_expression(dnf)
    print("dnf: ", dnf)
    print("dnf expr: ", dnf_expr)
    cnf_expr = to_cnf(dnf_expr, simplify=True)
    print("cnf expr: ", cnf_expr)
    cnf2 = convert_cnf_to_list(cnf_expr, var_to_symbol)
    print("cnf2: ", cnf2)
    




    
            

  