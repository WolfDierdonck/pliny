package main

import "cloud.google.com/go/civil"

type TopEditorsData struct {
	Date        civil.Date `bigquery:"date" json:"date"`
	PageName    string     `bigquery:"page_name" json:"page_name"`
	EditorCount int        `bigquery:"editor_count" json:"editor_count"`
}

type TopEditsData struct {
	Date      civil.Date `bigquery:"date" json:"date"`
	PageName  string     `bigquery:"page_name" json:"page_name"`
	EditCount int        `bigquery:"edit_count" json:"edit_count"`
}

type TopGrowingData struct {
	Date            civil.Date `bigquery:"date" json:"date"`
	PageName        string     `bigquery:"page_name" json:"page_name"`
	NetBytesChanged int        `bigquery:"net_bytes_changed" json:"net_bytes_changed"`
}

type TopVandalismData struct {
	Date             civil.Date `bigquery:"date" json:"date"`
	PageName         string     `bigquery:"page_name" json:"page_name"`
	ViewCount        int        `bigquery:"view_count" json:"view_count"`
	RevertCount      int        `bigquery:"revert_count" json:"revert_count"`
	AbsBytesReverted int        `bigquery:"abs_bytes_reverted" json:"abs_bytes_reverted"`
	EditCount        int        `bigquery:"edit_count" json:"edit_count"`
	PercentReverted  float64    `bigquery:"percent_reverted" json:"percent_reverted"`
}

type TopViewsData struct {
	Date      civil.Date `bigquery:"date" json:"date"`
	PageName  string     `bigquery:"page_name" json:"page_name"`
	ViewCount int        `bigquery:"view_count" json:"view_count"`
}

type TotalMetadataData struct {
	Date             civil.Date `bigquery:"date" json:"date"`
	TotalEditCount   int        `bigquery:"total_edit_count" json:"total_edit_count"`
	TotalViewCount   int        `bigquery:"total_view_count" json:"total_view_count"`
	TotalEditorCount int        `bigquery:"total_editor_count" json:"total_editor_count"`
	TotalRevertCount int        `bigquery:"total_revert_count" json:"total_revert_count"`
}

type WikipediaGrowthData struct {
	Date                 civil.Date `bigquery:"date" json:"date"`
	WikipediaGrowthBytes int        `bigquery:"wikipedia_growth_bytes" json:"wikipedia_growth_bytes"`
}
