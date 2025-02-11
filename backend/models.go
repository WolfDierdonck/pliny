package main

import "cloud.google.com/go/civil"

type TopViewsData struct {
	Date      civil.Date `bigquery:"date" json:"date"`
	PageName  string     `bigquery:"page_name" json:"page_name"`
	ViewCount int        `bigquery:"view_count" json:"view_count"`
}

type TopVandalismData struct {
	StartDate       civil.Date `bigquery:"start_date" json:"start_date"`
	EndDate         civil.Date `bigquery:"end_date" json:"end_date"`
	PageName        string     `bigquery:"page_name" json:"page_name"`
	ViewCount       int        `bigquery:"view_count" json:"view_count"`
	RevertCount     int        `bigquery:"revert_count" json:"revert_count"`
	BytesReverted   int        `bigquery:"bytes_reverted" json:"bytes_reverted"`
	EditCount       int        `bigquery:"edit_count" json:"edit_count"`
	PercentReverted float64    `bigquery:"percent_reverted" json:"percent_reverted"`
}

type TopGrowingData struct {
	Date            civil.Date `bigquery:"date" json:"date"`
	PageName        string     `bigquery:"page_name" json:"page_name"`
	NetBytesChanged int        `bigquery:"net_bytes_changed" json:"net_bytes_changed"`
}
