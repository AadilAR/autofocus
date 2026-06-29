const mongoose = require("mongoose");

const vehicleSchema = new mongoose.Schema(
    {
        user: {
            type: mongoose.Schema.Types.ObjectId,
            ref: "User",
            required: true
        },

        brand: {
            type: String,
            required: true
        },

        model: {
            type: String,
            required: true
        },

        year: {
            type: Number,
            required: true
        },

        registrationNumber: {
            type: String,
            required: true
        },

        mileage: {
            type: Number,
            default: 0
        },

        fuelType: {
            type: String,
            enum: [
                "Petrol",
                "Diesel",
                "Hybrid",
                "Electric"
            ],
            required: true
        }

    },
    {
        timestamps: true
    }
);

module.exports = mongoose.model("Vehicle", vehicleSchema);