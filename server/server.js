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

        //Declare custom Object Types

        //Sensors
        const sensorType = namespace.addObjectType({
            browseName: "SensorType",
            description: "A generic sensor that reads a process value."
        });

        namespace.addVariable({
            componentOf: sensorType,
            browseName: "Output",
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

        //Actuators
        const actuatorType = namespace.addObjectType({
            browseName: "ActuatorType",
            description: "Represents a piece of equipment that causes some action to occur."
        });

        namespace.addVariable({
            componentOf: actuatorType,
            browseName: "Input",
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

        //Declare custom objects

        //Folders
        const sensors = namespace.addObject({
            organizedBy: addressSpace.rootFolder.objects,
            typeDefinition: "FolderType",
            browseName: "Sensors"
        });

        const actuators = namespace.addObject({
            organizedBy: addressSpace.rootFolder.objects,
            typeDefinition: "FolderType",
            browseName: "Actuators"
        });

        // Sensors
        // Temp Sensor #1
        const tempSensor1 = namespace.addObject({
            browseName: "TempSensor#1",
            organizedBy: sensors,
            typeDefinition: tempSensorType
        });

        let ts1_min_temp = -40
        let ts1_max_temp = 125
        let ts1_min_v = 2.1
        let ts1_max_v = 3.6
        
        namespace.addVariable({
            propertyOf: tempSensor1,
            browseName: "Minimum Temperature",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: ts1_min_temp
                    });
                },
                set: function(variant) {
                    ts1_min_temp = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            propertyOf: tempSensor1,
            browseName: "Maximum Temperature",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: ts1_max_temp
                    });
                },
                set: function(variant) {
                    ts1_max_temp = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            propertyOf: tempSensor1,
            browseName: "Minimum Voltage",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: ts1_min_v
                    });
                },
                set: function(variant) {
                    ts1_min_v = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            propertyOf: tempSensor1,
            browseName: "Maximum Voltage",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: ts1_max_v
                    });
                },
                set: function(variant) {
                    ts1_max_v = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            componentOf: tempSensor1,
            browseName: "Output",
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(ts1_min_temp, ts1_max_temp)
                    })
                }
            }
        })

        // Temp Sensor #2
        const tempSensor2 = namespace.addObject({
            browseName: "TempSensor#2",
            organizedBy: sensors,
            typeDefinition: tempSensorType
        });

        let ts2_min_temp = -20
        let ts2_max_temp = 100
        let ts2_min_v = 1.5
        let ts2_max_v = 3.2
        
        namespace.addVariable({
            propertyOf: tempSensor2,
            browseName: "Minimum Temperature",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: ts2_min_temp
                    });
                },
                set: function(variant) {
                    ts2_min_temp = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            propertyOf: tempSensor2,
            browseName: "Maximum Temperature",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: ts2_max_temp
                    });
                },
                set: function(variant) {
                    ts2_max_temp = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            propertyOf: tempSensor2,
            browseName: "Minimum Voltage",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: ts2_min_v
                    });
                },
                set: function(variant) {
                    ts2_min_v = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            propertyOf: tempSensor2,
            browseName: "Maximum Voltage",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: ts2_max_v
                    });
                },
                set: function(variant) {
                    ts2_max_v = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            componentOf: tempSensor2,
            browseName: "Output",
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(ts2_min_temp, ts2_max_temp)
                    })
                }
            }
        })

        // Level Indicator
        const levelIndicator = namespace.addObject({
            browseName: "LevelIndicator",
            organizedBy: sensors,
            typeDefinition: levelIndicatorType
        });

        let min_work_temp = -40
        let max_work_temp = 85

        namespace.addVariable({
            propertyOf: levelIndicator,
            browseName: "Minimum Temperature",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: min_work_temp
                    });
                },
                set: function(variant) {
                    min_work_temp = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            propertyOf: levelIndicator,
            browseName: "Maximum Temperature",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: max_work_temp
                    });
                },
                set: function(variant) {
                    max_work_temp = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            componentOf: levelIndicator,
            browseName: "Output",
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(0, 100)
                    })
                }
            }
        })

        // Flow Sensor
        const flowSensor = namespace.addObject({
            browseName: "FlowSensor",
            organizedBy: sensors,
            typeDefinition: flowSensorType
        });
        
        let fs_min_v = 4.5
        let fs_max_v = 24

        namespace.addVariable({
            propertyOf: flowSensor,
            browseName: "Minimum Voltage",
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
            propertyOf: flowSensor,
            browseName: "Maximum Voltage",
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

        namespace.addVariable({
            componentOf: flowSensor,
            browseName: "Output",
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(0, 100)
                    })
                }
            }
        })

        // Actuators
        // Boiler
        const boiler = namespace.addObject({
            browseName: "Boiler",
            organizedBy: actuators,
            typeDefinition: boilerType
        });

        let nominal_pow = 3

        namespace.addVariable({
            propertyOf: boiler,
            browseName: "Nominal Power",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: nominal_pow
                    });
                },
                set: function(variant) {
                    nominal_pow = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            componentOf: boiler,
            browseName: "Input",
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(30, 70)
                    })
                }
            }
        })

        // Motor#1
        const motor1 = namespace.addObject({
            browseName: "Motor#1",
            organizedBy: actuators,
            typeDefinition: motorType
        });

        let m1_work_v = 24
        let m1_exit_speed = 6500

        namespace.addVariable({
            propertyOf: motor1,
            browseName: "Working Voltage",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: m1_work_v
                    });
                },
                set: function(variant) {
                    m1_work_v = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            propertyOf: motor1,
            browseName: "Exit Speed",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: m1_exit_speed
                    });
                },
                set: function(variant) {
                    m1_exit_speed = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            componentOf: motor1,
            browseName: "Input",
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(0, 20)
                    })
                }
            }
        })

        // Motor#2
        const motor2 = namespace.addObject({
            browseName: "Motor#2",
            organizedBy: actuators,
            typeDefinition: motorType
        });

        let m2_work_v = 32
        let m2_exit_speed = 7000

        namespace.addVariable({
            propertyOf: motor2,
            browseName: "Working Voltage",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: m2_work_v
                    });
                },
                set: function(variant) {
                    m2_work_v = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            propertyOf: motor2,
            browseName: "Exit Speed",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: m2_exit_speed
                    });
                },
                set: function(variant) {
                    m2_exit_speed = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            componentOf: motor2,
            browseName: "Input",
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(0, 30)
                    })
                }
            }
        })

        // Valve
        const valve = namespace.addObject({
            browseName: "Valve",
            organizedBy: actuators,
            typeDefinition: valveType
        });

        let exit_v = 330
        let base_type = "B9A"

        namespace.addVariable({
            propertyOf: valve,
            browseName: "Exit Voltage",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: exit_v
                    });
                },
                set: function(variant) {
                    exit_v = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            propertyOf: valve,
            browseName: "Base Type",
            dataType: "String",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.String, 
                        value: base_type
                    });
                },
                set: function(variant) {
                    base_type = variant.value;
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            componentOf: valve,
            browseName: "Input",
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(0, 100)
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
        console.log("The primary server endpoint url is ", endpointUrl);
    });
});

function getRandomValue(min, max) {
    return Math.random()*(max - min) + min;
}
