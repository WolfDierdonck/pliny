package main

import (
	"context"
	"fmt"
	"os"
	"strings"
	"time"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
	"google.golang.org/api/option"
)

type BigQueryClient struct {
	client  *bigquery.Client
	queries map[string]string
	limiter RateLimiter
}

func (bqc *BigQueryClient) getTopEditorsQuery(date string, limit int) (*string, error) {
	if !bqc.limiter.Allow() {
		return nil, fmt.Errorf("rate limit exceeded")
	}

	query := bqc.queries["fetch_top_editors.sql"]
	query = strings.ReplaceAll(query, "{{date}}", fmt.Sprintf("'%s'", date))
	query = strings.ReplaceAll(query, "{{limit}}", fmt.Sprintf("%d", limit))

	return &query, nil
}

func (bqc *BigQueryClient) getTopEditsQuery(date string, limit int) (*string, error) {
	if !bqc.limiter.Allow() {
		return nil, fmt.Errorf("rate limit exceeded")
	}

	query := bqc.queries["fetch_top_edits.sql"]
	query = strings.ReplaceAll(query, "{{date}}", fmt.Sprintf("'%s'", date))
	query = strings.ReplaceAll(query, "{{limit}}", fmt.Sprintf("%d", limit))

	return &query, nil
}

func (bqc *BigQueryClient) getTopGrowingQuery(date string, limit int) (*string, error) {
	if !bqc.limiter.Allow() {
		return nil, fmt.Errorf("rate limit exceeded")
	}

	query := bqc.queries["fetch_top_growing.sql"]
	query = strings.ReplaceAll(query, "{{date}}", fmt.Sprintf("'%s'", date))
	query = strings.ReplaceAll(query, "{{limit}}", fmt.Sprintf("%d", limit))

	return &query, nil
}

func (bqc *BigQueryClient) getTopShrinkingQuery(date string, limit int) (*string, error) {
	if !bqc.limiter.Allow() {
		return nil, fmt.Errorf("rate limit exceeded")
	}

	query := bqc.queries["fetch_top_shrinking.sql"]
	query = strings.ReplaceAll(query, "{{date}}", fmt.Sprintf("'%s'", date))
	query = strings.ReplaceAll(query, "{{limit}}", fmt.Sprintf("%d", limit))

	return &query, nil
}

func (bqc *BigQueryClient) getTopVandalismQuery(date string, limit int) (*string, error) {
	if !bqc.limiter.Allow() {
		return nil, fmt.Errorf("rate limit exceeded")
	}

	query := bqc.queries["fetch_top_vandalism.sql"]
	query = strings.ReplaceAll(query, "{{date}}", fmt.Sprintf("'%s'", date))
	query = strings.ReplaceAll(query, "{{limit}}", fmt.Sprintf("%d", limit))

	return &query, nil
}

func (bqc *BigQueryClient) getTopViewsGainedQuery(date string, limit int) (*string, error) {
	if !bqc.limiter.Allow() {
		return nil, fmt.Errorf("rate limit exceeded")
	}

	query := bqc.queries["fetch_top_views_gained.sql"]
	query = strings.ReplaceAll(query, "{{date}}", fmt.Sprintf("'%s'", date))
	query = strings.ReplaceAll(query, "{{limit}}", fmt.Sprintf("%d", limit))

	return &query, nil
}

func (bqc *BigQueryClient) getTopViewsLostQuery(date string, limit int) (*string, error) {
	if !bqc.limiter.Allow() {
		return nil, fmt.Errorf("rate limit exceeded")
	}

	query := bqc.queries["fetch_top_views_lost.sql"]
	query = strings.ReplaceAll(query, "{{date}}", fmt.Sprintf("'%s'", date))
	query = strings.ReplaceAll(query, "{{limit}}", fmt.Sprintf("%d", limit))

	return &query, nil
}

func (bqc *BigQueryClient) getTopViewsQuery(date string, limit int) (*string, error) {
	if !bqc.limiter.Allow() {
		return nil, fmt.Errorf("rate limit exceeded")
	}

	query := bqc.queries["fetch_top_views.sql"]
	query = strings.ReplaceAll(query, "{{date}}", fmt.Sprintf("'%s'", date))
	query = strings.ReplaceAll(query, "{{limit}}", fmt.Sprintf("%d", limit))

	return &query, nil
}

func (bqc *BigQueryClient) getTotalMetadataQuery(date string) (*string, error) {
	if !bqc.limiter.Allow() {
		return nil, fmt.Errorf("rate limit exceeded")
	}

	query := bqc.queries["fetch_total_metadata.sql"]
	query = strings.ReplaceAll(query, "{{date}}", fmt.Sprintf("'%s'", date))

	return &query, nil
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

	bqClient.limiter = NewRateLimiter(600, 30*time.Second)

	return nil
}

func FetchRows[T any](it *bigquery.RowIterator) ([]T, error) {
	var rows []T
	for {
		var row T
		err := it.Next(&row)
		if err == iterator.Done {
			break
		}
		if err != nil {
			return nil, fmt.Errorf("it.Next: %v", err)
		}
		rows = append(rows, row)
	}
	return rows, nil
}

