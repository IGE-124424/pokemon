'''
Cria um sistema Fuzzy que recebe como input a diferença dos niveis
e o efeito do ataque e devolve como output a probabilidade de ganhar
'''

def calculate_prob(level_input, effect_input):

    # definir os conjuntos fuzzy
    low = {-5:1, -4:1, -3:0.7, -2:0.4, -1:0.2, 0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
    equal = {-5:0, -4:0, -3:0, -2:0.3, -1:0.7, 0:1, 1:0.7, 2:0.3, 3:0, 4:0, 5:0}
    high = {-5:0, -4:0, -3:0, -2:0, -1:0, 0:0, 1:0.2, 2:0.4, 3:0.7, 4:1, 5:1}

    # definir os conjuntos fuzzy para o efeito do ataque (corrigido)
    weak = {0:1, 0.25:1, 0.5:0.8, 1:0.3, 2:0, 4:0}
    normal = {0:0, 0.25:0.2, 0.5:0.7, 1:1, 2:0.5, 4:0}
    strong = {0:0, 0.25:0, 0.5:0.1, 1:0.4, 2:0.9, 4:1}

    # definir os conjuntos fuzzy para a probabilidade de ganhar
    lose = {0:1, 0.25:0.7, 0.5:0.2, 0.75:0, 1:0}
    maybe = {0:0, 0.25:0.5, 0.5:1, 0.75:0.5, 1:0}
    win = {0:0, 0.25:0, 0.5:0.3, 0.75:0.8, 1:1}

    # fuzzificação
    def mu(set_dic, value):

        keys = sorted(set_dic.keys())

        if value <= keys[0]:
            return set_dic[keys[0]]

        for i in range(len(keys)-1):
            if keys[i] <= value <= keys[i+1]:
                return set_dic[keys[i]]

        return set_dic[keys[-1]]

    # calcular os graus de pertinência
    level_low = mu(low, level_input)
    level_equal = mu(equal, level_input)
    level_high = mu(high, level_input)

    effect_weak = mu(weak, effect_input)
    effect_normal = mu(normal, effect_input)
    effect_strong = mu(strong, effect_input)

    # regras fuzzy (AND = min)
    r1 = min(level_low, effect_weak)
    r2 = min(level_low, effect_normal)
    r3 = min(level_equal, effect_normal)
    r4 = min(level_high, effect_strong)
    r5 = min(level_high, effect_normal)

    # truncate
    def truncate(set_dic, q):
        return {x:min(v,q) for x,v in set_dic.items()}

    out1 = truncate(lose, r1)
    out2 = truncate(maybe, max(r2, r3))
    out3 = truncate(win, max(r4, r5))

    # agregação (max)
    combined = {}

    for x in lose:
        combined[x] = max(
            out1.get(x,0),
            out2.get(x,0),
            out3.get(x,0)
        )

    # defuzzificação (centroide)
    num = sum(x*v for x,v in combined.items())
    den = sum(v for v in combined.values())

    if den == 0:
        return 0

    return num / den