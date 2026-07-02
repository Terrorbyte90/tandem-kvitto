import json
import pytest
from logic import calculate_split


class TestCalculateSplit:
    def test_normal_case(self):
        result = calculate_split(1000, 4, 10)
        assert result["total_med_dricks"] == pytest.approx(1100.0)
        assert result["per_person"] == pytest.approx(275.0)

    def test_zero_tip(self):
        result = calculate_split(1000, 4, 0)
        assert result["total_med_dricks"] == pytest.approx(1000.0)
        assert result["per_person"] == pytest.approx(250.0)

    def test_single_person(self):
        result = calculate_split(500, 1, 15)
        assert result["total_med_dricks"] == pytest.approx(575.0)
        assert result["per_person"] == pytest.approx(575.0)

    def test_high_tip(self):
        result = calculate_split(200, 2, 25)
        assert result["total_med_dricks"] == pytest.approx(250.0)
        assert result["per_person"] == pytest.approx(125.0)

    def test_fractional_tip(self):
        result = calculate_split(100, 3, 7.5)
        assert result["total_med_dricks"] == pytest.approx(107.5)
        assert result["per_person"] == pytest.approx(35.833333333333336)

    def test_zero_people_raises(self):
        with pytest.raises(ValueError, match="Antal personer måste vara större än 0"):
            calculate_split(100, 0, 10)

    def test_negative_people_raises(self):
        with pytest.raises(ValueError, match="Antal personer måste vara större än 0"):
            calculate_split(100, -1, 10)

    def test_zero_amount(self):
        result = calculate_split(0, 4, 10)
        assert result["total_med_dricks"] == pytest.approx(0.0)
        assert result["per_person"] == pytest.approx(0.0)

    def test_large_group(self):
        result = calculate_split(5000, 10, 15)
        assert result["total_med_dricks"] == pytest.approx(5750.0)
        assert result["per_person"] == pytest.approx(575.0)

    # --- Tests for uneven splitting ---

    def test_special_person_50_percent(self):
        result = calculate_split(1000, 4, 10, special_person_percent=50)
        # total_med_dricks = 1000 * 1.10 = 1100
        assert result["total_med_dricks"] == pytest.approx(1100.0)
        # special_person_share = 1100 * 0.50 = 550
        assert result["special_person_share"] == pytest.approx(550.0)
        # others_share = (1100 - 550) / 3 = 183.333...
        assert result["others_share"] == pytest.approx(183.33333333333334)

    def test_special_person_100_percent(self):
        result = calculate_split(1000, 3, 0, special_person_percent=100)
        assert result["total_med_dricks"] == pytest.approx(1000.0)
        assert result["special_person_share"] == pytest.approx(1000.0)
        assert result["others_share"] == pytest.approx(0.0)

    def test_special_person_0_percent(self):
        result = calculate_split(1000, 3, 0, special_person_percent=0)
        assert result["total_med_dricks"] == pytest.approx(1000.0)
        assert result["special_person_share"] == pytest.approx(0.0)
        assert result["others_share"] == pytest.approx(500.0)

    def test_special_person_with_tip(self):
        result = calculate_split(2000, 5, 20, special_person_percent=25)
        # total = 2000 * 1.20 = 2400
        assert result["total_med_dricks"] == pytest.approx(2400.0)
        # special = 2400 * 0.25 = 600
        assert result["special_person_share"] == pytest.approx(600.0)
        # others = (2400 - 600) / 4 = 450
        assert result["others_share"] == pytest.approx(450.0)

    def test_special_person_sum_matches_total(self):
        """Special person + others must sum to total_med_dricks."""
        result = calculate_split(1000, 4, 10, special_person_percent=30)
        total_others = result["others_share"] * 3
        assert result["special_person_share"] + total_others == pytest.approx(
            result["total_med_dricks"]
        )

    def test_special_person_with_single_person_raises(self):
        with pytest.raises(ValueError, match="Specialprocent kräver minst 2 personer"):
            calculate_split(1000, 1, 10, special_person_percent=50)

    def test_special_person_invalid_percent_raises(self):
        with pytest.raises(ValueError, match="Specialprocent måste vara mellan 0 och 100"):
            calculate_split(1000, 3, 10, special_person_percent=150)

    def test_special_person_negative_percent_raises(self):
        with pytest.raises(ValueError, match="Specialprocent måste vara mellan 0 och 100"):
            calculate_split(1000, 3, 10, special_person_percent=-5)

    # --- Tests for JSON serialization ---

    def test_result_is_json_serializable_normal(self):
        """Result dictionary must be JSON-serializable for normal split."""
        result = calculate_split(1000, 4, 10)
        json_str = json.dumps(result, indent=2)
        assert "total_med_dricks" in json_str
        assert "per_person" in json_str
        assert "special_person_share" in json_str
        assert "others_share" in json_str
        # Verify round-trip
        parsed = json.loads(json_str)
        assert parsed["total_med_dricks"] == pytest.approx(1100.0)
        assert parsed["per_person"] == pytest.approx(275.0)
        assert parsed["special_person_share"] is None
        assert parsed["others_share"] is None

    def test_result_is_json_serializable_special(self):
        """Result dictionary must be JSON-serializable for special person split."""
        result = calculate_split(1000, 4, 10, special_person_percent=50)
        json_str = json.dumps(result, indent=2)
        assert "total_med_dricks" in json_str
        assert "special_person_share" in json_str
        assert "others_share" in json_str
        assert "per_person" in json_str
        # Verify round-trip
        parsed = json.loads(json_str)
        assert parsed["total_med_dricks"] == pytest.approx(1100.0)
        assert parsed["special_person_share"] == pytest.approx(550.0)
        assert parsed["others_share"] == pytest.approx(183.33333333333334)
        assert parsed["per_person"] is None

    def test_result_has_all_four_keys(self):
        """Result dictionary must always contain exactly four keys."""
        result_normal = calculate_split(1000, 4, 10)
        result_special = calculate_split(1000, 4, 10, special_person_percent=50)
        expected_keys = {"total_med_dricks", "special_person_share", "others_share", "per_person"}
        assert set(result_normal.keys()) == expected_keys
        assert set(result_special.keys()) == expected_keys

    def test_result_values_are_json_safe_types(self):
        """All values in result must be JSON-safe types (int, float, None)."""
        result_normal = calculate_split(1000, 4, 10)
        result_special = calculate_split(1000, 4, 10, special_person_percent=50)
        for result in (result_normal, result_special):
            for key, value in result.items():
                assert isinstance(value, (int, float, type(None))), (
                    f"Key '{key}' has non-JSON-safe type: {type(value)}"
                )
