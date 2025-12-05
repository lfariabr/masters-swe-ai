import express from "express";

const app = express();

app.get("/", (req, res) => {
  return res.json({ ok: true, runtime: "bun" });
});

app.listen(3000, () => {
  console.log("Bun app running on port 3000");
});
