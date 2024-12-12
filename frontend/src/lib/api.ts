export type TopViewsData = {
  article: string;
  views: number;
};

export async function getTopViewsData(): Promise<TopViewsData[]> {
  const response = await fetch('/topViews');
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return await response.json();
}
