export type TopViewsData = {
  article: string;
  views: number;
};

export async function getTopViewsData(): Promise<TopViewsData[]> {
  const response = await fetch('/topViews');
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  const data = await response.json();
  console.log(data);

  return data.map(
    (item: TopViewsData) =>
      ({
        article: item.article,
        views: item.views,
      }) as TopViewsData,
  );
}
