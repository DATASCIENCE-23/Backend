package visit

type VisitService struct {
    Repo *VisitRepository
}

func (s *VisitService) CreateVisit(visit *Visit) error {
    visit.Status = "ACTIVE"
    return s.Repo.CreateVisit(visit)
}

func (s *VisitService) GetVisitByID(id uint) (*Visit, error) {
    return s.Repo.GetVisitByID(id)
}

func (s *VisitService) GetAllVisits() ([]Visit, error) {
    return s.Repo.GetAllVisits()
}

func (s *VisitService) UpdateVisit(visit *Visit) error {
    return s.Repo.UpdateVisit(visit)
}

func (s *VisitService) DeleteVisit(id uint) error {
    return s.Repo.DeleteVisit(id)
}
