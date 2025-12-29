package visit

import "github.com/gin-gonic/gin"

func RegisterVisitRoutes(router *gin.Engine, controller *VisitController) {
    visit := router.Group("/visits")
    {
        visit.POST("/", controller.CreateVisit)
        visit.GET("/", controller.GetAllVisits)
        visit.GET("/:id", controller.GetVisitByID)
        visit.PUT("/", controller.UpdateVisit)
        visit.DELETE("/:id", controller.DeleteVisit)
    }
}
