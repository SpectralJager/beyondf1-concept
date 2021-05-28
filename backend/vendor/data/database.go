package data

import (
	"database/sql"
	"fmt"
	"log"
)

const (
	host     = "localhost"
	port     = "5432"
	user     = "postgres"
	password = "238516"
	dbname   = "beyondf1"
)

func ConnectDB() *sql.DB {
	psql_meta := fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname,
	)
	db, err := sql.Open("postgres", psql_meta)
	if err != nil {
		fmt.Println("[#] DB haven't connected!")
		log.Fatalln(err)
	}
	err = db.Ping()
	if err != nil {
		fmt.Println("[#] Cant get access to DB!")
		log.Fatalln(err)
	}
	fmt.Println("[#] DB connected!")
	return db
}
