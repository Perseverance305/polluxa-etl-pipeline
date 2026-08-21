from datetime import datetime

from src.watermark import get_watermark, set_watermark


PIPELINE_NAME = "test_watermark_pipeline"


def test_watermark_can_be_created_and_read():

    watermark = datetime(2026, 8, 20, 12, 0, 0)

    set_watermark(
        PIPELINE_NAME,
        watermark,
    )

    result = get_watermark(PIPELINE_NAME)

    assert result == watermark


def test_watermark_can_be_updated():

    first_watermark = datetime(2026, 8, 20, 12, 0, 0)
    second_watermark = datetime(2026, 8, 21, 12, 0, 0)

    set_watermark(
        PIPELINE_NAME,
        first_watermark,
    )

    set_watermark(
        PIPELINE_NAME,
        second_watermark,
    )

    result = get_watermark(PIPELINE_NAME)

    assert result == second_watermark