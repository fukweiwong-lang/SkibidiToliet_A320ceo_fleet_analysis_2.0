import math
from typing import Dict, Tuple

# 1. Data Input Section 
# Frequency
freq = {
    "BEG": 3*2,
    "IST": 2*2,
    "LHR": 1*2,
    "SVO": 2*2,
    "VIE": 2*2,
    "CDG": 1*2,
    "FCO": 1*2
}
# Block Hours
block = {
    "BEG": 1.00,
    "IST": 1.75,
    "LHR": 3.17,
    "SVO": 3.00,
    "VIE": 1.42,
    "CDG": 2.67,
    "FCO": 1.42
}
# Turnaround Time
turnaround = {
    "BEG": 0.50,
    "IST": 0.75,
    "LHR": 1.00,
    "SVO": 1.00,
    "VIE": 0.50,
    "CDG": 0.75,
    "FCO": 0.50
}


# 2. Calculation Functions
def calculate_total_workload(freq: Dict, block: Dict, turnaround: Dict) -> Tuple[float, float]:
    """Calculate Daily Total Block Hours and Total Workload (Block + Turnaround)"""
    total_block = sum(freq[dest] * block[dest] for dest in freq)
    total_workload = total_block + sum(freq[dest] * turnaround[dest] for dest in freq)
    return total_block, total_workload


def optimize_fleet_size(total_workload: float, 
                        util_per_aircraft: float = 8.0) -> int:
    """
    Mathematical Optimization Algorithm: Fleet Size
    
    Function：
        N* = ceil( total_workload / util_per_aircraft )
    
    Parameters:
        total_workload   : Daily Total Workload (hours)
        util_per_aircraft: Available Hours per Aircraft per Day (default 8 hours)
    
    Returns:
        Minimum Optimal Fleet Size
    """
    required = total_workload
    min_fleet = math.ceil(required / util_per_aircraft)
    return min_fleet

def evaluate_fixed_fleet(total_workload: float,
                         fleet_size: int,
                         util_per_aircraft: float = 8.0) -> dict:
    required = total_workload
    capacity = fleet_size * util_per_aircraft
    residual = capacity - required
    actual_util = total_workload / fleet_size if fleet_size > 0 else 0
    return {
        "fleet_size": fleet_size,
        "capacity": capacity,
        "required": required,
        "residual": residual,
        "actual_util": actual_util,
        "is_adequate": residual >= 0
    }

def sensitivity_analysis(total_workload: float, util_range: list = None):
    """Sensitivity Analysis: Test Fleet Requirements under Different Utilization Rates"""
    if util_range is None:
        util_range = [7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
    
    print("\n【Sensitivity Analysis】Minimum Fleet Size under Different Daily Utilization Assumptions:")
    print(f"{'Utilization (h/day)/':<15} {'Minimum Fleet/':<10} {'Residual Capacity (h)':<12}")
    print("-" * 40)
    
    for util in util_range:
        fleet = optimize_fleet_size(total_workload, util_per_aircraft=util)
        residual = fleet * util - total_workload
        print(f"{util:<15.1f} {fleet:<10} {residual:<12.2f}")


# 3. Main Program Execution
if __name__ == "__main__":
    # Calculate Total Workload
    total_block, total_workload = calculate_total_workload(freq, block, turnaround)
    
    print("=" * 50)
    print("A320ceo Fleet Optimization Results")
    print("=" * 50)
    print(f"Daily Total Block Hours     : {total_block:.2f} hours")
    print(f"Daily Total Workload (Block + Turnaround) : {total_workload:.2f} hours")

    # Main Optimization Result (Baseline Assumption: 8 hours/aircraft/day)
    base_util = 8.0
    min_fleet = optimize_fleet_size(total_workload, util_per_aircraft=base_util)
    
    print(f"\n【Optimization Results】")
    print(f"Baseline Utilization Assumption : {base_util} hours/aircraft/day")
    print(f"Minimum Fleet Size (A320ceo)    : {min_fleet} aircraft")
    
    # Calculate Actual Utilization
    actual_util = total_workload / min_fleet
    print(f"Actual Average Utilization      : {actual_util:.2f} hours/aircraft/day")
    
    # Sensitivity Analysis
    sensitivity_analysis(total_workload)

    print("=" * 70)
    print("A320ceo Fleet Optimization Results (Dynamic Comparison)")
    print("=" * 70)

    compare_sizes = [max(1, min_fleet - 1), min_fleet, min_fleet + 1]
    
    results = {}
    for size in compare_sizes:
        results[size] = evaluate_fixed_fleet(total_workload, size, base_util) 
    
    print(f"\n【Dynamic Comparison Table】")
    header = f"{'Item':<32}"
    for size in compare_sizes:
        label = f"{size} Aircraft"
        if size == min_fleet:
            label += " (Recommended)"
        header += f"{label:<22}"
    print(header)
    print("-" * 90)

    # Fleet Size
    row = f"{'Fleet Size':<32}"
    for size in compare_sizes:
        row += f"{results[size]['fleet_size']:<22}"
    print(row)
    
    # Daily Capacity
    row = f"{'Daily Capacity (hours)':<32}"
    for size in compare_sizes:
        row += f"{results[size]['capacity']:<22.2f}"
    print(row)
    
    # Demand
    row = f"{'Demand':<32}"
    for size in compare_sizes:
        row += f"{results[size]['required']:<22.2f}"
    print(row)

    # Residual
    row = f"{'Residual Capacity (hours)':<32}"
    for size in compare_sizes:
        row += f"{results[size]['residual']:+.2f}{'':<16}"
    print(row)

    # Actual Utilization
    row = f"{'Actual Utilization (h/ac/day)':<32}"
    for size in compare_sizes:
        row += f"{results[size]['actual_util']:<22.2f}"
    print(row)
    # Is Adequate
    row = f"{'Is Adequate':<32}"
    for size in compare_sizes:
        status = "Yes" if results[size]['is_adequate'] else "No"
        row += f"{status:<22}"
    print(row)
    
    print("=" * 90)
    print("Programmer: William so tired and Grok/Don't use, copy or even distribute without any permission by William")
    print("=" * 90)