from multiprocessing import Pool
from anc import f


with Pool(5) as p:
        print(p.map(f, [1, 2, 3,4,7]))