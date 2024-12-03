package main

import (
	"context"
	"fmt"
	"os"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
	"google.golang.org/api/option"
)

func fetchTopViewsFromBigQuery() ([]TopViewsData, error) {
	ctx := context.Background()

	credentialsFile := "../" + os.Getenv("PLINY_BIGQUERY_SERVICE_ACCOUNT")
	client, err := bigquery.NewClient(ctx, "pliny-1", option.WithCredentialsFile(credentialsFile))
	if err != nil {
		return nil, fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	query := "SELECT page_name as `article`, view_count as `views` FROM wikipedia_data.intermediate_table_sep where date='2024-09-01' order by view_count desc LIMIT 10"

	it, err := client.Query(query).Read(ctx)
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
