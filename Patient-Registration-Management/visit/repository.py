package visit

import "gorm.io/gorm"

type VisitRepository struct {
    DB *gorm.DB
}

func (r *VisitRepository) CreateVisit(visit *Visit) error {
    return r.DB.Create(visit).Error
}

func (r *VisitRepository) GetVisitByID(id uint) (*Visit, error) {
    var visit Visit
    err := r.DB.First(&visit, id).Error
    return &visit, err
}

func (r *VisitRepository) GetAllVisits() ([]Visit, error) {
    var visits []Visit
    err := r.DB.Find(&visits).Error
    return visits, err
}

func (r *VisitRepository) UpdateVisit(visit *Visit) error {
    return r.DB.Save(visit).Error
}

func (r *VisitRepository) DeleteVisit(id uint) error {
    return r.DB.Delete(&Visit{}, id).Error
}
