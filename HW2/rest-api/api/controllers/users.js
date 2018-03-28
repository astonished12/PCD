const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/user');

exports.users_sing_up = (req, res, next) => {
    User.find({
        email: req.body.email
    }).exec()
    .then(user => {
        if(user.length >= 1){
            return res.status(409).json({
                message: "Email exists in db"
            });
        }
        else{
            bcrypt.hash(req.body.password, 10, (err, hash) => {
                if(err){
                        return res.status(500).json({
                        error: err
                    });
                } else {              
                    const user = new User({
                        _id: new mongoose.Types.ObjectId(),
                        email: req.body.email,
                        role: req.body.role,
                        password: hash
                    });
                    
                    user.save()
                    .then(result => {
                       console.log(result);
                       res.status(201).json({
                           message: 'User created',
                       }) 
                    })
                    .catch(err => {
                        res.status(500).json({
                            error: err
                        })
                    })
                }
           });
         }
 })
    
    
}

exports.users_login = (req, res, next) => {
    User.find({ email: req.body.email })
    .exec()
    .then(user => {
        if(user.length < 1){
            return res.status(401).json({
                message: 'Auth failed'
            });
        }

        bcrypt.compare(req.body.password, user[0].password, (err, result) => {
            if(err){
                return res.status(401).json({
                    message: 'Auth failed'
                });
            } 

            if(result){
                const token = jwt.sign({
                    email: user[0].email,
                    role: user[0].role,
                    userId: user[0]._id
                    },
                    
                   process.env.JWT_KEY,
                   {
                    expiresIn: "1h"
                   }       
                );

                return res.status(200).json({
                    message: 'Auth successful',
                    token: token
                });
            }

            return res.status(401).json({
                message: 'Auth failed'
            });
        })
    })
    .catch(err => {
        res.status(500).json({
            error: err
        })
    })
}

exports.users_delete_by_id = (req, res, next) => {
    
    User.findById(req.params.userId)
    .exec()
    .then(user => {  
        if(req.userData.role !== "admin"){
            return res.status(401).json({
                message: 'Unauthorized'
            }); 
        } 

        if(user && user._id){
            User.remove({ _id: req.params.userId })
            .exec()
            .then(result => {
                return res.status(200).json({
                    message: 'User deleted'
                })
            })
        }
        else {
            return res.status(404).json({
                message: 'Id not found'
            });
        }
        
    })
    .catch(err => {
        console.log("CE plm");
        res.status(500).json({
            error: err
        })
    })
   

}