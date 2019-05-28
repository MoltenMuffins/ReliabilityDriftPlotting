import time
from multiprocessing import Pool
 
def f(a_list):
    out = 0
    for n in a_list:
        out += n*n
        time.sleep(0.1)
 
    return out
 
def f_mp(a_list):
    chunks = [a_list[i::5] for i in range(5)]
    print(chunks)
    pool = Pool(processes=5)
 
    result = pool.map(f, chunks)
 
    return sum(result)

def main():
    b_list = [x for x in range(100)]
    start = time.time()
    print(f_mp(b_list))
    end = time.time()
    print(end-start)
    start = time.time()
    print(f(b_list))
    end = time.time()
    print(end-start)

if __name__ == '__main__':
    main()
    print('all done?')