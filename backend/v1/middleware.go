package v1

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	jwt "github.com/dgrijalva/jwt-go"
)

var MySigningKey = []byte("MysyperpupersigIngnkey")

func IsAuth(endpoint func(http.ResponseWriter, *http.Request)) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Header["Token"] != nil {
			token, err := jwt.Parse(r.Header["Token"][0], func(token *jwt.Token) (interface{}, error) {
				if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
					return nil, fmt.Errorf("cant pars token")
				}
				return MySigningKey, nil
			})
			if err != nil {
				log.Println(err)
				json.NewEncoder(w).Encode(map[string]string{"message": "unauthorized"})
			}
			if token.Valid {
				endpoint(w, r)
			}
		} else {
			json.NewEncoder(w).Encode(map[string]string{"message": "unauthorized"})
		}
	})
}
