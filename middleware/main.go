package main

import (
	"fmt"
	"net/http"
	"os"

	bybit "github.com/bybit-exchange/bybit.go.api"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

func main() {
	r := chi.NewRouter()
	r.Use(middleware.Logger)
	r.Post("/route", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"message": "Hello World"}`))
	})
	port, exists := os.LookupEnv("MIDDLEWARE_PORT")
	if !exists {
		port = "6132"
	}

	err := http.ListenAndServe(fmt.Sprintf(":%s", port), r)
	if err != nil {
		panic(err)
	}
}
