"""
Pandas entrypoint for canonical entity preparation.
Reuses run_feature_engineering.py implementation to ensure one schema contract.
"""

from run_feature_engineering import main


if __name__ == "__main__":
    main()
