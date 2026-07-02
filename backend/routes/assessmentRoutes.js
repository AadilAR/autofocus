const express = require("express");
const router = express.Router();

const upload = require("../middleware/upload");

const {
    analyzeDamage,
    getAssessments,
    getAssessment
} = require("../controllers/assessmentController");

router.post(
    "/analyze",
    upload.single("image"),
    analyzeDamage
);

router.get("/", getAssessments);

router.get("/:id", getAssessment);

module.exports = router;