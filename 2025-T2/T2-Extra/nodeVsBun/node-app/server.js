const express = require('express');
const app = express();

app.get('/', (req, res) => {
    return res.json({ ok: true, runtime: "node" });
})

const port = 3000;
app.listen(port, () => console.log(`Server running on http://localhost:${port}`));