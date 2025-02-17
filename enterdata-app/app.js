const express = require('express');
const mysql = require('mysql2');
const cookieParser = require("cookie-parser");

const app = express();
const port = 4000;

app.use(cookieParser());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'))
app.set('view engine', 'pug');

function getDbConnection() {
    return mysql.createConnection({
      host: 'player-db',
      port: 3306,
      user: process.env.MYSQL_USER,
      password: process.env.MYSQL_PASSWORD,
      database: process.env.MYSQL_DATABASE
    });
}

// Route to insert data
app.post('/enter_data', (req, res) => {
  const { name, points } = req.body;
  if (!name || !points) {
    return res.status(400).json({ error: 'Invalid data' });
  }

  const db = getDbConnection();

  const sql = 'INSERT INTO players (name, points) VALUES (?, ?)';
  db.query(sql, [name, points], (err, result) => {
    db.end();
    if (err) return res.status(500).json({ error: err.message });
    console.log(`Player data entered, playerId :${result.insertId}`);
    res.redirect("/")
  });
});

app.get('/', async (req, res) => {
    try {
        const response = await fetch("http://auth-svc:5000/is_auth", {
            method: "GET",
            headers: {
                "Cookie": `session=${req.cookies.session}`
            }
        });
        if (!response.ok) {
            throw new Error("Failed to request auth status");
        }
        const data = await response.json()
        console.log(data)
        if (data.is_auth) {
            res.render('enter_data');
        } else {
            res.redirect(`http://localhost:5000/login?redirect=http://localhost:${port}`);
        }
    } catch (err) {
        console.error('Err getting auth status', err);
        res.status(500).send('Err getting auth status');
    }
  });

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
