"""
0/1 Knapsack Algorithm Implementation for Emergency Supply Selection
Uses Dynamic Programming with O(nW) time and space complexity.
"""

from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class Supply:
    """Represents an emergency supply item."""
    name: str
    weight: int
    priority: int

    def __post_init__(self):
        if self.weight < 0:
            raise ValueError("Weight cannot be negative")
        if self.priority < 0:
            raise ValueError("Priority cannot be negative")


@dataclass
class KnapsackResult:
    """Result of the knapsack computation."""
    selected_items: List[Supply]
    total_weight: int
    total_priority: int
    dp_table: List[List[int]]
    decision_path: List[Tuple[int, int]]  # (item_index, decision) where decision: 1=selected, 0=not selected


class KnapsackSolver:
    """
    0/1 Knapsack solver using Dynamic Programming.

    Time Complexity: O(n * W)
    Space Complexity: O(n * W)
    where n = number of items, W = capacity
    """

    def __init__(self):
        self.supplies: List[Supply] = []
        self.capacity: int = 0

    def set_supplies(self, supplies: List[Supply]) -> None:
        """Set the list of available supplies."""
        self.supplies = supplies

    def set_capacity(self, capacity: int) -> None:
        """Set the maximum capacity."""
        if capacity < 0:
            raise ValueError("Capacity cannot be negative")
        self.capacity = capacity

    def solve(self) -> KnapsackResult:
        """
        Solve the 0/1 Knapsack problem using Dynamic Programming.

        Returns:
            KnapsackResult containing selected items, totals, DP table, and decision path.
        """
        n = len(self.supplies)
        W = self.capacity

        # Create DP table: (n+1) x (W+1)
        # dp[i][w] = maximum priority value using first i items with capacity w
        dp = [[0] * (W + 1) for _ in range(n + 1)]

        # Fill DP table
        for i in range(1, n + 1):
            item = self.supplies[i - 1]
            for w in range(W + 1):
                # Don't take the item
                dp[i][w] = dp[i - 1][w]

                # Take the item if it fits and gives better value
                if item.weight <= w:
                    value_with_item = dp[i - 1][w - item.weight] + item.priority
                    if value_with_item > dp[i][w]:
                        dp[i][w] = value_with_item

        # Trace back to find selected items
        selected = []
        total_weight = 0
        w = W
        decision_path = []

        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                # Item was selected
                item = self.supplies[i - 1]
                selected.append(item)
                total_weight += item.weight
                w -= item.weight
                decision_path.append((i - 1, 1))  # 1 = selected
            else:
                decision_path.append((i - 1, 0))  # 0 = not selected

        # Reverse to get original order
        selected.reverse()
        decision_path.reverse()

        total_priority = dp[n][W]

        return KnapsackResult(
            selected_items=selected,
            total_weight=total_weight,
            total_priority=total_priority,
            dp_table=dp,
            decision_path=decision_path
        )

    def get_step_by_step_explanation(self, result: KnapsackResult) -> List[str]:
        """Generate step-by-step explanation of the algorithm execution."""
        steps = []
        n = len(self.supplies)
        W = self.capacity
        dp = result.dp_table

        steps.append("=" * 60)
        steps.append("0/1 KNAPSACK ALGORITHM - STEP BY STEP EXECUTION")
        steps.append("=" * 60)
        steps.append(f"Number of supplies: {n}")
        steps.append(f"Vehicle capacity: {W} kg")
        steps.append("")

        steps.append("DYNAMIC PROGRAMMING TABLE CONSTRUCTION:")
        steps.append("-" * 40)
        steps.append(f"DP Table dimensions: ({n+1}) rows × ({W+1}) columns")
        steps.append("dp[i][w] = max priority using first i items with capacity w")
        steps.append("")

        # Show table header
        header = "     " + "  ".join(f"{w:3d}" for w in range(W + 1))
        steps.append("Capacity (w): " + header)
        steps.append("Items (i):")

        for i in range(n + 1):
            if i == 0:
                row_label = "  0  "
            else:
                item = self.supplies[i - 1]
                row_label = f" {i:2d} "
            row = "  ".join(f"{dp[i][w]:3d}" for w in range(W + 1))
            steps.append(f"{row_label}  {row}")

        steps.append("")
        steps.append("TRACEBACK - FINDING SELECTED ITEMS:")
        steps.append("-" * 40)

        w = W
        for i in range(n, 0, -1):
            item = self.supplies[i - 1]
            if dp[i][w] != dp[i - 1][w]:
                steps.append(f"Item {i}: {item.name} (weight={item.weight}, priority={item.priority})")
                steps.append(f"  → SELECTED: dp[{i}][{w}] = {dp[i][w]} ≠ dp[{i-1}][{w}] = {dp[i-1][w]}")
                w -= item.weight
            else:
                steps.append(f"Item {i}: {item.name} (weight={item.weight}, priority={item.priority})")
                steps.append(f"  → NOT SELECTED: dp[{i}][{w}] = {dp[i][w]} = dp[{i-1}][{w}] = {dp[i-1][w]}")

        steps.append("")
        steps.append("FINAL RESULT:")
        steps.append("-" * 40)
        steps.append(f"Selected supplies: {len(result.selected_items)}")
        for item in result.selected_items:
            steps.append(f"  • {item.name}: {item.weight} kg, priority {item.priority}")
        steps.append(f"Total weight: {result.total_weight} kg / {W} kg")
        steps.append(f"Total priority value: {result.total_priority}")
        steps.append(f"Remaining capacity: {W - result.total_weight} kg")

        return steps


def demo():
    """Demo function to test the knapsack solver."""
    solver = KnapsackSolver()

    # Example from the project description
    supplies = [
        Supply("First-aid kit", 5, 10),
        Supply("Food packets", 8, 12),
        Supply("Water bottles", 6, 8),
        Supply("Emergency medicine", 3, 9),
        Supply("Blanket", 7, 7),
    ]

    solver.set_supplies(supplies)
    solver.set_capacity(20)

    result = solver.solve()
    steps = solver.get_step_by_step_explanation(result)

    for step in steps:
        print(step)


if __name__ == "__main__":
    demo()