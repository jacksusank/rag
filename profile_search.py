import cProfile
import pstats
import sys

# Import the main function from search
from chatgpt_search import main

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python profile_search.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    
    # Profile the main function
    profiler = cProfile.Profile()
    profiler.enable()
    
    main(query)
    
    profiler.disable()
    
    # Save the profiling data to a file
    profiler.dump_stats('profile_output.prof')
    
    # Print profiling stats to console
    pstats.Stats(profiler).strip_dirs().sort_stats('cumulative').print_stats(10)
