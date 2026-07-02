const mongoose = require("mongoose");

const assessmentSchema = new mongoose.Schema(
{
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "User"
    },

    vehicle: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Vehicle"
    },

    image: String,

    predictionImage: String,

    detections: [
        {
            class: String,
            confidence: Number,
            bbox: [Number]
        }
    ]
},
{
    timestamps: true
});

module.exports = mongoose.model("Assessment", assessmentSchema);