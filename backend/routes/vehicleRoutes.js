const express = require("express");
const router = express.Router();

const {
    addVehicle,
    getVehicles,
    updateVehicle,
    deleteVehicle
} = require("../controllers/vehicleController");

const protect = require("../middleware/authMiddleware");

// Protected Routes
router.post("/", protect, addVehicle);
router.get("/", protect, getVehicles);
router.put("/:id", protect, updateVehicle);
router.delete("/:id", protect, deleteVehicle);

module.exports = router;