import time

while True:
    f = open('lockState.txt', 'w')

    f.write('0')

    f.close()

    time.sleep(3)

    f = open('lockState.txt', 'w')

    f.write('1')

    f.close()

    time.sleep(3)