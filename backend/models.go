package main

import (
	"encoding/json"
	"math"
	"strconv"

	"cloud.google.com/go/bigquery"
	"cloud.google.com/go/civil"
)

type TopEditorsData struct {
	Date             civil.Date `bigquery:"date" json:"date"`
	PageName         string     `bigquery:"page_name" json:"page_name"`
	ViewCount        int        `bigquery:"view_count" json:"view_count"`
	EditCount        int        `bigquery:"edit_count" json:"edit_count"`
	RevertCount      int        `bigquery:"revert_count" json:"revert_count"`
	EditorCount      int        `bigquery:"editor_count" json:"editor_count"`
	NetBytesChanged  int        `bigquery:"net_bytes_changed" json:"net_bytes_changed"`
	AbsBytesChanged  int        `bigquery:"abs_bytes_changed" json:"abs_bytes_changed"`
	AbsBytesReverted int        `bigquery:"abs_bytes_reverted" json:"abs_bytes_reverted"`
}

type TopEditsData struct {
	Date             civil.Date `bigquery:"date" json:"date"`
	PageName         string     `bigquery:"page_name" json:"page_name"`
	ViewCount        int        `bigquery:"view_count" json:"view_count"`
	EditCount        int        `bigquery:"edit_count" json:"edit_count"`
	RevertCount      int        `bigquery:"revert_count" json:"revert_count"`
	EditorCount      int        `bigquery:"editor_count" json:"editor_count"`
	NetBytesChanged  int        `bigquery:"net_bytes_changed" json:"net_bytes_changed"`
	AbsBytesChanged  int        `bigquery:"abs_bytes_changed" json:"abs_bytes_changed"`
	AbsBytesReverted int        `bigquery:"abs_bytes_reverted" json:"abs_bytes_reverted"`
}

type TopGrowingData struct {
	Date             civil.Date `bigquery:"date" json:"date"`
	PageName         string     `bigquery:"page_name" json:"page_name"`
	ViewCount        int        `bigquery:"view_count" json:"view_count"`
	EditCount        int        `bigquery:"edit_count" json:"edit_count"`
	RevertCount      int        `bigquery:"revert_count" json:"revert_count"`
	EditorCount      int        `bigquery:"editor_count" json:"editor_count"`
	NetBytesChanged  int        `bigquery:"net_bytes_changed" json:"net_bytes_changed"`
	AbsBytesChanged  int        `bigquery:"abs_bytes_changed" json:"abs_bytes_changed"`
	AbsBytesReverted int        `bigquery:"abs_bytes_reverted" json:"abs_bytes_reverted"`
}

type TopShrinkingData struct {
	Date            civil.Date `bigquery:"date" json:"date"`
	PageName        string     `bigquery:"page_name" json:"page_name"`
	NetBytesChanged int        `bigquery:"net_bytes_changed" json:"net_bytes_changed"`
}

type TopVandalismData struct {
	Date                      civil.Date `bigquery:"date" json:"date"`
	PageName                  string     `bigquery:"page_name" json:"page_name"`
	ViewCount                 int        `bigquery:"view_count" json:"view_count"`
	EditCount                 int        `bigquery:"edit_count" json:"edit_count"`
	RevertCount               int        `bigquery:"revert_count" json:"revert_count"`
	EditorCount               int        `bigquery:"editor_count" json:"editor_count"`
	NetBytesChanged           int        `bigquery:"net_bytes_changed" json:"net_bytes_changed"`
	AbsBytesChanged           int        `bigquery:"abs_bytes_changed" json:"abs_bytes_changed"`
	AbsBytesReverted          int        `bigquery:"abs_bytes_reverted" json:"abs_bytes_reverted"`
	PercentReverted           JSONFloat  `bigquery:"percent_reverted" json:"percent_reverted"`
	AvgBytesRevertedPerRevert JSONFloat  `bigquery:"avg_bytes_reverted_per_revert" json:"avg_bytes_reverted_per_revert"`
}

