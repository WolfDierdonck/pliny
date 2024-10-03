from common.time_series import TimeSeries


class BasicScore:
    def __init__(self, scores: dict[str, TimeSeries]) -> None:
        self.scores = scores
