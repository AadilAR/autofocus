const mongoose = require("mongoose");

const connectDB = async () => {
    try {
        console.log("Connecting to:", process.env.MONGO_URI);

        const conn = await mongoose.connect(process.env.MONGO_URI);

        console.log(`MongoDB Connected: ${conn.connection.host}`);
    } catch (error) {
        console.error("========== FULL ERROR ==========");
        console.error(error);
        console.error("================================");
        process.exit(1);
    }
};

module.exports = connectDB;