package main

import (
	"beyondf1/backend/data"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	// create database's tables
	data.CreateTables()
	log.Println("database work")
	// create router
	router := mux.NewRouter()
	// routes

	// server
	const addr = "0.0.0.0:8000"
	log.Printf("Start listening on %s ...", addr)
	err := http.ListenAndServe(addr, router)
	log.Fatal(err)
}
