import multiprocessing

def worker(num):
    """thread worker function"""
    print('Worker:', num)
    return

def another_func():
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()

if __name__ == '__main__':
    another_func()