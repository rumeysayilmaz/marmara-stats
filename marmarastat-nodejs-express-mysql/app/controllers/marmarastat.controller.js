const Marmarastat = require("../models/marmarastat.model.js");

// Retrieve all marmaraamounstat data from the database.
exports.findAll = (req, res) => {
  
};

// Retrieve last marmaraamounstat data from the database.
exports.findLast = (req, res) => {
  
};

exports.findAll = (req, res) => {
  Marmarastat.getAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving stats."
      });
    else res.send(data);
  });
};

exports.findLast = (req, res) => {
  Marmarastat.getLast((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving the last stat record."
      });
    else res.send(data);
  });
};