type TopViewsGainedData struct {
	Date                civil.Date         `bigquery:"date" json:"date"`
	PageName            string             `bigquery:"page_name" json:"page_name"`
	CurrentViewCount    int                `bigquery:"current_view_count" json:"current_view_count"`
	OneDayAgoViewCount  bigquery.NullInt64 `bigquery:"one_day_ago_view_count" json:"one_day_ago_view_count"`
	TwoDaysAgoViewCount bigquery.NullInt64 `bigquery:"two_days_ago_view_count" json:"two_days_ago_view_count"`
	ViewCountRatio      JSONFloat          `bigquery:"view_count_ratio" json:"view_count_ratio"`
}

type TopViewsLostData struct {
	Date                civil.Date         `bigquery:"date" json:"date"`
	PageName            string             `bigquery:"page_name" json:"page_name"`
	CurrentViewCount    int                `bigquery:"current_view_count" json:"current_view_count"`
	OneDayAgoViewCount  bigquery.NullInt64 `bigquery:"one_day_ago_view_count" json:"one_day_ago_view_count"`
	TwoDaysAgoViewCount bigquery.NullInt64 `bigquery:"two_days_ago_view_count" json:"two_days_ago_view_count"`
	ViewCountRatio      JSONFloat          `bigquery:"view_count_ratio" json:"view_count_ratio"`
}

type TopViewsData struct {
	Date             civil.Date         `bigquery:"date" json:"date"`
	PageName         string             `bigquery:"page_name" json:"page_name"`
	ViewCount_0      int                `bigquery:"view_count_0" json:"view_count_0"`
	EditCount        int                `bigquery:"edit_count" json:"edit_count"`
	RevertCount      int                `bigquery:"revert_count" json:"revert_count"`
	EditorCount      int                `bigquery:"editor_count" json:"editor_count"`
	NetBytesChanged  int                `bigquery:"net_bytes_changed" json:"net_bytes_changed"`
	AbsBytesChanged  int                `bigquery:"abs_bytes_changed" json:"abs_bytes_changed"`
	AbsBytesReverted int                `bigquery:"abs_bytes_reverted" json:"abs_bytes_reverted"`
	ViewCount_1      bigquery.NullInt64 `bigquery:"view_count_1" json:"view_count_1"`
	ViewCount_2      bigquery.NullInt64 `bigquery:"view_count_2" json:"view_count_2"`
	ViewCount_3      bigquery.NullInt64 `bigquery:"view_count_3" json:"view_count_3"`
	ViewCount_4      bigquery.NullInt64 `bigquery:"view_count_4" json:"view_count_4"`
	ViewCount_5      bigquery.NullInt64 `bigquery:"view_count_5" json:"view_count_5"`
	ViewCount_6      bigquery.NullInt64 `bigquery:"view_count_6" json:"view_count_6"`
}

type TotalMetadataData struct {
	Date                 civil.Date `bigquery:"date" json:"date"`
	TotalEditCount       int        `bigquery:"total_edit_count" json:"total_edit_count"`
	TotalViewCount       int        `bigquery:"total_view_count" json:"total_view_count"`
	TotalEditorCount     int        `bigquery:"total_editor_count" json:"total_editor_count"`
	TotalRevertCount     int        `bigquery:"total_revert_count" json:"total_revert_count"`
	TotalNetBytesChanged int        `bigquery:"total_net_bytes_changed" json:"total_net_bytes_changed"`
}

type AvailableDate struct {
	Date civil.Date `bigquery:"date" json:"date"`
}

type JSONFloat float64

func (j JSONFloat) MarshalJSON() ([]byte, error) {
	v := float64(j)
	if math.IsInf(v, 0) {
		// handle infinity, assign desired value to v
		// or say +/- indicates infinity
		s := "\"+inf\""
		if math.IsInf(v, -1) {
			s = "\"-inf\""
		}
		return []byte(s), nil
	}
	return json.Marshal(strconv.FormatFloat(v, 'f', -1, 64)) // marshal result as standard float64
}
