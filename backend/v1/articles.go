package v1

import (
	data "beyondf1/backend/data"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

type Article struct {
	Id           int       `json:"id"`
	Title        string    `json:"title"`
	Content      string    `json:"content"`
	Image_url    string    `json:"bg_url"`
	Source       string    `json:"source"`
	Tag          string    `json:"tag"`
	Created_date time.Time `json:"date"`
}

func SetArticle(w http.ResponseWriter, r *http.Request) {
	fmt.Println("[#] Hit endpoint: SetArticle")
	db := data.ConnectDB()
	defer db.Close()
	// set response headers
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		return
	}
	// fetch data from site
	var article Article
	reqBody, err := ioutil.ReadAll(r.Body)
	json.Unmarshal(reqBody, &article)
	if err != nil {
		fmt.Println("[#] Cant decode request json!")
		json.NewEncoder(w).Encode(map[string]string{"message": "Data incorect or mising!"})
		log.Println(err)
		return
	}
	sql_statement := `insert into article (title, content, created_date, image_url, source, tag) values ($1, $2, $3, $4, $5, $6);`
	_, err = db.Exec(
		sql_statement,
		article.Title, article.Content, time.Now(), article.Image_url, article.Source, article.Tag,
	)
	if err != nil {
		fmt.Println("[#] Cant insert data to database!")
		json.NewEncoder(w).Encode(map[string]string{"message": "Data incorect or mising!"})
		log.Println(err)
		return
	}
	json.NewEncoder(w).Encode(map[string]string{"message": fmt.Sprintf("New article created! Title: %s", article.Title)})
}

func GetArticle(w http.ResponseWriter, r *http.Request) {
	fmt.Println("[#] Hit endpoint: GetArticle")
	db := data.ConnectDB()
	defer db.Close()
	// set headers
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		return
	}
	// get id from url
	id := mux.Vars(r)["id"]
	// fetch data from db
	sql_statement := `select * from article where id=$1;`
	res := db.QueryRow(sql_statement, id)
	var article Article
	err := res.Scan(&article.Id, &article.Title, &article.Content, &article.Created_date, &article.Image_url, &article.Source, &article.Tag)
	if err != nil {
		fmt.Println("[#] Cant feth data from db!")
		json.NewEncoder(w).Encode(map[string]string{"message": "Data missing or id incorect"})
		log.Println(err)
		return
	}
	//fmt.Println(user)
	json.NewEncoder(w).Encode(article)
}

func GetArticles(w http.ResponseWriter, r *http.Request) {
	fmt.Println("[#] Hit endpoint: GetArticles")
	db := data.ConnectDB()
	defer db.Close()
	// set headers
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		return
	}
	// fetch data from db
	sql_statement := `select * from article order by created_date desc;`
	rows, err := db.Query(sql_statement)
	var articles []Article
	if err != nil {
		fmt.Println("[#] Cant feth data from db!")
		json.NewEncoder(w).Encode(map[string]string{"message": "Data missing or id incorect"})
		log.Println(err)
		return
	}
	defer rows.Close()
	for rows.Next() {
		var article Article
		if err = rows.Scan(&article.Id, &article.Title, &article.Content, &article.Created_date, &article.Image_url, &article.Source, &article.Tag); err != nil {
			log.Println(err)
		}
		articles = append(articles, article)
	}
	json.NewEncoder(w).Encode(articles)
}

func GetArticlesByTag(w http.ResponseWriter, r *http.Request) {
	fmt.Println("[#] Hit endpoint: GetArticlesByTag")
	db := data.ConnectDB()
	defer db.Close()
	// set headers
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		return
	}
	// get id from url
	tag := mux.Vars(r)["tag"]
	// fetch data from db
	sql_statement := `select * from article where tag=$1 order by created_date desc;`
	rows, err := db.Query(sql_statement, tag)
	var articles []Article
	if err != nil {
		fmt.Println("[#] Cant feth data from db!")
		json.NewEncoder(w).Encode(map[string]string{"message": "Data missing or id incorect"})
		log.Println(err)
		return
	}
	defer rows.Close()
	for rows.Next() {
		var article Article
		if err = rows.Scan(&article.Id, &article.Title, &article.Content, &article.Created_date, &article.Image_url, &article.Source, &article.Tag); err != nil {
			log.Println(err)
		}
		articles = append(articles, article)
	}
	json.NewEncoder(w).Encode(articles)
}

func PutArticle(w http.ResponseWriter, r *http.Request) {
	fmt.Println("[#] Hit endpoint: PutArticle")
	db := data.ConnectDB()
	defer db.Close()
	// set headers
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		return
	}
	// get id from url
	id := mux.Vars(r)["id"]
	// fetch data from db
	var article Article
	reqBody, err := ioutil.ReadAll(r.Body)
	json.Unmarshal(reqBody, &article)
	fmt.Println(article)
	if err != nil {
		fmt.Println("[#] Cant decode request json!")
		json.NewEncoder(w).Encode(map[string]string{"message": "Data incorect or mising!"})
		log.Println(err)
		return
	}
	sql_statement := `update article set title=$1, content=$2, image_url=$3, source=$4, tag=$5 where id=$6;`
	res, err := db.Exec(
		sql_statement,
		article.Title, article.Content, article.Image_url, article.Source, article.Tag, id,
	)
	rows_affected, _ := res.RowsAffected()
	if err != nil || rows_affected == 0 {
		fmt.Println("[#] Cant update data!")
		json.NewEncoder(w).Encode(map[string]string{"message": "Data incorect or mising!"})
		log.Println(err)
		return
	}
	json.NewEncoder(w).Encode(map[string]string{"message": "Data updated! Article updated."})
}

func DeleteArticle(w http.ResponseWriter, r *http.Request) {
	fmt.Println("[#] Hit endpoint: DeleteArticle")
	db := data.ConnectDB()
	defer db.Close()
	// set headers
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		return
	}
	// get id from url
	id := mux.Vars(r)["id"]
	// fetch data from db
	sql_statement := `delete from article where id=$1;`
	res, err := db.Exec(sql_statement, id)
	rows_affected, _ := res.RowsAffected()
	if err != nil || rows_affected == 0 {
		fmt.Println("[#] Cant delete data!")
		json.NewEncoder(w).Encode(map[string]string{"message": "Data incorect or mising!"})
		log.Println(err)
		return
	}
	json.NewEncoder(w).Encode(map[string]string{"message": "Data updated! Article deleted."})
}
