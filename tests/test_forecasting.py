from src.forecasting import train_models, predict_test


def test_training_pipeline_persists_and_predicts(sample_data, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    table, meta = train_models(sample_data, "total_energy_kwh", tmp_path / "models")
    assert {"MAE", "RMSE", "R2", "Model"} <= set(table)
    assert len(table) == 4
    assert meta["test_samples"] > 0
    assert (
        tmp_path / "reports/evaluation/model_comparison_total_energy_kwh.csv"
    ).exists()
    assert (
        tmp_path / "reports/evaluation/test_predictions_total_energy_kwh.csv"
    ).exists()
    pred = predict_test(sample_data, "total_energy_kwh", tmp_path / "models")
    assert pred.predicted.notna().all()
