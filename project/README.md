# HY-487                |   Project-PhaseA
## Stivaktakis Giorgos  |   csd4300

### Question 1 comments

Depth-First Nature: DFS explores as far down a path as it can before backtracking. This means it doesn't necessarily take the shortest route to the goal; it takes the first route it finds to the goal.

Path Length: In a maze, the first path DFS finds to the goal can be much longer than the shortest path. The algorithm doesn't consider the length or cost of the path while exploring.

Successor Order: The order in which successors are explored can significantly affect the solution path length. DFS doesn't differentiate between a short path or a long one; it just keeps exploring down one branch until it can't go any further.

Lack of Optimization: DFS is not optimized for finding the shortest path; it's optimized for space (using less memory) and finding a path, any path, to the goal. In contrast, algorithms like Breadth-First Search (BFS) or A* are designed to find the shortest or least-cost path.

In your case, getting a path length of 130 or 246 indicates that DFS is working as expected, exploring paths thoroughly but not necessarily efficiently in terms of path length. To find the least-cost solution, you would need to use a different algorithm like Uniform Cost Search (UCS) or A*, which consider the cost or length of the path in their search strategy.

### Question 2 comments