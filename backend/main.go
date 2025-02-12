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
	router.GET("/topEditors/:date/:limit", getTopEditors)
	router.GET("/topEdits/:date/:limit", getTopEdits)
	router.GET("/topGrowing/:date/:limit", getTopGrowing)
	router.GET("/topVandalism/:date/:limit", getTopVandalism)
	router.GET("/topViewDelta/:date/:limit", getTopViewDelta)
	router.GET("/topViews/:date/:limit", getTopViews)
	router.GET("/totalMetadata/:date", getTotalMetadata)
	router.GET("/wikipediaGrowth/:date", getWikipediaGrowth)
	router.Run("localhost:8080")
}

func getTopEditors(c *gin.Context) {
	date := c.Param("date")
	limit, err := strconv.Atoi(c.Param("limit"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid limit parameter"})
		return
	}

	editors, err := fetchTopEditorsFromBigQuery(date, limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusOK, editors)
}

func getTopEdits(c *gin.Context) {
	date := c.Param("date")
	limit, err := strconv.Atoi(c.Param("limit"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid limit parameter"})
		return
	}

	edits, err := fetchTopEditsFromBigQuery(date, limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusOK, edits)
}

func getTopGrowing(c *gin.Context) {
	date := c.Param("date")
	limit, err := strconv.Atoi(c.Param("limit"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid limit parameter"})
		return
	}

	growing, err := fetchTopGrowingFromBigQuery(date, limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusOK, growing)
}

func getTopVandalism(c *gin.Context) {
	date := c.Param("date")
	limit, err := strconv.Atoi(c.Param("limit"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid limit parameter"})
		return
	}

	vandalism, err := fetchTopVandalismFromBigQuery(date, limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusOK, vandalism)
}

func getTopViewDelta(c *gin.Context) {
	date := c.Param("date")
	limit, err := strconv.Atoi(c.Param("limit"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid limit parameter"})
		return
	}

	viewDelta, err := fetchTopViewDeltaFromBigQuery(date, limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusOK, viewDelta)
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

func getTotalMetadata(c *gin.Context) {
	date := c.Param("date")

	metadata, err := fetchTotalMetadataFromBigQuery(date)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusOK, metadata)
}

func getWikipediaGrowth(c *gin.Context) {
	date := c.Param("date")

	growth, err := fetchWikipediaGrowthFromBigQuery(date)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusOK, growth)
}
