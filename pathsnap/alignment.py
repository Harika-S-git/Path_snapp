"""Align an ordered route to observations in O(observations × route arcs)."""
import numpy as np
from numba import njit


@njit
def align(distances, progress, steps):
    n, m = distances.shape
    back = np.zeros((n, m), dtype=np.int32)
    scores = distances[0].copy()
    queue = np.empty(m, dtype=np.int32)
    for i in range(1, n):
        old = progress[i - 1]
        lower = scores - .35 * old
        upper = scores + .35 * old
        next_scores = np.empty_like(scores)
        left = -1
        head = tail = 0
        best_lower = np.inf
        best_index = 0
        for j in range(m):
            target = progress[i, j] - steps[i]
            while left < j and old[left + 1] <= target:
                left += 1
                if lower[left] < best_lower:
                    best_lower = lower[left]
                    best_index = left
            while head < tail and queue[head] <= left:
                head += 1
            if j > left:
                while tail > head and upper[queue[tail - 1]] > upper[j]:
                    tail -= 1
                queue[tail] = j
                tail += 1
            cost = best_lower + .35 * target
            index = best_index
            if head < tail:
                alt = upper[queue[head]] - .35 * target
                if alt < cost:
                    cost = alt
                    index = queue[head]
            back[i, j] = index
            next_scores[j] = distances[i, j] + cost
        scores = next_scores
    path = np.empty(n, dtype=np.int32)
    index = scores.argmin()
    for i in range(n - 1, -1, -1):
        path[i] = index
        index = back[i, index]
    return path
