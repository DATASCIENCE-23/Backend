package visit

import (
    "gorm.io/gorm"
)

func InitVisitModule(db *gorm.DB) *VisitController {
    repo := &VisitRepository{DB: db}
    service := &VisitService{Repo: repo}
    controller := &VisitController{Service: service}
    return controller
}
