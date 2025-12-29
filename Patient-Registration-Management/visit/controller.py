package visit

import (
    "net/http"
    "strconv"

    "github.com/gin-gonic/gin"
)

type VisitController struct {
    Service *VisitService
}

func (c *VisitController) CreateVisit(ctx *gin.Context) {
    var visit Visit
    if err := ctx.ShouldBindJSON(&visit); err != nil {
        ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    err := c.Service.CreateVisit(&visit)
    if err != nil {
        ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    ctx.JSON(http.StatusCreated, visit)
}

func (c *VisitController) GetVisitByID(ctx *gin.Context) {
    id, _ := strconv.Atoi(ctx.Param("id"))
    visit, err := c.Service.GetVisitByID(uint(id))
    if err != nil {
        ctx.JSON(http.StatusNotFound, gin.H{"error": "Visit not found"})
        return
    }
    ctx.JSON(http.StatusOK, visit)
}

func (c *VisitController) GetAllVisits(ctx *gin.Context) {
    visits, _ := c.Service.GetAllVisits()
    ctx.JSON(http.StatusOK, visits)
}

func (c *VisitController) UpdateVisit(ctx *gin.Context) {
    var visit Visit
    ctx.ShouldBindJSON(&visit)
    c.Service.UpdateVisit(&visit)
    ctx.JSON(http.StatusOK, visit)
}

func (c *VisitController) DeleteVisit(ctx *gin.Context) {
    id, _ := strconv.Atoi(ctx.Param("id"))
    c.Service.DeleteVisit(uint(id))
    ctx.JSON(http.StatusOK, gin.H{"message": "Visit deleted"})
}
