package v1

import (
	"beyondf1/backend/data"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"golang.org/x/crypto/bcrypt"
)

type Admin struct {
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"password"`
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
	hash, err = bcrypt.GenerateFromPassword([]byte(admin.Username), bcrypt.DefaultCost)
	if err != nil {
		log.Println(err)
		return
	}
	cookie := &http.Cookie{
		Name:   "beyondf1",
		Value:  string(hash),
		Path:   "/",
		MaxAge: 86400, // One day
	}
	http.SetCookie(w, cookie)
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

func DeleteAdmin(w http.ResponseWriter, r *http.Request) {
	// set headers
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		return
	}
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
