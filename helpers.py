def bar_to_Pa(p):
    '''Converts pressure (gauge) from bar to Pa'''
    return 100000*p

def bar_to_kPa(p):
    '''Converts pressure (gauge) from bar to kPa'''
    return 10*p

def kw_to_tr(kilowatt):
    '''Converts power from kilowatt to refrigeration ton'''
    return kilowatt/3.51685