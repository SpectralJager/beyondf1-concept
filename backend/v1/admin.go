package v1

import (
	"beyondf1/backend/data"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"

	jwt "github.com/dgrijalva/jwt-go"
	"golang.org/x/crypto/bcrypt"
)

type Admin struct {
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

func GenerateToken(user string) (string, error) {
	token := jwt.New(jwt.SigningMethodHS256)
	claims := token.Claims.(jwt.MapClaims)
	claims["authorized"] = true
	claims["user"] = user
	claims["exp"] = time.Now().Add(time.Minute * 2).Unix()
	tokenString, err := token.SignedString(MySigningKey)
	if err != nil {
		fmt.Println("[#] Cant generate token")
		log.Println(err)
	}
	return tokenString, nil
}

func Logout(w http.ResponseWriter, r *http.Request) {
	// set headers
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		return
	}
	// Connect to db
	fmt.Println("[#] Hit endpoint: Logout")
	/*cookie := &http.Cookie{
		Name:     "Token",
		Value:    "",
		Path:     "/",
		HttpOnly: true,
		MaxAge:   -1,
	}
	http.SetCookie(w, cookie)*/
	w.Header().Set("Token", "")
	json.NewEncoder(w).Encode(map[string]string{"message": "You are log out!", "code": "success"})
}

func Login(w http.ResponseWriter, r *http.Request) {
	// set headers
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		return
	}
	// Connect to db
	fmt.Println("[#] Hit endpoint: Login")
	db := data.ConnectDB()
	defer db.Close()
	// fetch data from site
	var admin Admin
	reqBody, err := ioutil.ReadAll(r.Body)
	json.Unmarshal(reqBody, &admin)
	if err != nil {
		fmt.Println("[#] Cant decode request json!")
		json.NewEncoder(w).Encode(map[string]string{"message": "Data incorect or mising!"})
		log.Println(err)
		return
	}
	sql_statement := `select password from admins where username=$1;`
	row := db.QueryRow(sql_statement, admin.Username)
	var password string
	err = row.Scan(&password)
	if err != nil {
		fmt.Println("[#] Cant feth data from db!")
		json.NewEncoder(w).Encode(map[string]string{"message": "Data missing or id incorect"})
		log.Println(err)
		return
	}
	err = bcrypt.CompareHashAndPassword([]byte(password), []byte(admin.Password))
	if err != nil {
		fmt.Println("[#] Incorect passwords!")
		json.NewEncoder(w).Encode(map[string]string{"message": "Invalid or missing credentials!"})
		log.Println(err)
		return
	}
	token, err := GenerateToken(admin.Username)
	if err != nil {
		log.Println(err)
	}
	/*cookie := &http.Cookie{
		Name:     "Token",
		Value:    token,
		Path:     "/",
		HttpOnly: true,
		Expires:  time.Now().Add(time.Hour * 10),
	}
	http.SetCookie(w, cookie)*/
	w.Header().Add("Token", token)
	json.NewEncoder(w).Encode(map[string]string{"message": "You are login in!", "code": "success"})
}

func CreateAdmin(w http.ResponseWriter, r *http.Request) {
	// set headers
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		return
	}
	if r.Header["Token"] != nil {
		token, err := jwt.Parse(r.Header["Token"][0], func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("cant pars token")
			}
			return MySigningKey, nil
		})
		if err != nil {
			log.Println(err)
			w.Header().Set("Token", "")
			json.NewEncoder(w).Encode(map[string]string{"message": "unauthorized"})
		}
		if token.Valid {
			// Connect to db
			fmt.Println("[#] Hit endpoint: Login")
			db := data.ConnectDB()
			defer db.Close()
			// fetch data from site
			var admin Admin
			reqBody, err := ioutil.ReadAll(r.Body)
			json.Unmarshal(reqBody, &admin)
			if err != nil {
				fmt.Println("[#] Cant decode request json!")
				json.NewEncoder(w).Encode(map[string]string{"message": "Data incorect or mising!"})
				log.Println(err)
				return
			}
			hash, err := bcrypt.GenerateFromPassword([]byte(admin.Password), bcrypt.DefaultCost)
			if err != nil {
				log.Println(err)
			}
			admin.Password = string(hash)
			sql_statement := `insert into admins (username, email, password) values ($1, $2, $3);`
			_, err = db.Exec(
				sql_statement,
				admin.Username, admin.Email, admin.Password,
			)
			if err != nil {
				fmt.Println("[#] Cant insert data to database!")
				json.NewEncoder(w).Encode(map[string]string{"message": "Data incorect or mising!"})
				log.Println(err)
				return
			}
			json.NewEncoder(w).Encode(map[string]string{"message": fmt.Sprintf("New admin created! Username: %s", admin.Username)})
		}
	} else {
		json.NewEncoder(w).Encode(map[string]string{"message": "unauthorized"})
	}
}

func DeleteAdmin(w http.ResponseWriter, r *http.Request) {
	// set headers
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		return

	}
	if r.Header["Token"] != nil {
		token, err := jwt.Parse(r.Header["Token"][0], func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("cant pars token")
			}
			return MySigningKey, nil
		})
		if err != nil {
			log.Println(err)
			w.Header().Set("Token", "")
			json.NewEncoder(w).Encode(map[string]string{"message": "unauthorized"})
		}
		if token.Valid {
			// Connect to db
			fmt.Println("[#] Hit endpoint: DeleteAdmin")
			db := data.ConnectDB()
			defer db.Close()
			// fetch data from site
			cookie, err := r.Cookie("beyondf1")
			if err != nil {
				fmt.Println("[#] Cookies not found!")
				json.NewEncoder(w).Encode(map[string]string{"message": "Data incorect or mising!"})
				log.Println(err)
				return
			}
			sql_statement := `delete from admins where username=$1;`
			res, err := db.Exec(sql_statement, cookie.Value)
			rows_affected, _ := res.RowsAffected()
			if err != nil || rows_affected == 0 {
				fmt.Println("[#] Cant delete data!")
				json.NewEncoder(w).Encode(map[string]string{"message": "Data incorect or mising!"})
				log.Println(err)
				return
			}
			json.NewEncoder(w).Encode(map[string]string{"message": "Data updated! Admin deleted."})
		}
	} else {
		json.NewEncoder(w).Encode(map[string]string{"message": "unauthorized"})
	}

}
