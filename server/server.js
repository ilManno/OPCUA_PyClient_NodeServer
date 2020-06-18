const path = require("path");

const opcua = require("node-opcua");

const server = new opcua.OPCUAServer({
    port: 4334,
    resourcePath: "/UA/NodeServer",
    buildInfo: {
        productName: "NodeServer1",
        buildNumber: "1",
        buildDate: new Date()
    },
    serverCertificateManager: new opcua.OPCUACertificateManager({
        automaticallyAcceptUnknownCertificate: true,
        rootFolder: path.join(__dirname, "certs")
    })
});

server.initialize(() => {
    console.log("OPC UA Server initialized.");

    function build_my_address_space(server) {
        const addressSpace = server.engine.addressSpace;
        const namespace = addressSpace.getOwnNamespace();

        // Declare custom Object Types
        // Sensors
        const sensorType = namespace.addObjectType({
            browseName: "SensorType",
            description: "A generic sensor that reads a process value."
        });

        namespace.addVariable({
            browseName: "Output",
            componentOf: sensorType,
            description: "The output of a generic sensor.",
            dataType: "Double"
        })

        const tempSensorType = namespace.addObjectType({
            browseName: "TempSensorType",
            subtypeOf: sensorType,
            description: "A sensor that reports the temperature of something."
        });

        const levelIndicatorType = namespace.addObjectType({
            browseName: "LevelIndicatorType",
            subtypeOf: sensorType,
            description: "A sensor that reports the level of a liquid in a tank."
        });

        const flowSensorType = namespace.addObjectType({
            browseName: "FlowSensorType",
            subtypeOf: sensorType,
            description: "A sensor that reports the flow of a liquid in a pipe."
        });

        // Actuators
        const actuatorType = namespace.addObjectType({
            browseName: "ActuatorType",
            description: "Represents a piece of equipment that causes some action to occur."
        });

        namespace.addVariable({
            browseName: "Input",
            componentOf: actuatorType,
            description: "The input of a generic actuator.",
            dataType: "Double"
        })

        const boilerType = namespace.addObjectType({
            browseName: "BoilerType",
            subtypeOf: actuatorType,
            description: "A boiler used to produce steam for a turbine."
        });

        const motorType = namespace.addObjectType({
            browseName: "MotorType",
            subtypeOf: actuatorType,
            description: "An actuator that rotates."
        });

        const valveType = namespace.addObjectType({
            browseName: "ValveType",
            subtypeOf: actuatorType,
            decription: "An actuator that controls the flow through a pipe."
        });

        // Declare custom Objects
        // Folders
        const sensors = namespace.addObject({
            browseName: "Sensors",
            organizedBy: addressSpace.rootFolder.objects,
            typeDefinition: "FolderType"
        });

        const actuators = namespace.addObject({
            browseName: "Actuators",
            organizedBy: addressSpace.rootFolder.objects,
            typeDefinition: "FolderType"
        });

        // Sensors
        // Temp Sensor #1
        const tempSensor1 = namespace.addObject({
            browseName: "TempSensor#1",
            organizedBy: sensors,
            typeDefinition: tempSensorType
        });

        let ts1_min_voltage = 2.1
        let ts1_max_voltage = 3.6
        const ts1_min_temp = -40
        const ts1_max_temp = 125

        namespace.addVariable({
            browseName: "Minimum Voltage",
            propertyOf: tempSensor1,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: ts1_min_voltage
                    });
                },
                set: function(variant) {
                    ts1_min_voltage = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            browseName: "Maximum Voltage",
            propertyOf: tempSensor1,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: ts1_max_voltage
                    });
                },
                set: function(variant) {
                    ts1_max_voltage = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addAnalogDataItem({
            browseName: "Temperature",
            engineeringUnitsRange: {
                low:  ts1_min_temp,
                high: ts1_max_temp
            },
            engineeringUnits: opcua.standardUnits.degree_celsius,
            componentOf: tempSensor1,
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(ts1_min_temp, ts1_max_temp)
                    });
                }
            }
        });

        // Temp Sensor #2
        const tempSensor2 = namespace.addObject({
            browseName: "TempSensor#2",
            organizedBy: sensors,
            typeDefinition: tempSensorType
        });

        let ts2_min_voltage = 1.5
        let ts2_max_voltage = 3.2
        const ts2_min_temp = -20
        const ts2_max_temp = 100

        namespace.addVariable({
            browseName: "Minimum Voltage",
            propertyOf: tempSensor2,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: ts2_min_voltage
                    });
                },
                set: function(variant) {
                    ts2_min_voltage = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            browseName: "Maximum Voltage",
            propertyOf: tempSensor2,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: ts2_max_voltage
                    });
                },
                set: function(variant) {
                    ts2_max_voltage = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addAnalogDataItem({
            browseName: "Temperature",
            engineeringUnitsRange: {
                low:  ts2_min_temp,
                high: ts2_max_temp
            },
            engineeringUnits: opcua.standardUnits.degree_celsius,
            componentOf: tempSensor2,
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(ts2_min_temp, ts2_max_temp)
                    });
                }
            }
        });

        // Level Indicator
        const levelIndicator = namespace.addObject({
            browseName: "LevelIndicator",
            organizedBy: sensors,
            typeDefinition: levelIndicatorType
        });

        let li_min_work_temp = -40
        let li_max_work_temp = 85
        const li_min_level = 0
        const li_max_level = 100

        namespace.addVariable({
            browseName: "Minimum Working Temperature",
            propertyOf: levelIndicator,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: li_min_work_temp
                    });
                },
                set: function(variant) {
                    li_min_work_temp = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            browseName: "Maximum Working Temperature",
            propertyOf: levelIndicator,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: li_max_work_temp
                    });
                },
                set: function(variant) {
                    li_max_work_temp = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addAnalogDataItem({
            browseName: "Level",
            engineeringUnitsRange: {
                low:  li_min_level,
                high: li_max_level
            },
            engineeringUnits: opcua.standardUnits.centimetre,
            componentOf: levelIndicator,
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(li_min_level, li_max_level)
                    });
                }
            }
        });

        // Flow Sensor
        const flowSensor = namespace.addObject({
            browseName: "FlowSensor",
            organizedBy: sensors,
            typeDefinition: flowSensorType
        });

        let fs_min_v = 4.5
        let fs_max_v = 24
        const fs_min_pressure = 0.1
        const fs_max_pressure = 1.2

        namespace.addVariable({
            browseName: "Minimum Voltage",
            propertyOf: flowSensor,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: fs_min_v
                    });
                },
                set: function(variant) {
                    fs_min_v = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            browseName: "Maximum Voltage",
            propertyOf: flowSensor,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: fs_max_v
                    });
                },
                set: function(variant) {
                    fs_max_v = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addAnalogDataItem({
            browseName: "Pressure",
            engineeringUnitsRange: {
                low:  fs_min_pressure,
                high: fs_max_pressure
            },
            engineeringUnits: opcua.standardUnits.bar,
            componentOf: flowSensor,
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(fs_min_pressure, fs_max_pressure)
                    });
                }
            }
        });

        // Actuators
        // Boiler
        const boiler = namespace.addObject({
            browseName: "Boiler",
            organizedBy: actuators,
            typeDefinition: boilerType
        });

        let b_op_pressure = 100
        const b_min_heat_input = 0
        const b_max_heat_input = 3000

        namespace.addVariable({
            browseName: "Operating Pressure",
            propertyOf: boiler,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: b_op_pressure
                    });
                },
                set: function(variant) {
                    b_op_pressure = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addAnalogDataItem({
            browseName: "Heat Input",
            engineeringUnitsRange: {
                low:  b_min_heat_input,
                high: b_max_heat_input
            },
            engineeringUnits: opcua.standardUnits.watt,
            componentOf: boiler,
            dataType: "Double",
            value: { 
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(b_min_heat_input, b_max_heat_input)
                    });
                }
            }
        });

        // Motor#1
        const motor1 = namespace.addObject({
            browseName: "Motor#1",
            organizedBy: actuators,
            typeDefinition: motorType
        });

        let m1_work_voltage = 24
        let m1_max_exit_speed = 6500
        const m1_min_power = 0
        const m1_max_power = 6500

        namespace.addVariable({
            browseName: "Working Voltage",
            propertyOf: motor1,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: m1_work_voltage
                    });
                },
                set: function(variant) {
                    m1_work_voltage = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            browseName: "Max Exit Speed",
            propertyOf: motor1,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: m1_max_exit_speed
                    });
                },
                set: function(variant) {
                    m1_max_exit_speed = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addAnalogDataItem({
            browseName: "Power",
            engineeringUnitsRange: {
                low:  m1_min_power,
                high: m1_max_power
            },
            engineeringUnits: opcua.standardUnits.watt,
            componentOf: motor1,
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(m1_min_power, m1_max_power)
                    });
                }
            }
        });

        // Motor#2
        const motor2 = namespace.addObject({
            browseName: "Motor#2",
            organizedBy: actuators,
            typeDefinition: motorType
        });

        let m2_work_voltage = 32
        let m2_max_exit_speed = 7000
        const m2_min_power = 0
        const m2_max_power = 7000

        namespace.addVariable({
            browseName: "Working Voltage",
            propertyOf: motor2,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: m2_work_voltage
                    });
                },
                set: function(variant) {
                    m2_work_voltage = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            browseName: "Max Exit Speed",
            propertyOf: motor2,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: m2_max_exit_speed
                    });
                },
                set: function(variant) {
                    m2_max_exit_speed = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addAnalogDataItem({
            browseName: "Power",
            engineeringUnitsRange: {
                low:  m2_min_power,
                high: m2_max_power
            },
            engineeringUnits: opcua.standardUnits.watt,
            componentOf: motor2,
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(m2_min_power, m2_max_power)
                    });
                }
            }
        });

        // Valve
        const valve = namespace.addObject({
            browseName: "Valve",
            organizedBy: actuators,
            typeDefinition: valveType
        });

        let v_exit_voltage = 330
        let v_base_type = "B9A"
        const v_min_pressure = 0.2
        const v_max_pressure = 1

        namespace.addVariable({
            browseName: "Exit Voltage",
            propertyOf: valve,
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: v_exit_voltage
                    });
                },
                set: function(variant) {
                    v_exit_voltage = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            browseName: "Base Type",
            propertyOf: valve,
            dataType: "String",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.String, 
                        value: v_base_type
                    });
                },
                set: function(variant) {
                    v_base_type = variant.value;
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addAnalogDataItem({
            browseName: "Pressure",
            engineeringUnitsRange: {
                low:  v_min_pressure,
                high: v_max_pressure
            },
            engineeringUnits: opcua.standardUnits.bar,
            componentOf: valve,
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(v_min_pressure, v_max_pressure)
                    })
                }
            }
        })
    }

    build_my_address_space(server);
    console.log("Address space initialized.");

    server.start(() => {
        console.log(`Server is now listening port ${server.endpoints[0].port}... (press CTRL+C to stop)`);
        const endpointUrl = server.endpoints[0].endpointDescriptions()[0].endpointUrl;
        console.log("The primary server endpoint url is:", endpointUrl);
    });
});

function getRandomValue(min, max) {
    return Math.random()*(max - min) + min;
}
