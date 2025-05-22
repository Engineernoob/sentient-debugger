import cProfile
import pstats
import io
from typing import Callable, Any, Dict
import time
import tracemalloc

class CodeProfiler:
    def __init__(self):
        self.profiling_history = []
    
    def profile_function(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Profile a function's execution time and memory usage"""
        # CPU profiling
        pr = cProfile.Profile()
        pr.enable()
        
        # Memory profiling
        tracemalloc.start()
        start_time = time.time()
        
        # Execute function
        result = func(*args, **kwargs)
        
        # Collect metrics
        execution_time = time.time() - start_time
        current, peak = tracemalloc.get_traced_memory()
        
        pr.disable()
        tracemalloc.stop()
        
        # Process profiling results
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        
        profile_data = {
            'execution_time': execution_time,
            'memory_current': current / 10**6,  # MB
            'memory_peak': peak / 10**6,  # MB
            'detailed_stats': s.getvalue()
        }
        
        self.profiling_history.append(profile_data)
        return profile_data