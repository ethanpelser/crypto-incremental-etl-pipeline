import pipeline


def test_run_pipeline_calls_steps_in_order(monkeypatch):
    calls = []

    monkeypatch.setattr(pipeline, "create_database", lambda: calls.append("create_database"))
    monkeypatch.setattr(pipeline, "extract_all_coins", lambda: calls.append("extract_all_coins"))
    monkeypatch.setattr(pipeline, "transform_all_coins", lambda: calls.append("transform_all_coins"))
    monkeypatch.setattr(pipeline, "load_incremental_data", lambda: calls.append("load_incremental_data"))
    monkeypatch.setattr(pipeline, "run_validation_checks", lambda: calls.append("run_validation_checks"))

    pipeline.run_pipeline()

    assert calls == [
        "create_database",
        "extract_all_coins",
        "transform_all_coins",
        "load_incremental_data",
        "run_validation_checks",
    ]
