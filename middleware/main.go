package main

import (
	"fmt"
	"middleware/Config"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"middleware/BybitAPI"
)

func main() {
	cfg, err := Config.GetConfigEnv()
	if err != nil {
		panic(err)
	}

	r := chi.NewRouter()
	r.Use(middleware.Logger)
	r.Post("/route", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"message": "Hello World"}`))
	})
	port := cfg.MiddlewarePort

	bybitApi := BybitAPI.New(cfg)
	println(bybitApi.GetBalance())

	err = http.ListenAndServe(fmt.Sprintf(":%d", port), r)
	if err != nil {
		panic(err)
	}

}
