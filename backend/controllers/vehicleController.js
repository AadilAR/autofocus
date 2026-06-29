const Vehicle = require("../models/Vehicle");

// Add Vehicle
const addVehicle = async (req, res) => {
    try {
        const {
            brand,
            model,
            year,
            registrationNumber,
            mileage,
            fuelType
        } = req.body;

        const vehicle = await Vehicle.create({
            user: req.user.id,
            brand,
            model,
            year,
            registrationNumber,
            mileage,
            fuelType
        });

        res.status(201).json({
            message: "Vehicle added successfully",
            vehicle
        });

    } catch (error) {
        res.status(500).json({
            message: error.message
        });
    }
};

// Get Logged-in User's Vehicles
const getVehicles = async (req, res) => {
    try {

        const vehicles = await Vehicle.find({
            user: req.user.id
        });

        res.status(200).json(vehicles);

    } catch (error) {

        res.status(500).json({
            message: error.message
        });

    }
};

// Update Vehicle
// Update Vehicle
const updateVehicle = async (req, res) => {
    try {
        const vehicle = await Vehicle.findById(req.params.id);

        if (!vehicle) {
            return res.status(404).json({
                message: "Vehicle not found"
            });
        }

        // Check ownership
        if (vehicle.user.toString() !== req.user.id) {
            return res.status(403).json({
                message: "Not authorized"
            });
        }

        const updatedVehicle = await Vehicle.findByIdAndUpdate(
            req.params.id,
            req.body,
            {
                new: true,
                runValidators: true
            }
        );

        res.status(200).json({
            message: "Vehicle updated successfully",
            vehicle: updatedVehicle
        });

    } catch (error) {
        res.status(500).json({
            message: error.message
        });
    }
};

// Delete Vehicle
// Delete Vehicle
const deleteVehicle = async (req, res) => {
    try {
        const vehicle = await Vehicle.findById(req.params.id);

        if (!vehicle) {
            return res.status(404).json({
                message: "Vehicle not found"
            });
        }

        // Check ownership
        if (vehicle.user.toString() !== req.user.id) {
            return res.status(403).json({
                message: "Not authorized"
            });
        }

        await vehicle.deleteOne();

        res.status(200).json({
            message: "Vehicle deleted successfully"
        });

    } catch (error) {
        res.status(500).json({
            message: error.message
        });
    }
};

module.exports = {
    addVehicle,
    getVehicles,
    updateVehicle,
    deleteVehicle
};