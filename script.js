const readings = {
    temperature: 22.5,
    humidity: 48.0,
    light: 125.0,
    voltage: 3.30,
    current: 120.0,
    power: 396.0,
    acceleration: null,
    gyroscope: null
};

function displayValue(value, decimalPlaces = 1) {
    if (
        value === null ||
        value === undefined ||
        !Number.isFinite(value)
    ) {
        return "N/A";
    }

    return value.toFixed(decimalPlaces);
}

function updateDashboard(data) {
    document.getElementById("temperature").textContent =
        displayValue(data.temperature, 1) + " °C";

    document.getElementById("humidity").textContent =
        displayValue(data.humidity, 1) + " %";

    document.getElementById("light").textContent =
        displayValue(data.light, 1) + " lux";

    document.getElementById("voltage").textContent =
        displayValue(data.voltage, 2) + " V";

    document.getElementById("current").textContent =
        displayValue(data.current, 1) + " mA";

    document.getElementById("power").textContent =
        displayValue(data.power, 1) + " mW";

    document.getElementById("acceleration").textContent =
        data.acceleration == null
            ? "N/A"
            : data.acceleration;

    document.getElementById("gyroscope").textContent =
        data.gyroscope == null
            ? "N/A"
            : data.gyroscope;
}

updateDashboard(readings);
