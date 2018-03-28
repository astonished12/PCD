const Order = require('../models/order');
const Product = require('../models/product');
const mongoose = require('mongoose');

exports.orders_get_all =  (req, res, next) => {
    Order.find()
    .select('product quantity')
    .populate('product', 'name') //add more info about products
    .exec()
    .then(docs => {
        const response = {
            count: docs.length,
            orders: docs.map(doc => {
                return {
                    product: doc.product,
                    quantity: doc.quantity,
                    id: doc._id,
                    request: {
                        type: 'GET',
                        url: 'http://localhost:3000/orders/'+ doc._id
                    }
                }
            })
        }
        
        res.status(200).json(response);
    })
    .catch(err => {
        res.status(500).json({
            error: err
        })
    }) 
}

exports.orders_create_order = (req, res, next) => {
    Product.findById(req.body.productId)
    .then(product => {
        if(!product){
            return res.status(404).json({
                message: 'Product not found'
            })
        }
        const order = new Order({
            _id: mongoose.Types.ObjectId(),
            quantity: req.body.quantity,
            product: req.body.productId
        });
        return order.save();                      
    })
    .then(result => {
        console.log(result);
        res.status(201).json({
            message: 'Order stored',
            createdOrder: {
                product: result.product,
                quantity: result.quantity,
                _id : result._id,
                requst: {
                    type: 'GET',
                    url: 'http://localhost:3000/orders/'+ result._id
                }
            }
        });        
    })
    .catch(err => {
        res.status(500).json({
            message: 'Product not found',
            error: err
        });
    })
  
}

exports.orders_get_order_by_id = (req, res, next) => {
    const id = req.params.orderId;

    Order.findById(id)
    .select('product quantity')
    .populate('product')
    .exec()
    .then(doc => {
        console.log(doc);
        if(doc){
            res.status(200).json({
              order: doc,
              request: {
                type: 'GET',
                url: 'http://localhost/orders'
            }  
            });
        } else {
            res.status(404).json({
                message: "No valid entry found for proived ID"
            });
        }
    })
    .catch(err => {
        res.status(500).json({
            error: err
        })
    })
    
}

exports.orders_delete_order =  (req, res, next) => {
    Order.remove({_id:req.params.orderId})
    .exec()
    .then(result => {
        res.status(200).json({
            message: 'Order deleted',
            request: {
                    type: 'POST',
                    url: 'http://localhost:3000/orders',
                    body: {
                        product: "ID",
                        quantity: "Number"
                    }
        }
    })
        
    })
    .catch(err=>{
        res.status(500).json({
            error: err
        })
    })
    
}