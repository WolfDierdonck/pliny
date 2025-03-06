function processPageName(page_name: string): string {
  return page_name.replace(/_/g, ' ');
}

async function getResponseJson<T>(response: Response): Promise<T[]> {
  if (!response.ok) {
    console.error('Network response was not ok in getResponseJson');
    return Promise.resolve([]);
  }

  let data: T[] = [];
  const responseText = await response.text();
  try {
    // Try to parse the response as JSON
    data = JSON.parse(responseText);
  } catch (error) {
    // Sometimes, the backend randomly returns two JSON identical objects concatenated
    // We can try to parse the response as JSON again, but this time, we will split the response in half
    const firstHalf = responseText.split('][')[0] + ']';
    data = JSON.parse(firstHalf);
  }

  if (!data) {
    return [];
  }
  return data;
}

export type TopEditorsData = {
  date: string;
  page_name: string;
  view_count: number;
  edit_count: number;
  revert_count: number;
  editor_count: number;
  net_bytes_changed: number;
  abs_bytes_changed: number;
  abs_bytes_reverted: number;
};

export async function getTopEditorsData(
  date: string,
  limit: number,
): Promise<TopEditorsData[]> {
  const response = await fetch(`/topEditors/${date}/${limit}`);

  const data: TopEditorsData[] = await getResponseJson(response);

  data.forEach((item) => {
    item.page_name = processPageName(item.page_name);
  });
  return data;
}

export type TopEditsData = {
  date: string;
  page_name: string;
  view_count: number;
  edit_count: number;
  revert_count: number;
  editor_count: number;
  net_bytes_changed: number;
  abs_bytes_changed: number;
  abs_bytes_reverted: number;
};

export async function getTopEditsData(
  date: string,
  limit: number,
): Promise<TopEditsData[]> {
  const response = await fetch(`/topEdits/${date}/${limit}`);

  const data: TopEditsData[] = await getResponseJson(response);

  data.forEach((item) => {
    item.page_name = processPageName(item.page_name);
  });
  return data;
}

export type TopGrowingData = {
  date: string;
  page_name: string;
  view_count: number;
  edit_count: number;
  revert_count: number;
  editor_count: number;
  net_bytes_changed: number;
  abs_bytes_changed: number;
  abs_bytes_reverted: number;
};

export async function getTopGrowingData(
  date: string,
  limit: number,
): Promise<TopGrowingData[]> {
  const response = await fetch(`/topGrowing/${date}/${limit}`);

  const data: TopGrowingData[] = await getResponseJson(response);

  data.forEach((item) => {
    item.page_name = processPageName(item.page_name);
  });
  return data;
}

export type TopShrinkingData = {
  date: string;
  page_name: string;
  net_bytes_changed: number;
};

export async function getTopShrinkingData(
  date: string,
  limit: number,
): Promise<TopShrinkingData[]> {
  const response = await fetch(`/topShrinking/${date}/${limit}`);

  const data: TopShrinkingData[] = await getResponseJson(response);

  data.forEach((item) => {
    item.page_name = processPageName(item.page_name);
  });
  return data;
}

export type TopVandalismData = {
  page_name: string;
  view_count: number;
  edit_count: number;
  revert_count: number;
  editor_count: number;
  net_bytes_changed: number;
  abs_bytes_changed: number;
  abs_bytes_reverted: number;
  percent_reverted: number;
  avg_bytes_reverted_per_revert: number;
};

export async function getTopVandalismData(
  end_date: string,
  limit: number,
): Promise<TopVandalismData[]> {
  const response = await fetch(`/topVandalism/${end_date}/${limit}`);

  const data: TopVandalismData[] = await getResponseJson(response);

  data.forEach((item) => {
    item.page_name = processPageName(item.page_name);
  });
  return data;
}

export type TopViewsGainedData = {
  page_name: string;
  current_view_count: number;
  one_day_ago_view_count: number;
  two_days_ago_view_count: number;
  view_count_ratio: number;
};

export async function getTopViewsGainedData(
  date: string,
  limit: number,
): Promise<TopViewsGainedData[]> {
  const response = await fetch(`/topViewsGained/${date}/${limit}`);

  const data: TopViewsGainedData[] = await getResponseJson(response);

  data.forEach((item) => {
    item.page_name = processPageName(item.page_name);
  });
  return data;
}

export type TopViewsLostData = {
  date: string;
  page_name: string;
  current_view_count: number;
  one_day_ago_view_count: number;
  two_days_ago_view_count: number;
  view_count_ratio: number;
};

export async function getTopViewsLostData(
  date: string,
  limit: number,
): Promise<TopViewsLostData[]> {
  const response = await fetch(`/topViewsLost/${date}/${limit}`);

  const data: TopViewsLostData[] = await getResponseJson(response);

  data.forEach((item) => {
    item.page_name = processPageName(item.page_name);
  });
  return data;
}

export type TopViewsData = {
  date: string;
  page_name: string;
  view_count_0: number;
  edit_count: number;
  revert_count: number;
  editor_count: number;
  net_bytes_changed: number;
  abs_bytes_changed: number;
  abs_bytes_reverted: number;
  view_count_1: number;
  view_count_2: number;
  view_count_3: number;
  view_count_4: number;
  view_count_5: number;
  view_count_6: number;
};

export async function getTopViewsData(
  date: string,
  limit: number,
): Promise<TopViewsData[]> {
  const response = await fetch(`/topViews/${date}/${limit}`);

  const data: TopViewsData[] = await getResponseJson(response);

  data.forEach((item) => {
    item.page_name = processPageName(item.page_name);
  });
  return data;
}

export type WikipediaStatsData = {
  total_edit_count: number;
  total_view_count: number;
  total_editor_count: number;
  total_revert_count: number;
  total_net_bytes_changed: number;
};

export async function getTotalMetadata(
  date: string,
): Promise<WikipediaStatsData | null> {
  const response = await fetch(`/totalMetadata/${date}`);

  const data: WikipediaStatsData[] = await getResponseJson(response);

  // Return the first element of the array
  return data ? data[0] : null;
}
