from .ranking import Ranking
from .interleaving_method import InterleavingMethod
import numpy as np

class Balanced(InterleavingMethod):
    '''
    Balanced Interleaving
    '''
    def interleave(self, k, a, b):
        '''
        k: the maximum length of resultant interleaving
        a: a list of document IDs
        b: a list of document IDs

        Return an instance of Ranking
        '''
        is_a_first = np.random.randint(0, 2) == 0
        result = Ranking()
        k_a = 0
        k_b = 0
        while k_a < len(a) and k_b < len(b) and len(result) < k:
            if (k_a < k_b) or (k_a == k_b and is_a_first):
                if not a[k_a] in result:
                    result.append(a[k_a])
                k_a += 1
            else:
                if not b[k_b] in result:
                    result.append(b[k_b])
                k_b += 1
        result.a = a
        result.b = b
        return result

    def evaluate(self, ranking, clicks):
        '''
        ranking: an instance of Ranking generated by Balanced.interleave
        clicks: a list of indices clicked by a user

        Return one of the following tuples:
        - (1, 0): Ranking 'a' won
        - (0, 1): Ranking 'b' won
        - (0, 0): Tie
        '''
        if len(clicks) == 0:
            return (0, 0)
        c_max = np.max(clicks)
        r_max = ranking[c_max]
        k_a = ranking.a.index(r_max) if r_max in ranking.a else len(ranking.a)
        k_b = ranking.b.index(r_max) if r_max in ranking.b else len(ranking.b)
        k = np.min([k_a, k_b])
        h_a = len([c for c in clicks if ranking[c] in ranking.a[:k+1]])
        h_b = len([c for c in clicks if ranking[c] in ranking.b[:k+1]])
        if h_a > h_b:
            return (1, 0)
        elif h_b > h_a:
            return (0, 1)
        else:
            return (0, 0)