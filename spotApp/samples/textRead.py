while True:
    f = open('lockState.txt', 'r')

    data = f.read()

    f.close()

    print(data)