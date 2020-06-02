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
        let sensorType = namespace.addObjectType({
            browseName: "SensorType",
            description: "A generic sensor that reads a process value."
        });

        let output = namespace.addVariable({
            componentOf: sensorType,
            browseName: "Output",
            description: "The output of a generic sensor.",
            dataType: "Double"
        })

        let tempSensorType = namespace.addObjectType({
            browseName: "TempSensorType",
            subtypeOf: sensorType,
            description: "A sensor that reports the temperature of something."
        });

        let levelIndicatorType = namespace.addObjectType({
            browseName: "LevelIndicatorType",
            subtypeOf: sensorType,
            description: "A sensor that reports the level of a liquid in a tank."
        });

        //Actuators
        let actuatorType = namespace.addObjectType({
            browseName: "ActuatorType",
            description: "Represents a piece of equipment that causes some action to occur."
        });

        let input = namespace.addVariable({
            componentOf: actuatorType,
            browseName: "Input",
            description: "The input of a generic actuator.",
            dataType: "Double"
        })
        
        let boilerType = namespace.addObjectType({
            browseName: "BoilerType",
            subtypeOf: actuatorType,
            description: "A boiler used to produce steam for a turbine."
        });

        let motorType = namespace.addObjectType({
            browseName: "MotorType",
            subtypeOf: actuatorType,
            description: "An actuator that rotates."
        });

        let valveType = namespace.addObjectType({
            browseName: "ValveType",
            subtypeOf: actuatorType,
            decription: "An actuator that controls the flow through a pipe."
        });

        //Declare new objects

        //Folders
        let sensors = namespace.addObject({
            organizedBy: addressSpace.rootFolder.objects,
            typeDefinition: "FolderType",
            browseName: "Sensors"
        });

        let actuators = namespace.addObject({
            organizedBy: addressSpace.rootFolder.objects,
            typeDefinition: "FolderType",
            browseName: "Actuators"
        });

        //Sensors
        let tempSensor = namespace.addObject({
            browseName: "TempSensor",
            organizedBy: sensors,
            typeDefinition: tempSensorType
        });

        let levelIndicator = namespace.addObject({
            browseName: "LevelIndicator",
            organizedBy: sensors,
            typeDefinition: levelIndicatorType
        });

        let tempSensorOutput = namespace.addVariable({
            componentOf: tempSensor,
            browseName: "Output",
            dataType: "Double",
            value: {
                get: function() {
                    return new opcua.Variant({
                        dataType: opcua.DataType.Double,
                        value: getRandomValue(10, 50)
                    })
                }
            }
        })

        let levelIndicatorOutput = namespace.addVariable({
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

        //Actuators
        let boiler = namespace.addObject({
            browseName: "Boiler",
            organizedBy: actuators,
            typeDefinition: boilerType
        });

        let motor = namespace.addObject({
            browseName: "Motor",
            organizedBy: actuators,
            typeDefinition: motorType
        });

        let valve = namespace.addObject({
            browseName: "Valve",
            organizedBy: actuators,
            typeDefinition: valveType
        });

        let boilerInput = namespace.addVariable({
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

        let motorInput = namespace.addVariable({
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

        let valveInput = namespace.addVariable({
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
        let endpointUrl = server.endpoints[0].endpointDescriptions()[0].endpointUrl;
        console.log("The primary server endpoint url is ", endpointUrl);
    });
});

function getRandomValue(min, max) {
    return Math.random()*(max - min) + min;
}
