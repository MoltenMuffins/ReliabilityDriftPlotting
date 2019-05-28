import multiprocessing

def worker(num1, num2):
    """Thread worker function. This function takes two numbers and sums them up"""
    print("The sum of values is:", num1 + num2)
    return


def another_func():
    """This function initiates a multiprocessing call when this function is called."""
    # Parameters to input into function
    num1 = [x/3 for x in range(100)]
    num2 = [x*(2/3) for x in range(100)]

    # Create a list of jobs

    print("Multiprocessing Beginning:")

    for i, j in zip(num1, num2):
        # The target function should be the name of the function you want to call in parallel
        # without the brackets ()
        # arguments should be passed as (something,something,)
        p = multiprocessing.Process(target=worker, args=(i, j))
        p.start()


if __name__ == "__main__":
    another_func()

