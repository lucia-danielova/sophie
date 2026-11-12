from __future__ import annotations

from typing import Dict, List, Tuple


def to_bool(value: int) -> bool:
    return bool(value)


def gate_truth_table(gate: str, inputs: List[int]) -> Dict[str, object]:
    gate_name = gate.upper()
    if len(inputs) == 0:
        inputs = [0, 0]

    def bit(value: bool) -> int:
        return 1 if value else 0

    def and_gate(values: List[bool]) -> bool:
        return all(values)

    def or_gate(values: List[bool]) -> bool:
        return any(values)

    def xor_gate(values: List[bool]) -> bool:
        return sum(1 for v in values if v) % 2 == 1

    def nand_gate(values: List[bool]) -> bool:
        return not and_gate(values)

    def nor_gate(values: List[bool]) -> bool:
        return not or_gate(values)

    def not_gate(values: List[bool]) -> bool:
        return not values[0] if values else False

    handlers = {
        "AND": and_gate,
        "OR": or_gate,
        "XOR": xor_gate,
        "NAND": nand_gate,
        "NOR": nor_gate,
        "NOT": not_gate,
    }

    if gate_name not in handlers:
        raise ValueError(f"Unsupported gate: {gate_name}")

    rows = []
    for combination in range(1 << max(len(inputs), 1)):
        row_inputs = [bool((combination >> index) & 1) for index in range(len(inputs))]
        result = handlers[gate_name](row_inputs)
        rows.append({
            "input": row_inputs,
            "output": bit(result),
            "label": " | ".join(str(bit(v)) for v in row_inputs),
        })

    return {
        "gate": gate_name,
        "input_count": len(inputs),
        "rows": rows,
        "result": handlers[gate_name]([to_bool(v) for v in inputs]),
    }


def comparator_math(signal: int, threshold: int) -> Dict[str, object]:
    if signal < 0 or threshold < 0:
        raise ValueError("Signal and threshold must be non-negative integers.")

    output = 1 if signal >= threshold else 0
    return {
        "signal": signal,
        "threshold": threshold,
        "output": output,
        "comparison": "HIGH" if output else "LOW",
        "excess": signal - threshold,
    }


def timing_summary(repeater_delay_ticks: int, pulses: int, period_ticks: int | None = None) -> Dict[str, object]:
    if repeater_delay_ticks < 1:
        raise ValueError("Repeater delay must be at least 1 tick.")

    total_delay = repeater_delay_ticks * pulses
    cycle_time = period_ticks if period_ticks is not None else total_delay
    return {
        "repeater_delay_ticks": repeater_delay_ticks,
        "pulses": pulses,
        "total_delay_ticks": total_delay,
        "period_ticks": cycle_time,
        "notes": "Use equal branch lengths for synchronized output routing.",
    }


def farm_plan(farm_type: str) -> Dict[str, object]:
    plans = {
        "mob": {
            "name": "Mob grinder",
            "layout": "Compact kill chamber with direct chute collection and a low-entity-density processing corridor.",
            "throughput": "High, but keep active entities below the cap to avoid cramming.",
            "notes": [
                "Use a tight kill box and a short drop route.",
                "Keep the collection lane under active item throughput without excess mob stacking.",
                "Use a short hopper line to reduce churn and chunk stress.",
            ],
        },
        "iron": {
            "name": "Iron farm",
            "layout": "Center the spawning platform on a capped but dense village core, then route iron golems through a compact kill + collection tunnel.",
            "throughput": "Optimized for steady iron output with minimal entity pileups.",
            "notes": [
                "Use a village center and a forced spawn surface only where it is still within the valid radius.",
                "Limit active golem count to avoid extremely sparse chunk load spikes.",
                "Maintain a direct, short drop line to prevent item pile stagnation.",
            ],
        },
        "gold": {
            "name": "Gold farm",
            "layout": "Dense piglin-capable platform with strong kill geometry and immediate collection routing.",
            "throughput": "Very high if the platform is capped correctly.",
            "notes": [
                "Keep the piglin cap controlled to avoid excessive whip-through and lag spikes.",
                "Shorten the loot path to maximize item retention and reduce entity pile delay.",
            ],
        },
        "villager": {
            "name": "Villager breeder",
            "layout": "Use a compact breeding box with controlled food input and a short overflow path to avoid cramming.",
            "throughput": "Stable and efficient if the breeding box remains well-ventilated and compact.",
            "notes": [
                "Feed in a disciplined rhythm to avoid stack bottlenecks.",
                "Keep the breeding area small and clean to preserve movement and reduce pathing drift.",
            ],
        },
        "crop": {
            "name": "Crop farm",
            "layout": "Short, dense hydration and bonemeal cycle with direct collection routing.",
            "throughput": "High for compact crop layouts with minimal chunk activation.",
            "notes": [
                "Use compact row spacing to minimize pathing and update churn.",
                "Avoid overlong collection lanes or stale item storage in the active region.",
            ],
        },
    }

    if farm_type.lower() not in plans:
        raise ValueError(f"Unsupported farm type: {farm_type}")

    return plans[farm_type.lower()]
