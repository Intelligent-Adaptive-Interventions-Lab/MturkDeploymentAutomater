
def parse_regression_formuala(formula, include_intercept=True):
    reward = formula.split("~")[0].strip()
    variables = formula.split("~")[1].split(" + ")
    return reward, len(variables) + int(include_intercept)


def create_coefficient_covariance_and_mean_matrix(length):
    matrix = []
    for i in range(length):
        zeros = [0.0] * length
        zeros[i] = 1.0
        matrix.append(zeros)
    return matrix, [0.0]*length

