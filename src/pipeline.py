from create_database import create_database
from extract import extract_all_coins
from transform import transform_all_coins
from load import load_incremental_data
from validate import run_validation_checks

def run_pipeline():
    """
    Run the full normalized incremental crypto ETL pipeline locally.
    """

    print("=" * 60)
    print("STARTING NORMALIZED CRYPTO INCREMENTAL ETL PIPELINE")
    print("=" * 60)

    print("\n[1/5] Creating database...")
    create_database()

    print("\n[2/5] Extracting crypto data...")
    extract_all_coins()

    print("\n[3/5 Transforming raw JSON...")
    transform_all_coins()

    print("\n[4/5] Loading new records incrementally...")
    load_incremental_data()

    print("\n[5/5] Running validation checks...")
    run_validation_checks()

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()