func fetchTopEditorsFromBigQuery(date string, limit int) ([]TopEditorsData, error) {
	ctx := context.Background()

	if bqClient.client == nil {
		return nil, fmt.Errorf("BigQuery client is not initialized")
	}

	query, err := bqClient.getTopEditorsQuery(date, limit)
	if err != nil {
		return nil, err
	}

	it, err := bqClient.client.Query(*query).Read(ctx)
	if err != nil {
		return nil, fmt.Errorf("client.Query: %v", err)
	}

	rows, err := FetchRows[TopEditorsData](it)
	if err != nil {
		return nil, err
	}
	return rows, nil
}

func fetchTopEditsFromBigQuery(date string, limit int) ([]TopEditsData, error) {
	ctx := context.Background()

	if bqClient.client == nil {
		return nil, fmt.Errorf("BigQuery client is not initialized")
	}

	query, err := bqClient.getTopEditsQuery(date, limit)
	if err != nil {
		return nil, err
	}

	it, err := bqClient.client.Query(*query).Read(ctx)
	if err != nil {
		return nil, fmt.Errorf("client.Query: %v", err)
	}

	rows, err := FetchRows[TopEditsData](it)
	if err != nil {
		return nil, err
	}
	return rows, nil
}

func fetchTopGrowingFromBigQuery(date string, limit int) ([]TopGrowingData, error) {
	ctx := context.Background()

	if bqClient.client == nil {
		return nil, fmt.Errorf("BigQuery client is not initialized")
	}

	query, err := bqClient.getTopGrowingQuery(date, limit)
	if err != nil {
		return nil, err
	}

	it, err := bqClient.client.Query(*query).Read(ctx)
	if err != nil {
		return nil, fmt.Errorf("client.Query: %v", err)
	}

	rows, err := FetchRows[TopGrowingData](it)
	if err != nil {
		return nil, err
	}
	return rows, nil
}

func fetchTopShrinkingFromBigQuery(date string, limit int) ([]TopShrinkingData, error) {
	ctx := context.Background()

	if bqClient.client == nil {
		return nil, fmt.Errorf("BigQuery client is not initialized")
	}

	query, err := bqClient.getTopShrinkingQuery(date, limit)
	if err != nil {
		return nil, err
	}

	it, err := bqClient.client.Query(*query).Read(ctx)
	if err != nil {
		return nil, fmt.Errorf("client.Query: %v", err)
	}

	rows, err := FetchRows[TopShrinkingData](it)
	if err != nil {
		return nil, err
	}
	return rows, nil
}

func fetchTopVandalismFromBigQuery(date string, limit int) ([]TopVandalismData, error) {
	ctx := context.Background()

	if bqClient.client == nil {
		return nil, fmt.Errorf("BigQuery client is not initialized")
	}

	query, err := bqClient.getTopVandalismQuery(date, limit)
	if err != nil {
		return nil, err
	}

	it, err := bqClient.client.Query(*query).Read(ctx)
	if err != nil {
		return nil, fmt.Errorf("client.Query: %v", err)
	}

	rows, err := FetchRows[TopVandalismData](it)
	if err != nil {
		return nil, err
	}
	return rows, nil
}

func fetchTopViewsGainedFromBigQuery(date string, limit int) ([]TopViewsGainedData, error) {
	ctx := context.Background()

	if bqClient.client == nil {
		return nil, fmt.Errorf("BigQuery client is not initialized")
	}

	query, err := bqClient.getTopViewsGainedQuery(date, limit)
	if err != nil {
		return nil, err
	}

	it, err := bqClient.client.Query(*query).Read(ctx)
	if err != nil {
		return nil, fmt.Errorf("client.Query: %v", err)
	}

	rows, err := FetchRows[TopViewsGainedData](it)
	if err != nil {
		return nil, err
	}
	return rows, nil
}

func fetchTopViewsLostFromBigQuery(date string, limit int) ([]TopViewsLostData, error) {
	ctx := context.Background()

	if bqClient.client == nil {
		return nil, fmt.Errorf("BigQuery client is not initialized")
	}

	query, err := bqClient.getTopViewsLostQuery(date, limit)
	if err != nil {
		return nil, err
	}

	it, err := bqClient.client.Query(*query).Read(ctx)
	if err != nil {
		return nil, fmt.Errorf("client.Query: %v", err)
	}

	rows, err := FetchRows[TopViewsLostData](it)
	if err != nil {
		return nil, err
	}
	return rows, nil
}

func fetchTopViewsFromBigQuery(date string, limit int) ([]TopViewsData, error) {
	ctx := context.Background()

	if bqClient.client == nil {
		return nil, fmt.Errorf("BigQuery client is not initialized")
	}

	query, err := bqClient.getTopViewsQuery(date, limit)
	if err != nil {
		return nil, err
	}

	it, err := bqClient.client.Query(*query).Read(ctx)
	if err != nil {
		return nil, fmt.Errorf("client.Query: %v", err)
	}

	rows, err := FetchRows[TopViewsData](it)
	if err != nil {
		return nil, err
	}
	return rows, nil
}

func fetchTotalMetadataFromBigQuery(date string) ([]TotalMetadataData, error) {
	ctx := context.Background()

	if bqClient.client == nil {
		return nil, fmt.Errorf("BigQuery client is not initialized")
	}

	query, err := bqClient.getTotalMetadataQuery(date)
	if err != nil {
		return nil, err
	}

	it, err := bqClient.client.Query(*query).Read(ctx)
	if err != nil {
		return nil, fmt.Errorf("client.Query: %v", err)
	}

	rows, err := FetchRows[TotalMetadataData](it)
	if err != nil {
		return nil, err
	}
	return rows, nil
}
