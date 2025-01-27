package main

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func main() {
	// Setup bigquery client
	err := initBigQueryClient()
	if err != nil {
		panic(err)
	}

	router := gin.Default()
	router.GET("/topViews/:date/:limit", getTopViews)
	router.Run("localhost:8080")
}

func getTopViews(c *gin.Context) {
	date := c.Param("date")
	limit, err := strconv.Atoi(c.Param("limit"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid limit parameter"})
		return
	}

	views, err := fetchTopViewsFromBigQuery(date, limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusOK, views)
}
