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
		cookie, err := r.Cookie("Token")
		if err != nil {
			json.NewEncoder(w).Encode(map[string]string{"message": "unauthorized"})
		} else {
			token, err := jwt.Parse(cookie.Value, func(token *jwt.Token) (interface{}, error) {
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
		}
	})
}
