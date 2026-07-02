require("dotenv").config();

const express = require("express");
const cors = require("cors");

const connectDB = require("./config/db");

const authRoutes = require("./routes/authRoutes");
const vehicleRoutes = require("./routes/vehicleRoutes");
const assessmentRoutes = require("./routes/assessmentRoutes");

const protect = require("./middleware/authMiddleware");

// Create Express app FIRST
const app = express();

// Connect to MongoDB
connectDB();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/vehicles", vehicleRoutes);
app.use("/api/assessments", assessmentRoutes);

// Test Route
app.get("/", (req, res) => {
    res.json({
        message: "🚗 AutoFocus Backend Running Successfully"
    });
});

// Protected Route
app.get("/api/profile", protect, (req, res) => {
    res.json({
        message: "Protected Route",
        user: req.user
    });
});

// Start Server
const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
});