import sys

def main():
    if len(sys.argv) != 8:
        print("Usage: python sim_cache.py <BLOCKSIZE> <L1_SIZE> <L1_ASSOC> <L2_SIZE> <L2_ASSOC> <REPLACEMENT_POLICY> <INCLUSION_PROPERTY> <trace_file>")
        return

    block_size = int(sys.argv[1])
    l1_size = int(sys.argv[2])
    l1_assoc = int(sys.argv[3])
    l2_size = int(sys.argv[4])
    l2_assoc = int(sys.argv[5])
    replacement_policy = int(sys.argv[6])
    inclusion_property = int(sys.argv[7])
    trace_file = sys.argv[8]

if __name__ == "__main__":
  main()
