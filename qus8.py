
MOD = 10**9 + 7

n, m = map(int, input().split())
matrix = [input().split() for _ in range(n)]

prev_score = [None] * m
prev_ways = [0] * m

for i in range(n):
    curr_score = [None] * m
    curr_ways = [0] * m

    for j in range(m):
        if matrix[i][j] == "X":
            continue

        value = int(matrix[i][j])

        if i == 0 and j == 0:
            curr_score[j] = value
            curr_ways[j] = 1
            continue

        candidates = []

        if i > 0 and prev_score[j] is not None:
            candidates.append((prev_score[j], prev_ways[j]))

        if j > 0 and curr_score[j - 1] is not None:
            candidates.append((curr_score[j - 1], curr_ways[j - 1]))

        if i > 0 and j > 0 and prev_score[j - 1] is not None:
            candidates.append((prev_score[j - 1], prev_ways[j - 1]))

        if candidates:
            best = max(score for score, ways in candidates)
            curr_score[j] = best + value
            curr_ways[j] = sum(
                ways for score, ways in candidates if score == best
            ) % MOD

    prev_score = curr_score
    prev_ways = curr_ways

if prev_score[m - 1] is None:
    print("IMPOSSIBLE")
else:
    print(prev_score[m - 1], prev_ways[m - 1])
