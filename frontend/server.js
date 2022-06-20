const express = require('express');
const serveStatic = require('serve-static');

const port = process.env.PORT || 7000;
const app = express();

app.use(serveStatic(__dirname + '/dist/spa'));
app.listen(port);
