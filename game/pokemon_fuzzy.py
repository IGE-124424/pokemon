import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

'''
Cria um sistema Fuzzy que recebe como input a diferença dos niveis
e o efeito do ataque e devolve como input a probabilidade de ganhar
'''

def calculate_prob(level_input, effect_input):

    # ---------- fuzzy sets LEVEL ----------
    low = {-5:1, -4:1, -3:0.7, -2:0.4, -1:0.2, 0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
    equal = {-5:0, -4:0, -3:0, -2:0.3, -1:0.7, 0:1, 1:0.7, 2:0.3, 3:0, 4:0, 5:0}
    high = {-5:0, -4:0, -3:0, -2:0, -1:0, 0:0, 1:0.2, 2:0.4, 3:0.7, 4:1, 5:1}

    # ---------- fuzzy sets EFFECT ----------
    weak = {0:1, 0.5:0.7, 1:0.2, 1.5:0, 2:0}
    normal = {0:0, 0.5:0.5, 1:1, 1.5:0.5, 2:0}
    strong = {0:0, 0.5:0, 1:0.3, 1.5:0.8, 2:1}

    # ---------- fuzzy sets OUTPUT ----------
    lose = {0:1, 0.25:0.7, 0.5:0.2, 0.75:0, 1:0}
    maybe = {0:0, 0.25:0.5, 0.5:1, 0.75:0.5, 1:0}
    win = {0:0, 0.25:0, 0.5:0.3, 0.75:0.8, 1:1}

    # ---------- função pertença ----------
    def mu(set_dic, value):

        keys = sorted(set_dic.keys())

        if value <= keys[0]:
            return set_dic[keys[0]]

        for i in range(len(keys)-1):
            if keys[i] <= value <= keys[i+1]:
                return set_dic[keys[i]]

        return set_dic[keys[-1]]

    # ---------- graus verdade ----------
    q_low = mu(low, level_input)
    q_equal = mu(equal, level_input)
    q_high = mu(high, level_input)

    q_weak = mu(weak, effect_input)
    q_normal = mu(normal, effect_input)
    q_strong = mu(strong, effect_input)

    # ---------- regras (AND = min) ----------
    r1 = min(q_low, q_weak)
    r2 = min(q_low, q_normal)
    r3 = min(q_equal, q_normal)
    r4 = min(q_high, q_strong)
    r5 = min(q_high, q_normal)

    # ---------- truncate ----------
    def truncate(set_dic, q):
        return {x:min(v,q) for x,v in set_dic.items()}

    out1 = truncate(lose, r1)
    out2 = truncate(maybe, max(r2, r3))
    out3 = truncate(win, max(r4, r5))

    # ---------- else-link (max) ----------
    combined = {}

    for x in lose:
        combined[x] = max(
            out1.get(x,0),
            out2.get(x,0),
            out3.get(x,0)
        )

    # ---------- centroid ----------
    num = sum(x*v for x,v in combined.items())
    den = sum(v for v in combined.values())

    if den == 0:
        return 0

    return num / den