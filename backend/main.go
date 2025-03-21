package main

import (
	"net/http"
	"strconv"
	"time"

	"github.com/gin-contrib/cache"
	"github.com/gin-contrib/cache/persistence"
	"github.com/gin-gonic/gin"
)

func main() {
	// Setup bigquery client
	err := initBigQueryClient()
	if err != nil {
		panic(err)
	}

	store := persistence.NewInMemoryStore(time.Hour)

	router := gin.Default()
	router.GET("/topEditors/:date/:limit", cache.CachePage(store, time.Hour, getTopEditors))
	router.GET("/topEdits/:date/:limit", cache.CachePage(store, time.Hour, getTopEdits))
	router.GET("/topGrowing/:date/:limit", cache.CachePage(store, time.Hour, getTopGrowing))
	router.GET("/topShrinking/:date/:limit", cache.CachePage(store, time.Hour, getTopShrinking))
	router.GET("/topVandalism/:date/:limit", cache.CachePage(store, time.Hour, getTopVandalism))
	router.GET("/topViewsGained/:date/:limit", cache.CachePage(store, time.Hour, getTopViewsGained))
	router.GET("/topViewsLost/:date/:limit", cache.CachePage(store, time.Hour, getTopViewsLost))
	router.GET("/topViews/:date/:limit", cache.CachePage(store, time.Hour, getTopViews))
	router.GET("/totalMetadata/:date", cache.CachePage(store, time.Hour, getTotalMetadata))
	router.GET("/availableDates", cache.CachePage(store, time.Hour, getAvailableDates))
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

func getTopShrinking(c *gin.Context) {
	date := c.Param("date")
	limit, err := strconv.Atoi(c.Param("limit"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid limit parameter"})
		return
	}

	shrinking, err := fetchTopShrinkingFromBigQuery(date, limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusOK, shrinking)
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

func getTopViewsGained(c *gin.Context) {
	date := c.Param("date")
	limit, err := strconv.Atoi(c.Param("limit"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid limit parameter"})
		return
	}

	viewDelta, err := fetchTopViewsGainedFromBigQuery(date, limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusOK, viewDelta)
}

func getTopViewsLost(c *gin.Context) {
	date := c.Param("date")
	limit, err := strconv.Atoi(c.Param("limit"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid limit parameter"})
		return
	}

	viewDelta, err := fetchTopViewsLostFromBigQuery(date, limit)
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

func getAvailableDates(c *gin.Context) {
	dates, err := fetchAvailableDatesFromBigQuery()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusOK, dates)
}