from common.dates import Date
from common.score import BasicScore
from common.pages import PageMetadata
import math


def safe_log10(value: float) -> float:
    if value < 1:
        return 0
    return math.log10(value)


class BasicScorer:
    def __init__(self) -> None:
        pass

    def score(self, date: Date, data: dict[str, PageMetadata]) -> BasicScore:
        """
        Return the score for each page for the specified day. Here, the score is simply its relative view/edit delta compared to the previous week.
        """
        scores: dict[str, float] = {}
        for key, page_metadata in data.items():
            previous_day = date.add_days(-1)

            current_views = page_metadata.views.get_data_point(date)
            previous_week_views = page_metadata.views.get_data_point(previous_day)
            current_edits = page_metadata.net_bytes_difference.get_data_point(date)
            previous_week_edits = page_metadata.net_bytes_difference.get_data_point(
                previous_day
            )

            # Compute relative percent change in views and edits
            view_score = (
                abs(current_views - previous_week_views) / previous_week_views
                if previous_week_views != 0
                else 0
            )
            edit_score = (
                abs(current_edits - previous_week_edits) / previous_week_edits
                if previous_week_edits != 0
                else 0
            )

            # Combine the two scores
            # We give more weight to the view score (80%) than the edit score (20%)
            # We also cap the edit score at 10 to avoid it being too influential
            # The max value of this is 10
            delta_score = min(view_score, 10) * 0.8 + min(edit_score, 10) * 0.2

            # We also want to account for the overall magnitude of the views and edits
            # We do this by getting the log_10 of the sum of the views and edits
            # The max value of this is 10
            magnitude_score = min(safe_log10(current_views), 5) + min(
                safe_log10(current_edits), 5
            )

            # Combine the delta and magnitude scores
            scores[key] = delta_score + magnitude_score

        return BasicScore(scores)
