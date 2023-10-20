import sys
from simulator import Simulator


def main():
    if len(sys.argv) != 9:
        print(
            "Usage: python sim_cache.py <BLOCKSIZE> <L1_SIZE> <L1_ASSOC> <L2_SIZE> <L2_ASSOC> <REPLACEMENT_POLICY> <INCLUSION_PROPERTY> <trace_file>"
        )
        return

    block_size = int(sys.argv[1])
    l1_size = int(sys.argv[2])
    l1_assoc = int(sys.argv[3])
    l2_size = int(sys.argv[4])
    l2_assoc = int(sys.argv[5])
    replacement_policy = int(sys.argv[6])
    inclusion_property = int(sys.argv[7])
    trace_file = sys.argv[8]

    simulator = Simulator(
        block_size=block_size,
        l1_size=l1_size,
        l1_assoc=l1_assoc,
        l2_size=l2_size,
        l2_assoc=l2_assoc,
        replacement_policy=replacement_policy,
        inclusion_property=inclusion_property,
        trace_file=trace_file,
    )

    simulator.create_caches()
    simulator.run()
    simulator.print_results()


if __name__ == "__main__":
    main()
