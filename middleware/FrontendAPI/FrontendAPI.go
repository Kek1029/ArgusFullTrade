package FrontendAPI

type RouteRequest struct {
	To   int
	Data map[string]interface{}
}

type RouteResponse struct {
	Status    string
	RequestID string
	Result    map[string]interface{}
	Error     string
}

type FrontendAPI interface {
	Route(req RouteRequest) (RouteResponse, error)
}
