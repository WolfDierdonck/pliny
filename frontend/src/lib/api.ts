export type TopViewsData = {
  date: string;
  page_name: string;
  view_count: number;
};

export async function getTopViewsData(
  date: string,
  limit: number,
): Promise<TopViewsData[]> {
  const response = await fetch(`/topViews/${date}/${limit}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return await response.json();
}

export type TopVandalismData = {
  start_date: string;
  end_date: string;
  page_name: string;
  view_count: number;
  revert_count: number;
  bytes_reverted: number;
  edit_count: number;
  percent_reverted: number;
};

export async function getTopVandalismData(
  end_date: string,
  limit: number,
): Promise<TopVandalismData[]> {
  const response = await fetch(`/topVandalism/${end_date}/${limit}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return await response.json();
}

export type TopGrowingData = {
  date: string;
  page_name: string;
  net_bytes_changed: number;
};

export async function getTopGrowingData(
  date: string,
  limit: number,
): Promise<TopGrowingData[]> {
  const response = await fetch(`/topGrowing/${date}/${limit}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return await response.json();
}

export type TopEditorsData = {
  date: string;
  page_name: string;
  editor_count: number;
};

export async function getTopEditorsData(
  date: string,
  limit: number,
): Promise<TopEditorsData[]> {
  const response = await fetch(`/topEditors/${date}/${limit}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return await response.json();
}

export type TopEditsData = {
  date: string;
  page_name: string;
  edit_count: number;
};

export async function getTopEditsData(
  date: string,
  limit: number,
): Promise<TopEditsData[]> {
  const response = await fetch(`/topEdits/${date}/${limit}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return await response.json();
}

export type TopViewDeltaData = {
  date: string;
  page_name: string;
  current_view_count: number;
  previous_view_count: number;
  view_count_ratio: number;
};

export async function getTopViewDeltaData(
  date: string,
  limit: number,
): Promise<TopViewDeltaData[]> {
  const response = await fetch(`/topViewDelta/${date}/${limit}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return await response.json();
}

export type WikipediaStatsData = {
  total_edit_count: number;
  total_view_count: number;
  total_editor_count: number;
  total_revert_count: number;
};

export async function getTotalMetadata(
  date: string,
): Promise<WikipediaStatsData> {
  const response = await fetch(`/totalMetadata/${date}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  const data = await response.json();
  // Return the first element of the array
  return data[0];
}

export type WikipediaGrowthData = {
  wikipedia_growth_bytes: number;
};

export async function getWikipediaGrowth(
  date: string,
): Promise<WikipediaGrowthData> {
  const response = await fetch(`/wikipediaGrowth/${date}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  const data = await response.json();
  return data[0];
}
