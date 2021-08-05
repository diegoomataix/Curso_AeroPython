# Ley d'Hondt

def hondt(votes, n):
    """ Ley d'Hondt; coefficient: c_i = V_i / (s_i + 1) 
        V_i = total number of votes obtained by party i
        s_i = number of seats assigned to party i (initially 0)
    """
    s = [0] * len(votes)
    for i in range(n):
        c = [v[j] / (s[j] + 1) for j in range(len(s))]
        s[c.index(max(c))] += 1
    return s

# Example
v = [340000, 280000, 160000, 60000, 15000] # votes for each party
n = 155 # number of seats
print(hondt(v, n))