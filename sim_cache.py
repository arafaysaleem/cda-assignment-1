import sys

from src.caches.cache_heirarchy import CacheHeirarchy


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

    # Print the simulator configuration
    print("===== Simulator configuration =====")
    print(f"BLOCKSIZE:             {block_size}")
    print(f"L1_SIZE:               {l1_size}")
    print(f"L1_ASSOC:              {l1_assoc}")
    print(f"L2_SIZE:               {l2_size}")
    print(f"L2_ASSOC:              {l2_assoc}")
    print(f"REPLACEMENT POLICY:    {'LRU' if replacement_policy == 0 else 'FIFO'}")
    print(
        f"INCLUSION PROPERTY:    {'non-inclusive' if inclusion_property == 0 else 'inclusive'}"
    )
    print(f"trace_file:            {trace_file}")

    # Create the cache heirarchy
    cache_heirarchy = CacheHeirarchy(
        replacement_policy=replacement_policy,
        inclusion_property=inclusion_property,
        block_size=block_size,
    )
    cache_heirarchy.create_cache(level=1, cache_size=l1_size, associativity=l1_assoc)
    if l2_size > 0:
        cache_heirarchy.create_cache(
            level=2, cache_size=l2_size, associativity=l2_assoc
        )

    # Read the trace file
    with open(trace_file, "r") as file:
        for line in file:
            (
                operation,
                address,
            ) = line.split()  # split the line into operation and address

            if operation == "r":
                cache_heirarchy.read(address)
            elif operation == "w":
                cache_heirarchy.write(address)

    # Print the simulation results
    cache_heirarchy.print_results()


if __name__ == "__main__":
    main()
