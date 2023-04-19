from collections import defaultdict, deque


def parse(puzzle: str) -> dict[int, set[int]]:
    parsed: dict[int, set[int]] = defaultdict(set)
    with open(puzzle) as file:
        for line in file.readlines():
            h, _, *t = line.replace(',', ' ').split()
            head = int(h)
            tail = [int(n) for n in t]
            parsed[head] = set(tail)
            for node in parsed[head]:
                parsed[node].add(head)
    return parsed


def count_nodes(graph: dict[int, set[int]], entry_node: int) -> int:
    nodes_count = 0
    visited: dict[int, bool] = {k: False for k in graph}
    queue: deque[int] = deque([entry_node])
    while len(queue):
        node = queue.popleft()
        if visited[node]:
            continue
        nodes_count += 1
        visited[node] = True
        for child in graph[node]:
            if not visited[child]:
                queue.append(child)
    return nodes_count


def count_groups(graph) -> int:
    groups_count = 0
    visited: dict[int, bool] = {k: False for k in graph}
    for entry_node in visited:
        if visited[entry_node]:
            continue
        groups_count += 1
        queue: deque[int] = deque([entry_node])
        while len(queue):
            node = queue.popleft()
            if visited[node]:
                continue
            visited[node] = True
            for child in graph[node]:
                if not visited[child]:
                    queue.append(child)

    return groups_count


def main(puzzle: str, label: str, expected: tuple[int, int] | None = None) -> None:
    graph = parse(puzzle)
    nodes = count_nodes(graph, entry_node=0)
    groups = count_groups(graph)
    print(f'part 1 {label:.^8} = {nodes}{(", shall be " + str(expected[0])) if expected else ""}')
    print(f'part 2 {label:.^8} = {groups}{(", shall be " + str(expected[1])) if expected else ""}')


if __name__ == '__main__':
    print("-" * 40)
    main("test.txt", "test", expected=(6, 2))
    print("-" * 40)
    main("puzzle.txt", "solution", expected=(141, 171))
    print("=" * 40)
