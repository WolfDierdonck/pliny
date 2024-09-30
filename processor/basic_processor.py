class BasicProcessor:
    def __init__(self) -> None:
        pass

    def process_test(self, data: list[dict[str, int]]) -> list[str]:
        """
        Return the page with the biggest view count delta for each day
        """
        assert len(data) > 1, "Data must have at least 2 days"

        previous_day = {key: value for key, value in data[0].items()}
        result = []
        for day in data[1:]:
            current_day = {key: value for key, value in day.items()}

            biggest_delta = float("-inf")
            biggest_delta_article = ""
            for article, count in current_day.items():
                previous_count = previous_day[article]
                delta = count - previous_count
                if delta > biggest_delta:
                    biggest_delta = delta
                    biggest_delta_article = article

            result.append(biggest_delta_article)
            previous_day = current_day

        return result
