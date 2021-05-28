package main

import (
	"fmt"
	"net/http"

	v1 "beyondf1/backend/v1"

	"github.com/gorilla/mux"
	_ "github.com/lib/pq"
)

func CreateServer() {
	multiplexer := mux.NewRouter()
	go api_v1(multiplexer, "/api/v1")
	http.ListenAndServe("0.0.0.0:8000", multiplexer)
}

func api_v1(mul *mux.Router, prefix string) {
	mul.HandleFunc(fmt.Sprintf("%s%s", prefix, "/articles"), v1.GetArticles).Methods("GET", "OPTIONS")
	mul.HandleFunc(fmt.Sprintf("%s%s", prefix, "/articles"), v1.SetArticle).Methods("POST", "OPTIONS")
	mul.HandleFunc(fmt.Sprintf("%s%s", prefix, "/articles/tag={tag}"), v1.GetArticlesByTag).Methods("GET", "OPTIONS")
	mul.HandleFunc(fmt.Sprintf("%s%s", prefix, "/articles/id={id}"), v1.GetArticle).Methods("GET", "OPTIONS")
	mul.HandleFunc(fmt.Sprintf("%s%s", prefix, "/articles/id={id}"), v1.PutArticle).Methods("PUT", "OPTIONS")
	mul.HandleFunc(fmt.Sprintf("%s%s", prefix, "/articles/id={id}"), v1.DeleteArticle).Methods("DELETE", "OPTIONS")
}
