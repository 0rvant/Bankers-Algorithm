P = int(input("Enter the number of processes : "))
R = int(input("Enter the number of resources : "))


def calculateNeed(need, maxm, allot):
    for i in range(P):
        for j in range(R):
            need[i][j] = maxm[i][j] - allot[i][j]

    return need


def isSafe(processes, avail, maxm, allot, need, request_flag):
    if request_flag == 0:
        need = []
        for i in range(P):
            l = []
            for j in range(R):
                l.append(0)
            need.append(l)
        need_mat = calculateNeed(need, maxm, allot)

    elif request_flag == 1:
        need_mat = need

    finish = [0] * P

    safeSeq = [0] * P

    work = [0] * R
    for i in range(R):
        work[i] = avail[i]

    count = 0
    while count < P:

        found = False
        for p in range(P):

            if finish[p] == 0:

                for j in range(R):
                    if need_mat[p][j] > work[j]:
                        break

                if j == R - 1:

                    for k in range(R):
                        work[k] += allot[p][k]

                    safeSeq[count] = p
                    count += 1

                    finish[p] = 1

                    found = True

        if found == False:
            print("No, system is not in safe state.")
            return False
    if request_flag == 0:
        print("Yes, system is in safe state.",
              "\nSafe sequence is: ", end=" ")
        print(*safeSeq)

    elif request_flag == 1:
        print("Yes ,request can be granted.",
              "\nSafe sequence is: ", end=" ")
        print(*safeSeq)

    print("Need Matrix = ", need_mat)

    return True


def request_safe(processes, avail, maxm, allot, requested, process_num):
    need = []
    for i in range(P):
        l = []
        for j in range(R):
            l.append(0)
        need.append(l)
    need = calculateNeed(need, maxm, allot)

    for i in range(P):
        for j in range(R):
            if requested[j] > need[process_num][j]:
                return print("Error, because process has exceeded its maximum claim.")

    for i in range(P):
        for j in range(R):
            if requested[j] > avail[j]:
                return print("Request must wait, since resources are not available.")

    for j in range(R):
        avail[j] -= requested[j]
        allot[process_num][j] += requested[j]
        need[process_num][j] -= requested[j]

    isSafe(processes, avail, maxm, allot, need, request_flag=1)


if __name__ == "__main__":
    processes = []
    for i in range(0, P):
        processes.append(i)

    rows, cols = (P, R)
    maxm = [[0] * cols] * rows
    allot = [[0] * cols] * rows

    for i in range(0, P):
        maxm[i] = (list(map(int, input("Enter the maximum vector for process " + str(i) + " : ").split())))

    for i in range(0, P):
        allot[i] = (list(map(int, input("Enter the allocation vector for process " + str(i) + " : ").split())))

    avail = list(map(int, input("Enter the available resources vector : ").split()))
    isSafe(processes, avail, maxm, allot, need=[], request_flag=0)

    request = input("Do you want to request a process ? (YES/NO) : ")
    if request == "YES":
        process_num = int(input("Enter the number of the request process : "))
        requested = list(map(int, input("Enter the request vector : ").split()))
        request_safe(processes, avail, maxm, allot, requested, process_num)
