const express = require('express');
const router = express.Router();
const multer = require("multer");

const storage = multer.diskStorage({
    destination: function(req, file, cb){
        cb(null, 'uploads/');
    },
    filename: function(req, file, cb){
        cb(null, Date.now() + file.originalname);
    }
});

const fileFilter = (req, file, cb) => {
    if(file.mimetype==='image/jpeg' || file.mimetype === 'image/png'){
        cb(null, true);
    } else {
        cb(null, false);
    }

};

const upload = multer({storage: storage, limits: {
    fileSize: 1024 * 1024 * 5,
    fileFilter: fileFilter
}});


const checkAuth = require('../middleware/check-auth');

const ProductsController = require('../controllers/product');

router.get('/', ProductsController.products_get_all);

router.post('/', upload.single('productImage'), checkAuth, ProductsController.products_create_product);

router.get('/:productId', ProductsController.products_get_product_by_id);

router.patch('/:productId', checkAuth, ProductsController.products_update_product);


router.delete('/:productId', checkAuth, ProductsController.products_delete_product);



module.exports = router;