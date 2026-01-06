# Firebase Realtime Database API Documentation

## Base URL
```bash
https://english-zone-2c406-default-rtdb.asia-southeast1.firebasedatabase.app
```
### 1. GET - Membaca Data
#### Get Semua Data
```bash
GET /questions.json
```
#### Response:
```bash
{
  "question1": {
    "text": "What is your name?",
    "correct": "A",
    "options": ["John", "Jane", "Bob"]
  },
  "question2": { ... }
}
```
#### Get Data Spesifik
```bash
GET /questions/question1.json
```
#### Get dengan Shallow Query
Hanya mengambil keys tanpa data lengkap:
```bash
GET /questions.json?shallow=true
```
#### Response:
```bash
{
  "question1": true,
  "question2": true
}
```
---
### 2. POST - Menambah Data Baru
```bash
POST /questions.json
Content-Type: application/json

{
  "text": "What is the capital of Indonesia?",
  "correct": "A",
  "options": ["Jakarta", "Bandung", "Surabaya"]
}
```
#### Response:
```bash
{
  "name": "-N1234abcd5678efgh"
}
```
> Note: POST akan generate unique key otomatis.
---
### 3. PUT - Update/Replace Data
#### Replace Entire Object
```bash
PUT /questions/question1.json
Content-Type: application/json

{
  "text": "Updated question",
  "correct": "B",
  "options": ["A", "B", "C"]
}
```
#### Set Data di Path Baru
```bash
PUT /questions/newQuestion.json
Content-Type: application/json

{
  "text": "New question",
  "correct": "C"
}
```
---
### 4. PATCH - Update Partial Data
Update sebagian field tanpa menghapus field lain:
```bash
PATCH /questions/question1.json
Content-Type: application/json

{
  "correct": "C"
}
```
---
### 5. DELETE - Menghapus Data
```bash
DELETE /questions/question1.json
```
#### Response:
```bash
null
```
---
### 6. Query & Filter Data
#### Order By Child
Mengurutkan berdasarkan field tertentu:
```bash
GET /questions.json?orderBy="correct"
```
#### Filter: Equal To
Ambil data dengan nilai spesifik:
```bash
GET /questions.json?orderBy="correct"&equalTo="A"
```
#### Filter: Start At & End At
Ambil data dalam rentang tertentu:
```bash
GET /questions.json?orderBy="correct"&startAt="A"&endAt="B"
```
#### Limit Results
#### Limit to First
Ambil N data pertama:
```bash
GET /questions.json?orderBy="$key"&limitToFirst=5
```
#### Limit to Last
Ambil N data terakhir:
```bash
GET /questions.json?orderBy="$key"&limitToLast=5
```
---
### 7. Advanced Queries
#### Order By Key
```bash
GET /questions.json?orderBy="$key"
```
#### Order By Value
Untuk data primitif (string, number):
```bash
httpGET /questions.json?orderBy="$value"
```
#### Complex Query Example
Ambil 10 pertanyaan dengan jawaban `"A"`, diurutkan berdasarkan key:
```bash
httpGET /questions.json?orderBy="correct"&equalTo="A"&limitToFirst=10
```
---
### 8. Print Format
#### Pretty Print
```bash
httpGET /questions.json?print=pretty
```
#### Silent (No Response Body)
```bash
httpPUT /questions/question1.json?print=silent
```
---
### 9. Server Values
#### Timestamp
```bash
PUT /questions/question1/createdAt.json
Content-Type: application/json

{
  ".sv": "timestamp"
}
```
---
### 10. Examples dengan JavaScript
#### Fetch API
#### GET
```bash
fetch('https://english-zone-2c406-default-rtdb.asia-southeast1.firebasedatabase.app/questions.json')
  .then(response => response.json())
  .then(data => console.log(data));
```
#### POST
```bash
fetch('https://english-zone-2c406-default-rtdb.asia-southeast1.firebasedatabase.app/questions.json', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: "New question",
    correct: "A",
    options: ["A", "B", "C"]
  })
})
.then(response => response.json())
.then(data => console.log(data));
```
#### PUT
```bash
fetch('https://english-zone-2c406-default-rtdb.asia-southeast1.firebasedatabase.app/questions/question1.json', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: "Updated question",
    correct: "B"
  })
})
.then(response => response.json());
```
#### PATCH
```bash
fetch('https://english-zone-2c406-default-rtdb.asia-southeast1.firebasedatabase.app/questions/question1.json', {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    correct: "C"
  })
})
.then(response => response.json());
```
#### DELETE
```bash
fetch('https://english-zone-2c406-default-rtdb.asia-southeast1.firebasedatabase.app/questions/question1.json', {
  method: 'DELETE'
})
.then(response => response.json());
```
#### Filter Query
```bash
// Get questions where correct = "A"
fetch('https://english-zone-2c406-default-rtdb.asia-southeast1.firebasedatabase.app/questions.json?orderBy="correct"&equalTo="A"')
  .then(response => response.json())
  .then(data => console.log(data));
```
---
### 11. Best Practices

- <b>Gunakan PATCH</b> untuk update partial data
- <b>Gunakan POST</b> untuk auto-generated keys
- <b>Gunakan PUT</b> untuk set data dengan key yang sudah ditentukan
- <b>Tambahkan indexOn</b> di rules untuk query yang sering digunaka
```bash
{
     "rules": {
       "questions": {
         ".indexOn": ["correct", "difficulty"]
       }
     }
   }
```
- <b>Batasi akses</b> di production dengan authentication rules
---
### 12. Error Handling
#### Common Error Responses
#### 400 Bad Request
```bash
{
  "error": "Invalid data; couldn't parse JSON object"
}
```
#### 401 Unauthorized
```bash
{
  "error": "Permission denied"
}
```
### 404 Not Found
> Data tidak ditemukan (akan return null)
---
### 13. Query Limitations

- `orderBy` harus digunakan dengan filter (`equalTo`, `startAt`, `endAt`)
- Hanya bisa menggunakan satu `orderBy` per query
- `limitToFirst` dan `limitToLast` tidak bisa digunakan bersamaan
- Index harus didefinisikan di rules untuk query pada child properties
---
## Resources

- [https://firebase.google.com/docs/database/rest/start](Firebase REST API Documentation)
- [https://firebase.google.com/docs/database/security](Firebase Security Rules)