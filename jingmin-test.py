
def helper(order, j, X):
    if order == 0:
        return [1]
    rtn = []
    for k in range(j, len(X)):
        # temp = k
        temp_list = helper(order-1, k, X)
        for item in temp_list:
            rtn.append(item * X[k])
    # print(rtn)
    return rtn


if __name__ == '__main__':
    # X = [1,2,3]
    # order = 7
    # rtn = []
    # for i in range(order):
    #     print(helper(i, 0, X))
    import numpy as np
    a = np.array([1,2,3,4])
    b = np.array([1,2,3,4])
    print(np.matmul(np.diag(1/a), b))
    c = np.zeros(4)
    for i in range(4):
        c[i] = a[i]/b[i]
    print(c)