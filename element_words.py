import csv

table = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F',
         'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl',
         'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn',
         'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As',
         'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb',
         'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In',
         'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La',
         'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb',
         'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta',
         'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl',
         'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac',
         'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk',
         'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db',
         'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh',
         'Fl', 'Mc', 'Lv', 'Ts', 'Og']

def recursive(word, elementised_word=''):
    """Check if a word can be made allowing repeat elements"""
    if len(word) == 0:#Completed, go back up the stack
        return elementised_word
    for i in table:
        if i.lower() == word[:len(i)]:#If the element matches the start of the remaining letters
            new_word = recursive(word[len(i):], elementised_word+i)#Recursively call the function with values taken off the word
            if new_word:#If not false then the word is found, send it back up the stack
                return new_word
    else:#If the loop completes without breaking then the word cannot be made with the elements used so far
        return False

def recursive_no_repeats(table, word, elementised_word=''):
    """Check if a word can be made without repeating an element"""
    if len(word) == 0:#Completed, go back up the stack
        return elementised_word
    for i in table:
        if i.lower() == word[:len(i)]:#If the element matches the start of the remaining letters
            new_table = table[:]
            new_table.remove(i)#remove that element from a copy of the table
            new_word = recursive_no_repeats(new_table, word[len(i):], elementised_word+i)#Recursively call the function with values taken off the word
            if new_word:#If not false then the word is found, send it back up the stack
                return new_word
    else:#If the loop completes without breaking then the word cannot be made with the elements used so far
        return False                   

print(recursive('metal'))
