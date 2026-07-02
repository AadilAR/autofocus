const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs");

const Assessment = require("../models/Assessment");

exports.analyzeDamage = async (req, res) => {
    try {

        if (!req.file) {
            return res.status(400).json({
                message: "No image uploaded"
            });
        }

        const form = new FormData();

        form.append(
            "image",
            fs.createReadStream(req.file.path)
        );

        const flaskResponse = await axios.post(
            process.env.FLASK_API + "/predict",
            form,
            {
                headers: form.getHeaders()
            }
        );

        const assessment = await Assessment.create({
            image: req.file.path,
            predictionImage: flaskResponse.data.predictionImage,
            detections: flaskResponse.data.detections
        });

        res.json({
            message: "Assessment completed",
            assessment
        });

    } catch (error) {

        console.error(error);

        res.status(500).json({
            message: "Assessment failed",
            error: error.message
        });

    }
};

// Get all assessments
exports.getAssessments = async (req, res) => {
    try {

        const assessments = await Assessment.find().sort({
            createdAt: -1
        });

        res.json(assessments);

    } catch (error) {

        res.status(500).json({
            message: error.message
        });

    }
};

// Get one assessment by ID
exports.getAssessment = async (req, res) => {
    try {

        const assessment = await Assessment.findById(req.params.id);

        if (!assessment) {
            return res.status(404).json({
                message: "Assessment not found"
            });
        }

        res.json(assessment);

    } catch (error) {

        res.status(500).json({
            message: error.message
        });

    }
};