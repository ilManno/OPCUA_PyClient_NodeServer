let path = require("path");

let opcua = require("node-opcua");

let server = new opcua.OPCUAServer({
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

        //Declare new Object Types

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

        //Declare new objects

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
        // Temp Sensor
        const tempSensor = namespace.addObject({
            browseName: "TempSensor",
            organizedBy: sensors,
            typeDefinition: tempSensorType
        });

        const min_temp = -40
        const max_temp = 125
        const min_v = 2.1 
        const max_v = 3.6      
        
        namespace.addVariable({
            propertyOf: tempSensor,
            browseName: "Min Temp",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: min_temp
                    });
                }
            }
        });

        namespace.addVariable({
            propertyOf: tempSensor,
            browseName: "Max Temp",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: max_temp
                    });
                }
            }
        });

        namespace.addVariable({
            propertyOf: tempSensor,
            browseName: "Min V",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: min_v
                    });
                }
            }
        });

        namespace.addVariable({
            propertyOf: tempSensor,
            browseName: "Max V",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: max_v
                    });
                }
            }
        });

        namespace.addVariable({
            componentOf: tempSensor,
            browseName: "Output",
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(min_temp, max_temp)
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

        namespace.addVariable({
            propertyOf: levelIndicator,
            browseName: "Min Temp",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: -40
                    });
                }
            }
        });

        namespace.addVariable({
            propertyOf: levelIndicator,
            browseName: "Max Temp",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: 85
                    });
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

        namespace.addVariable({
            propertyOf: flowSensor,
            browseName: "Min V",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: 4.5
                    });
                }
            }
        });

        namespace.addVariable({
            propertyOf: flowSensor,
            browseName: "Max V",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: 24
                    });
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

        namespace.addVariable({
            propertyOf: boiler,
            browseName: "Nominal Power",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: 3
                    });
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

        // Motor
        const motor = namespace.addObject({
            browseName: "Motor",
            organizedBy: actuators,
            typeDefinition: motorType
        });

        namespace.addVariable({
            propertyOf: motor,
            browseName: "Voltage",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: 24
                    });
                }
            }
        });

        namespace.addVariable({
            propertyOf: motor,
            browseName: "Exit Speed",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: 6500
                    });
                }
            }
        });

        namespace.addVariable({
            componentOf: motor,
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

        // Valve
        const valve = namespace.addObject({
            browseName: "Valve",
            organizedBy: actuators,
            typeDefinition: valveType
        });

        namespace.addVariable({
            propertyOf: valve,
            browseName: "Exit Voltage",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.Double, 
                        value: 330
                    });
                }
            }
        });

        namespace.addVariable({
            propertyOf: valve,
            browseName: "Base Type",
            dataType: "Double",
            value: {
                get: function() { 
                    return new opcua.Variant({ 
                        dataType: opcua.DataType.String, 
                        value: "B9A"
                    });
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
