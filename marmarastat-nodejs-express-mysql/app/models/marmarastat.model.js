const sql = require("./db.js");

// constructor
const Marmarastats = function(marmarastats) {
  this.Height = marmarastats.Height;
  this.CalculatedTotalNormals = marmarastats.CalculatedTotalNormals;
  this.CalculatedTotalActivated = marmarastats.CalculatedTotalActivated;
  this.CalculatedTotalLockedInLoops = marmarastats.CalculatedTotalLockedInLoops;
  this.BlockTime = marmarastats.BlockTime;
};

Marmarastats.getAll = result => {
  sql.query("SELECT Height, CalculatedTotalNormals, CalculatedTotalActivated, CalculatedTotalLockedInLoops, BlockTime FROM marmarastat", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log("marmarastats: ", res);
    result(null, res);
  });
};

Marmarastats.getLast = result => {
  sql.query("SELECT Height, CalculatedTotalNormals, CalculatedTotalActivated, CalculatedTotalLockedInLoops, BlockTime FROM marmarastat ORDER BY Height DESC LIMIT 1", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log("marmarastats: ", res);
    result(null, res);
  });
};

module.exports = Marmarastats;