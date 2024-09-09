import time

def countDown(t):
    while t > -1:
        print(f"Retrying in {t} seconds")
        t -= 1
    return True