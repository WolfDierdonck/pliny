package main

import "cloud.google.com/go/civil"

type TopViewsData struct {
	Date      civil.Date `bigquery:"date" json:"date"`
	PageName  string     `bigquery:"page_name" json:"page_name"`
	ViewCount int        `bigquery:"view_count" json:"view_count"`
}

type MockData struct {
	Date     civil.Date `bigquery:"date" json:"date"`
	PageName string     `bigquery:"page_name" json:"page_name"`
}
