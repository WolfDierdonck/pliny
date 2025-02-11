package main

import (
	"context"
	"fmt"
	"os"
	"strings"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
	"google.golang.org/api/option"
)

type BigQueryClient struct {
	client  *bigquery.Client
	queries map[string]string
}

func (bqc *BigQueryClient) getTopViewsQuery(date string, limit int) string {
	query := bqc.queries["fetch_top_views.sql"]
	query = strings.ReplaceAll(query, "{{date}}", fmt.Sprintf("'%s'", date))
	query = strings.ReplaceAll(query, "{{limit}}", fmt.Sprintf("%d", limit))

	return query
}

func (bqc *BigQueryClient) getTopVandalismQuery(startDate string, endDate string, limit int) string {
	query := bqc.queries["fetch_top_vandalism.sql"]
	query = strings.ReplaceAll(query, "{{startDate}}", fmt.Sprintf("'%s'", startDate))
	query = strings.ReplaceAll(query, "{{endDate}}", fmt.Sprintf("'%s'", endDate))
	query = strings.ReplaceAll(query, "{{limit}}", fmt.Sprintf("%d", limit))

	return query
}

func (bqc *BigQueryClient) getTopGrowingQuery(date string, limit int) string {
	query := bqc.queries["fetch_top_growing.sql"]
	query = strings.ReplaceAll(query, "{{date}}", fmt.Sprintf("'%s'", date))
	query = strings.ReplaceAll(query, "{{limit}}", fmt.Sprintf("%d", limit))

	return query
}

var bqClient BigQueryClient

func initBigQueryClient() error {
	// Init the client
	ctx := context.Background()
	credentialsFile := "../" + os.Getenv("PLINY_BIGQUERY_SERVICE_ACCOUNT")
	client, err := bigquery.NewClient(ctx, "pliny-1", option.WithCredentialsFile(credentialsFile))
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	bqClient = BigQueryClient{client: client}

	// Now, load all the files from the ./queries directory into the queries map
	path := "./queries"
	files, err := os.ReadDir(path)
	if err != nil {
		return fmt.Errorf("os.ReadDir: %v", err)
	}

	bqClient.queries = make(map[string]string)
	for _, file := range files {
		query, err := os.ReadFile(path + "/" + file.Name())
		if err != nil {
			return fmt.Errorf("os.ReadFile: %v", err)
		}

		bqClient.queries[file.Name()] = string(query)
	}

	return nil
}

func fetchTopViewsFromBigQuery(date string, limit int) ([]TopViewsData, error) {
	ctx := context.Background()

	if bqClient.client == nil {
		return nil, fmt.Errorf("BigQuery client is not initialized")
	}

	query := bqClient.getTopViewsQuery(date, limit)
	it, err := bqClient.client.Query(query).Read(ctx)
	if err != nil {
		return nil, fmt.Errorf("client.Query: %v", err)
	}

	var views []TopViewsData
	for {
		var row TopViewsData
		err := it.Next(&row)
		if err == iterator.Done {
			break
		}
		if err != nil {
			return nil, fmt.Errorf("it.Next: %v", err)
		}
		views = append(views, row)
	}
	return views, nil
}

func fetchTopVandalismFromBigQuery(startDate string, endDate string, limit int) ([]TopVandalismData, error) {
	ctx := context.Background()

	if bqClient.client == nil {
		return nil, fmt.Errorf("BigQuery client is not initialized")
	}

	query := bqClient.getTopVandalismQuery(startDate, endDate, limit)
	it, err := bqClient.client.Query(query).Read(ctx)
	if err != nil {
		return nil, fmt.Errorf("client.Query: %v", err)
	}

	var vandalism []TopVandalismData
	for {
		var row TopVandalismData
		err := it.Next(&row)
		if err == iterator.Done {
			break
		}
		if err != nil {
			return nil, fmt.Errorf("it.Next: %v", err)
		}
		vandalism = append(vandalism, row)
	}
	return vandalism, nil
}

func fetchTopGrowingFromBigQuery(date string, limit int) ([]TopGrowingData, error) {
	ctx := context.Background()

	if bqClient.client == nil {
		return nil, fmt.Errorf("BigQuery client is not initialized")
	}

	query := bqClient.getTopGrowingQuery(date, limit)
	it, err := bqClient.client.Query(query).Read(ctx)
	if err != nil {
		return nil, fmt.Errorf("client.Query: %v", err)
	}

	var growing []TopGrowingData
	for {
		var row TopGrowingData
		err := it.Next(&row)
		if err == iterator.Done {
			break
		}
		if err != nil {
			return nil, fmt.Errorf("it.Next: %v", err)
		}
		growing = append(growing, row)
	}
	return growing, nil
}
