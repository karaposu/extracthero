"""
Benchmark script for FilterHero performance testing.
Tests different models and methodologies (extractive vs subtractive).

Usage:
    python benchmark.py
"""

import csv
import json
import time
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from extracthero import FilterHero, WhatToRetain
from extracthero.utils import read_md


class FilterHeroBenchmark:
    def __init__(self):
        self.filter_hero = FilterHero()
        self.results = []
        self.individual_runs = []  # Store all individual run data
        
        # Configuration
        self.framework = "filterhero"
        self.methodologies = ["extractive", "subtractive"]
        self.models = [
            "gpt-4o", 
            "gpt-4.1-mini",  
            "gpt-4.1",
            "gpt-5-mini",  
            "gpt-5",      
        ]
        self.run_count = 5
        self.documents = [
            {"path": "samples/1.md", "name": "1.md", "expected_lines": 980},
            {"path": "samples/2.md", "name": "2.md", "expected_lines": 538},
        ]
        
        # What to retain specification
        self.what_to_retain = WhatToRetain(
            name="technical content",
            desc="actionable technical API sections: all information regarding endpoints, data types, all usage examples, authentications",
            text_rules=[
                "Keep all code examples and API documentation",
                "Keep authentication and setup instructions",
               
            ]
        )
    
    def run_single_test(self, doc_content: str, doc_lines: int, methodology: str, model: str) -> Dict[str, Any]:
        """Run a single test and collect metrics."""
        start_time = time.time()
        
        try:
            if methodology == "extractive":
                filter_op = self.filter_hero.run(
                    text=doc_content,
                    extraction_spec=self.what_to_retain,
                    filter_strategy="contextual",
                    filter_mode="extractive",
                    model_name=model
                )
            else:  # subtractive
                filter_op = self.filter_hero.run(
                    text=doc_content,
                    extraction_spec=self.what_to_retain,
                    filter_strategy="contextual",
                    filter_mode="subtractive",
                    model_name=model
                )
            
            elapsed_time = time.time() - start_time
            
            # Calculate metrics
            if filter_op.success:
                original_lines = filter_op.original_line_count or doc_lines
                retained_lines = filter_op.retained_line_count or 0
                line_retain_ratio = retained_lines / original_lines if original_lines > 0 else 0
                
                # Extract costs from usage
                usage = filter_op.usage or {}
                total_cost = usage.get('total_cost', 0)
                
                # Calculate input/output costs if available
                # If specific costs aren't provided, try to derive from tokens
                input_cost = usage.get('prompt_cost', 0)
                output_cost = usage.get('completion_cost', 0)
                
                # If we don't have prompt_cost/completion_cost but have total_cost,
                # we can't split it accurately, but we know the total
                if total_cost > 0 and input_cost == 0 and output_cost == 0:
                    # For reporting purposes, just show total cost
                    # We can't accurately split without token counts and pricing
                    pass
                
                return {
                    "success": True,
                    "line_retain_ratio": line_retain_ratio,
                    "elapsed_time": elapsed_time,
                    "total_cost": total_cost,
                    "input_cost": input_cost,
                    "output_cost": output_cost,
                    "original_lines": original_lines,
                    "retained_lines": retained_lines
                }
            else:
                return {
                    "success": False,
                    "error": filter_op.error
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def run_benchmark_combination(self, doc: Dict, methodology: str, model: str):
        """Run multiple tests for a single combination and aggregate results."""
        print(f"Testing: {doc['name']} | {methodology} | {model}")
        
        # Read document
        doc_content = read_md(doc['path'])
        doc_lines = len(doc_content.split('\n'))
        
        # Run multiple tests
        test_results = []
        for run_num in range(self.run_count):
            print(f"  Run {run_num + 1}/{self.run_count}...", end='')
            result = self.run_single_test(doc_content, doc_lines, methodology, model)
            
            # Save individual run data
            individual_run = {
                "framework": self.framework,
                "methodology": methodology,
                "model_name": model,
                "model_config": "-",
                "doc_name": doc['name'],
                "doc_length": doc_lines,
                "run_number": run_num + 1,
                "timestamp": datetime.now().isoformat(),
                "success": result["success"]
            }
            
            if result["success"]:
                test_results.append(result)
                individual_run.update({
                    "line_retain_ratio": result["line_retain_ratio"],
                    "elapsed_time": result["elapsed_time"],
                    "total_cost": result["total_cost"],
                    "input_cost": result["input_cost"],
                    "output_cost": result["output_cost"],
                    "original_lines": result["original_lines"],
                    "retained_lines": result["retained_lines"],
                    "error": None
                })
                print(" ✓")
            else:
                individual_run.update({
                    "line_retain_ratio": None,
                    "elapsed_time": None,
                    "total_cost": None,
                    "input_cost": None,
                    "output_cost": None,
                    "original_lines": doc_lines,
                    "retained_lines": None,
                    "error": result.get('error', 'Unknown error')
                })
                print(f" ✗ ({result.get('error', 'Unknown error')})")
            
            self.individual_runs.append(individual_run)
            
            # Wait between runs (except after the last run)
            if run_num < self.run_count - 1:
                print("  Waiting 10 seconds before next run...")
                time.sleep(10)
        
        # Calculate aggregate metrics
        if test_results:
            line_retain_ratios = [r["line_retain_ratio"] for r in test_results]
            elapsed_times = [r["elapsed_time"] for r in test_results]
            total_costs = [r["total_cost"] for r in test_results]
            input_costs = [r["input_cost"] for r in test_results]
            output_costs = [r["output_cost"] for r in test_results]
            
            benchmark_result = {
                "framework": self.framework,
                "methodology": methodology,
                "model_name": model,
                "model_config": "-",
                "run_count": len(test_results),
                "doc_length": doc_lines,
                "doc_name": doc['name'],
                "avg_line_retain_ratio": np.mean(line_retain_ratios),
                "line_retain_std": np.std(line_retain_ratios),
                "avg_elapsed_time": np.mean(elapsed_times),
                "avg_cost": np.mean(total_costs),
                "avg_input_cost": np.mean(input_costs),
                "avg_output_cost": np.mean(output_costs),
                "successful_runs": len(test_results),
                "failed_runs": self.run_count - len(test_results)
            }
        else:
            # All runs failed
            benchmark_result = {
                "framework": self.framework,
                "methodology": methodology,
                "model_name": model,
                "model_config": "-",
                "run_count": 0,
                "doc_length": doc_lines,
                "doc_name": doc['name'],
                "avg_line_retain_ratio": 0,
                "line_retain_std": 0,
                "avg_elapsed_time": 0,
                "avg_cost": 0,
                "avg_input_cost": 0,
                "avg_output_cost": 0,
                "successful_runs": 0,
                "failed_runs": self.run_count
            }
        
        self.results.append(benchmark_result)
        return benchmark_result
    
    def run_all_benchmarks(self):
        """Run all benchmark combinations."""
        print("=" * 80)
        print("Starting FilterHero Benchmark")
        print("=" * 80)
        
        total_combinations = len(self.documents) * len(self.methodologies) * len(self.models)
        current = 0
        
        for doc in self.documents:
            for methodology in self.methodologies:
                for model in self.models:
                    current += 1
                    print(f"\n[{current}/{total_combinations}] ", end='')
                    self.run_benchmark_combination(doc, methodology, model)
        
        print("\n" + "=" * 80)
        print("Benchmark completed!")
        print("=" * 80)
    
    def save_results(self, filename: str = None):
        """Save benchmark results to CSV."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.csv"
        
        if not self.results and not self.individual_runs:
            print("No results to save!")
            return
        
        # Save individual runs first
        if self.individual_runs:
            individual_filename = filename.replace('.csv', '_individual_runs.csv')
            individual_columns = [
                "framework",
                "methodology",
                "model_name", 
                "model_config",
                "doc_name",
                "doc_length",
                "run_number",
                "timestamp",
                "success",
                "line_retain_ratio",
                "elapsed_time",
                "total_cost",
                "input_cost",
                "output_cost",
                "original_lines",
                "retained_lines",
                "error"
            ]
            
            with open(individual_filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=individual_columns)
                writer.writeheader()
                for run in self.individual_runs:
                    # Round numerical values for better readability
                    formatted_run = run.copy()
                    if run["line_retain_ratio"] is not None:
                        formatted_run["line_retain_ratio"] = round(run["line_retain_ratio"], 4)
                    if run["elapsed_time"] is not None:
                        formatted_run["elapsed_time"] = round(run["elapsed_time"], 2)
                    if run["total_cost"] is not None:
                        formatted_run["total_cost"] = round(run["total_cost"], 6)
                    if run["input_cost"] is not None:
                        formatted_run["input_cost"] = round(run["input_cost"], 6)
                    if run["output_cost"] is not None:
                        formatted_run["output_cost"] = round(run["output_cost"], 6)
                    writer.writerow(formatted_run)
            
            print(f"\nIndividual runs saved to: {individual_filename}")
            
            # Also save individual runs as JSON
            individual_json_filename = individual_filename.replace('.csv', '.json')
            with open(individual_json_filename, 'w') as jsonfile:
                json.dump(self.individual_runs, jsonfile, indent=2)
            print(f"Individual runs JSON saved to: {individual_json_filename}")
        
        # Save aggregated results
        if self.results:
            # Define CSV columns for aggregated results
            columns = [
                "framework",
                "methodology", 
                "model_name",
                "model_config",
                "run_count",
                "doc_length",
                "doc_name",
                "avg_line_retain_ratio",
                "line_retain_std",
                "avg_elapsed_time",
                "avg_cost",
                "avg_input_cost",
                "avg_output_cost",
                "successful_runs",
                "failed_runs"
            ]
            
            # Write aggregated CSV
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
                for result in self.results:
                    # Round numerical values for better readability
                    formatted_result = result.copy()
                    formatted_result["avg_line_retain_ratio"] = round(result["avg_line_retain_ratio"], 4)
                    formatted_result["line_retain_std"] = round(result["line_retain_std"], 4)
                    formatted_result["avg_elapsed_time"] = round(result["avg_elapsed_time"], 2)
                    formatted_result["avg_cost"] = round(result["avg_cost"], 6)
                    formatted_result["avg_input_cost"] = round(result["avg_input_cost"], 6)
                    formatted_result["avg_output_cost"] = round(result["avg_output_cost"], 6)
                    writer.writerow(formatted_result)
            
            print(f"Aggregated results saved to: {filename}")
            
            # Also save aggregated as JSON for detailed analysis
            json_filename = filename.replace('.csv', '.json')
            with open(json_filename, 'w') as jsonfile:
                json.dump(self.results, jsonfile, indent=2)
            print(f"Aggregated results JSON saved to: {json_filename}")
    
    def print_summary(self):
        """Print a summary of the benchmark results."""
        if not self.results:
            print("No results to summarize!")
            return
        
        print("\n" + "=" * 80)
        print("BENCHMARK SUMMARY")
        print("=" * 80)
        
        # Group by methodology
        for methodology in self.methodologies:
            method_results = [r for r in self.results if r["methodology"] == methodology]
            if not method_results:
                continue
            
            print(f"\n{methodology.upper()} MODE:")
            print("-" * 40)
            
            for result in method_results:
                print(f"  {result['doc_name']} | {result['model_name']}")
                print(f"    Retain Ratio: {result['avg_line_retain_ratio']:.2%} ± {result['line_retain_std']:.2%}")
                print(f"    Avg Time: {result['avg_elapsed_time']:.2f}s")
                print(f"    Avg Cost: ${result['avg_cost']:.4f}")
                print(f"    Success Rate: {result['successful_runs']}/{result['run_count']}")
        
        print("=" * 80)


def main():
    """Main execution function."""
    benchmark = FilterHeroBenchmark()
    
    try:
        # Run benchmarks
        benchmark.run_all_benchmarks()
        
        # Save results
        benchmark.save_results()
        
        # Print summary
        benchmark.print_summary()
        
    except KeyboardInterrupt:
        print("\n\nBenchmark interrupted by user!")
        if benchmark.results:
            print("Saving partial results...")
            benchmark.save_results("benchmark_partial_results.csv")
    except Exception as e:
        print(f"\nError during benchmark: {e}")
        if benchmark.results:
            print("Saving partial results...")
            benchmark.save_results("benchmark_error_results.csv")


if __name__ == "__main__":
    main()