module.exports = app => {
  const marmarastats = require("../controllers/marmarastat.controller.js");

    // Retrieve all Customers
  app.get("/marmarastats", marmarastats.findAll);

  app.get("/marmarastatlast", marmarastats.findLast);

};