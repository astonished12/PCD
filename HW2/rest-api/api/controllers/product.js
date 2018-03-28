const Product = require('../models/product');
const mongoose = require('mongoose');

exports.products_get_all = (req, res, next) => {
    Product.find()
    .select('name price _id productImage')
    .exec()
    .then( docs => {
            const response = {
                count: docs.length,
                products: docs.map(doc => {
                    return {
                        name: doc.name,
                        price: doc.price,
                        productImage: doc.productImage,
                        id: doc._id,
                        requst: {
                            type: 'GET',
                            url: 'http://localhost:3000/products/'+ doc._id
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
    });
}

exports.products_create_product =  (req, res, next) => {
    if(req.userData.role !== "admin"){
        return res.status(401).json({
            message: 'Unauthorized'
        }); 
    }

    const product = new Product({
        _id: new mongoose.Types.ObjectId(),
        name : req.body.name,
        price: req.body.price,
        productImage: req.file.path
    });
    
    product.save()
    .then(result => {
        console.log(result);
        res.status(201).json({
            message: 'Handling POST request to /products',
            createdProduct: {
                name: result.name,
                _id : result._id,
                requst: {
                    type: 'GET',
                    url: 'http://localhost:3000/products/'+ result._id
                }
            }
        });
    })
    .catch(err => {
        res.status(500).json({
            error: err
        });
    }); //in db

    
}

exports.products_get_product_by_id = (req, res, next) =>{
    const id = req.params.productId;
    Product.findById(id)
    .select('name price _id productImage')
    .exec()
    .then(doc => {
        console.log(doc);
        if(doc){
            res.status(200).json({
                product: doc,
                request: {
                    type: 'GET',
                    url: 'http://localhost/products'
                }
            });
        } else {
            res.status(404).json({
                message: "No valid entry found for proived ID"
            });
        }
    })
    .catch(err => {
        console.log(err);
        res.status(500).json({error:err});
    });
}

exports.products_update_product =   (req, res, next) => {
    if(req.userData.role !== "admin"){
        return res.status(401).json({
            message: 'Unauthorized'
        }); 
    }
    
    const id = req.params.productId;
    const updateOps  = {};
    for(const ops of req.body){
        updateOps[ops.propName] = ops.value;
    }

    Product.update({_id : id}, { $set: updateOps })
    .exec()
    .then(result => {
        console.log(result);
        res.status(200).json({
            message: 'Product update',
            request: {
                type: 'GET',
                url: 'http://localhost:3000/products/' + id   
            }
        });
    })
    .catch(err => {
        res.status(500).json({
            error: err
        })
    });
}

exports.products_delete_product = (req, res, next) => {
    const id = req.params.productId;
    Product.findById(id)
    .exec()
    .then(product => {
        if(req.userData.role !== "admin"){
            return res.status(401).json({
                message: 'Unauthorized'
            }); 
        } 
        
        if(product && product._id){
         Product.remove({ _id: id })
        .exec()
        .then(result => {
            res.status(200).json({
                message: 'Product deleted',
                request: {
                    type: 'POST',
                    url: 'http://localhost:3000/products/',
                    body: {name: 'String', price: 'Number'}
                }
                })
            });
        }
        else {
            return res.status(404).json({
                message: 'Product Id not found'
            });
        }
    })
    .catch(err => {
    console.log(err);
    res.status(500).json({error: err});
    });
    }