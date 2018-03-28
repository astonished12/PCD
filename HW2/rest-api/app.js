const express = require('express');
const app = express();
const morgan = require('morgan');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const productsRoutes = require('./api/routes/products');
const ordersRoutes = require('./api/routes/orders');
const userRoutes = require('./api/routes/users');


mongoose.connect('mongodb://dancehan95:' + process.env.MONGO_ATLAS_PW + '@clothes-shop-shard-00-00-ngcrv.mongodb.net:27017,clothes-shop-shard-00-01-ngcrv.mongodb.net:27017,clothes-shop-shard-00-02-ngcrv.mongodb.net:27017/test?ssl=true&replicaSet=clothes-shop-shard-0&authSource=admin');
mongoose.Promise = global.Promise;


app.use(morgan('dev')); 
app.use('/uploads', express.static('uploads'));
app.use(bodyParser.urlencoded({extended: false}))
app.use(bodyParser.json());

app.use((req, res, next) => {
    res.header('Acces-Control-Allow-Origin', '*'); // acces to any client 
    res.header('Acces-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Authorization');
    if(req.method === 'OPTIONS'){
        res.header('Acces-Control-Allow-Methods', 'PUT, POST, PATCH, DELETE, GET');
        return res.status(200).json({});
    }
    next();
});

//ROUTES
app.use('/products', productsRoutes);
app.use('/orders', ordersRoutes);
app.use('/users', userRoutes);

app.use((req, res, next) => {
    const error = new Error('Not found');
    error.status = 404;
    next(error);
});

app.use((error, req, res, next) => {
    res.status(error.status || 500);
    res.json({
        error :{
            message: error.message
        }
    });
});

module.exports = app;