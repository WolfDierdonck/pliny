package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	router.GET("/topViews", getTopViews)
	router.Run("localhost:8080")
}

func getTopViews(c *gin.Context) {
	views, err := fetchTopViewsFromBigQuery()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusOK, views)
}
