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

        //Sensors
        const tempSensor = namespace.addObject({
            browseName: "TempSensor",
            organizedBy: sensors,
            typeDefinition: tempSensorType
        });

        const levelIndicator = namespace.addObject({
            browseName: "LevelIndicator",
            organizedBy: sensors,
            typeDefinition: levelIndicatorType
        });

        const flowSensor = namespace.addObject({
            browseName: "FlowSensor",
            organizedBy: sensors,
            typeDefinition: flowSensorType
        });

        const min_temp = -40
        const max_temp = 125

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

        //Actuators
        const boiler = namespace.addObject({
            browseName: "Boiler",
            organizedBy: actuators,
            typeDefinition: boilerType
        });

        const motor = namespace.addObject({
            browseName: "Motor",
            organizedBy: actuators,
            typeDefinition: motorType
        });

        const valve = namespace.addObject({
            browseName: "Valve",
            organizedBy: actuators,
            typeDefinition: valveType
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
