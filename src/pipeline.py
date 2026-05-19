from create_database import create_database
from extract import extract_all_coins
from transform import transform_all_coins
from load import load_incremental_data

def run_pipeline():
    """
    Run the full normalized incremental crypto ETL pipeline locally.
    """

    print("=" * 60)
    print("STARTING NORMALIZED CRYPTO INCREMENTAL ETL PIPELINE")
    print("=" * 60)

    print("\n[1/4] Creating database...")
    create_database()

    print("\n[2/4] Extracting crypto data...")
    extract_all_coins()

    print("\n[3/4] Transforming raw JSON...")
    transform_all_coins()

    print("\n[4/4] Loading new records incrementally...")
    load_incremental_data()

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()