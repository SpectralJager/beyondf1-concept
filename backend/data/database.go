package data

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/lib/pq"
)

// db info
const (
	host     = "localhost"
	port     = 5432
	username = "postgres"
	password = "238516"
	dbname   = "beyondf1"
)

// sql statements
// admin
const (
	adminTable = `
	create table if not exists admin (
		id integer primary key,
		username varchar(64) not null unique,
		email varchar(126) not null unique,
		password varchar(512) not null,
		token varchar(32) not null
	);
	`
	getAdmin = `select * from admin where username = $1, token = $2;`
)

// structures
type Admin struct {
	ID       int    `json:"id" sql:"id"`
	Username string `json:"username" sql:"username"`
	Email    string `json:"email" sql:"email"`
	Password string `json:"password" sql:"password"`
	Token    string `json:"token" sql:"token"`
}
type Credentials struct {
	Username string `json:"username" sql:"username"`
	Token    string `json:"token" sql:"token"`
}

// functions
func ConnectDB() (*sql.DB, error) {
	psqlInfo := fmt.Sprintf(
		"host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, username, password, dbname,
	)
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		log.Println("Cant connect to db")
		log.Fatalln(err)
		return db, err
	}
	err = db.Ping()
	log.Println("Db connected")
	return db, err
}

func CreateTables() {
	db, err := ConnectDB()
	if err != nil {
		log.Println("Cant connect to db")
		log.Fatalln(err)
		return
	}
	_, err = db.Exec(adminTable)
	if err != nil {
		log.Fatalln(err)
		return
	}
}

func CheckCredentials(cred *Credentials) error {
	db, err := ConnectDB()
	if err != nil {
		log.Println("Cant connect to db")
		log.Fatalln(err)
		return err
	}
	res, err := db.Exec(adminTable)
	rows, _ := res.RowsAffected()
	if err != nil || rows == 0 {
		log.Fatalln(err)
		return fmt.Errorf("not such admin")
	}
	return nil
}
