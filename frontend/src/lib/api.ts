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
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return await response.json();
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
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return await response.json();
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
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return await response.json();
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
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return await response.json();
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
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return await response.json();
}

// Changed type name from TopViewGrowthData to TopViewsGainedData
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
  total_net_bytes_changed: number;
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

// todo: top views lost
// date as date,
// page_name,
// current_view_count,
// one_day_ago_view_count,
// two_days_ago_view_count,
// view_count_ratio

// todo: top shrinking
// date,
// page_name,
// net_bytes_changed
