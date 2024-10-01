from common.score import BasicScore


class BasicProcessor:
    def __init__(self) -> None:
        pass

    def process_test(self, data: list[dict[str, int]]) -> BasicScore:
        """
        Return the score for each page/day. Here, the score is simple its view delta from the previous day.
        """
        assert len(data) > 1, "Data must have at least 2 days"

        scores: list[dict[str, int]] = []
        previous_day = {key: value for key, value in data[0].items()}
        for day in data[1:]:
            current_day = {key: value for key, value in day.items()}

            scores.append(
                {key: current_day[key] - previous_day[key] for key in current_day}
            )
            previous_day = current_day

        return BasicScore(scores)
