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
  start_date: string,
  end_date: string,
  limit: number,
): Promise<TopVandalismData[]> {
  const response = await fetch(
    `/topVandalism/${start_date}/${end_date}/${limit}`,
  );
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
