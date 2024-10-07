from multiprocessing import Pool

def worker(x, y):
    return x + y

if __name__ == '__main__':
    with Pool(4) as p:
        results = p.starmap(worker, [(x, y) for x in range(10) for y in range(10)])
        print(results)
