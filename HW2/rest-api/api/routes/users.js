const express = require('express');
const router = express.Router();
const checkAuth = require('../middleware/check-auth');

const UserController = require('../controllers/users');

router.post('/singup', UserController.users_sing_up);

router.post('/singin', UserController.users_login);

router.delete('/:userId',checkAuth, UserController.users_delete_by_id);

module.exports = router;