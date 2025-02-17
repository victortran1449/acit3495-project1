const express = require('express');
const { MongoClient } = require('mongodb');
const cookieParser = require("cookie-parser");

const app = express();
const port = 3000;

app.use(cookieParser());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'))
app.set('view engine', 'pug');

const mongoUri = 'mongodb://stats-db:27017';
const dbName = process.env.MONGO_INITDB_DATABASE;

async function fetchStats() {
    let client;
    try {
        client = new MongoClient(mongoUri);
        await client.connect();
        const db = client.db(dbName);
        const statsCollection = db.collection(process.env.MONGO_COLLECTION);

        const stats = await statsCollection.find().sort({ timestamp: -1 }).limit(1).toArray();
        return stats.length > 0 ? stats[0] : undefined;
    } catch (err) {
        console.error("Error fetching stats:", err);
        return { error: "Failed to retrieve stats" };
    } finally {
        if (client) {
            await client.close();
        }
    }
}

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
            const stats = await fetchStats();
            res.render('show_results', { stats });
        } else {
            res.redirect(`http://localhost:5000/login?redirect=http://localhost:${port}`);
        }
    } catch (err) {
        console.error('Err getting auth status', err);
        res.status(500).send('Err getting auth status');
    }

});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
