from random import choices

if __name__ == '__main__':
    population = [1, 2, 3, 4, 5, 6]
    weights = [0.1, 0.05, 0.05, 0.2, 0.4, 0.2]
    print(choices(population, weights))