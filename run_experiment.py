"""Master command line interface for reproducible SPOTPY examples."""
from __future__ import annotations
import argparse
from src.experiments import run_hydrology, run_rosenbrock

def main():
    parser=argparse.ArgumentParser(description="SPOTPY Laboratory for SWAT+ IGP")
    parser.add_argument("--example",choices=("rosenbrock","hydrology"),required=True)
    parser.add_argument("--algorithm",choices=("mc","lhs","sceua","dds","fast"),required=True)
    parser.add_argument("--runs",type=int,default=100)
    parser.add_argument("--objective",choices=("nse","kge","rmse"),default="nse")
    parser.add_argument("--seed",type=int,default=42)
    args=parser.parse_args()
    if args.example=="rosenbrock": run_rosenbrock(args.algorithm,args.runs,args.seed)
    else: run_hydrology(args.algorithm,args.runs,args.objective,args.seed)
if __name__=="__main__": main()

