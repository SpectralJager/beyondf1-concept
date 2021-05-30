package middleware

import (
	"encoding/base64"
	"encoding/json"
	"log"
	"net/http"

	"beyondf1/backend/data"
)

func MiddlewareCORS(next http.Handler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// set cors headers
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
		//w.Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
		if r.Method == "OPTIONS" {
			log.Printf("Option request for %s from %s", r.RequestURI, r.RemoteAddr)
			w.WriteHeader(http.StatusOK)
			return
		}
		// call endpoint
		next.ServeHTTP(w, r)
	}
}

func MiddlewareAUTH(next http.Handler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		session, err := r.Cookie("auth")
		if err != nil {
			log.Println("Cant find auth cookies")
			log.Fatalln(err)
			json.NewEncoder(w).Encode(map[string]string{"auth": "false"})
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		value, err := base64.StdEncoding.DecodeString(session.Value)
		if err != nil {
			log.Println("Cant decode cookies")
			log.Fatalln(err)
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{"auth": "false"})
			return
		}
		var cred data.Credentials
		err = json.Unmarshal(value, &cred)
		if err != nil {
			log.Println("Cant parse cokies")
			log.Fatalln(err)
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{"auth": "false"})
			return
		}
		err = data.CheckCredentials(&cred)
		if err != nil {
			log.Println("Unauthorize access")
			log.Fatalln(err)
			w.WriteHeader(http.StatusNotAcceptable)
			json.NewEncoder(w).Encode(map[string]string{"auth": "false"})
			return
		}
		log.Println("User identificated")
		w.WriteHeader(http.StatusOK)
		next.ServeHTTP(w, r)
	}
}
