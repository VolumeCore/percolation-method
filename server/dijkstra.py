import heapq


class Dijkstra:

    def __init__(self, matrix, start, end):
        self.matrix = matrix
        self.start = start
        self.end = end

    def method(self):
        # преобразуем матрицу в граф
        graph = {}
        rows, cols = len(self.matrix), len(self.matrix[0])
        for i in range(rows):
            for j in range(cols):
                neighbors = []
                if i > 0:
                    neighbors.append([(i - 1, j), 1 if self.matrix[i - 1][j] == 1 else 50000])
                if i < rows - 1:
                    neighbors.append([(i + 1, j), 1 if self.matrix[i + 1][j] == 1 else 50000])
                if j > 0:
                    neighbors.append([(i, j - 1), 1 if self.matrix[i][j - 1] == 1 else 50000])
                if j < cols - 1:
                    neighbors.append([(i, j + 1), 1 if self.matrix[i][j + 1] == 1 else 50000])
                graph[(i, j)] = neighbors

        # инициализируем алгоритм Дейкстры
        queue = [(0, self.start, [])]
        visited = set()
        # алгоритм Дейкстры
        while queue:
            cost, node, path = heapq.heappop(queue)
            if node in visited:
                continue
            if node == self.end:
                return path + [node], cost
            visited.add(node)
            for neighbor in graph[node]:
                heapq.heappush(queue, (cost + neighbor[1], neighbor[0], path + [node]))

        # если не удалось найти путь до конечной вершины
        return None, None
